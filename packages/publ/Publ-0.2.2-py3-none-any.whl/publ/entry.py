# item.py
""" Functions for handling content items """

from __future__ import absolute_import, with_statement

import email
import functools
import logging
import os
import re
import shutil
import tempfile
import uuid
import hashlib
import arrow
import flask
from werkzeug.utils import cached_property

from . import config
from . import model
from . import queries
from . import path_alias
from . import markdown
from . import utils
from . import cards
from .utils import CallableProxy, TrueCallableProxy, make_slug

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@functools.lru_cache(10)
def load_message(filepath):
    """ Load a message from the filesystem """
    with open(filepath, 'r') as file:
        return email.message_from_file(file)


class Entry:
    """ A wrapper for an entry. Lazily loads the actual message data when
    necessary.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, record):
        """ Construct an Entry wrapper

        record -- the index record to use as the basis
        """

        self._record = record   # index record

    @cached_property
    def date(self):
        """ Get the display date of the entry, as an Arrow object """
        return arrow.get(self._record.display_date)

    @cached_property
    def link(self):
        """ Get a link to this entry. Accepts the same parameters as permalink;
        may be pre-redirected. """
        return CallableProxy(self._link)

    @cached_property
    def permalink(self):
        """ Get a canonical link to this entry. Accepts the following parameters:

        absolute -- if True, return an absolute/portable link (default: False)
        expand -- if True, expands the link to include the category and slug text;
            if False, it will only be the entry ID (default: True)
        """
        return CallableProxy(self._permalink)

    @cached_property
    def archive(self):
        """ Get a link to this entry in the context of a category template.
        Accepts the following arguments:

        paging -- Which pagination scheme to use; one of:
            day -- the entry date's day
            month -- the entry date's month
            year -- the entry date's year
            offset -- count-based pagination starting at the entry (default)
        category -- Which category to generate the link against (default: the entry's category)
        template -- Which template to generate the link for
        """
        return CallableProxy(self._archive_link)

    @cached_property
    def next(self):
        """ Get the next entry in the category, ordered by date.

        Accepts view parameters as arguments.
        """
        return CallableProxy(self._next)

    @cached_property
    def previous(self):
        """ Get the previous entry in the category, ordered by date.

        Accepts view parameters as arguments.
        """
        return CallableProxy(self._previous)

    @cached_property
    def category(self):
        """ Get the category this entry belongs to. """
        from .category import Category  # pylint: disable=cyclic-import
        return Category(self._record.category)

    def _link(self, *args, **kwargs):
        """ Returns a link, potentially pre-redirected """
        if self._record.redirect_url:
            return self._record.redirect_url

        return self._permalink(*args, **kwargs)

    def _permalink(self, absolute=False, expand=True, **kwargs):
        """ Returns a canonical URL for the item """
        return flask.url_for('entry',
                             entry_id=self._record.id,
                             category=self._record.category if expand else None,
                             slug_text=self._record.slug_text if expand else None,
                             _external=absolute,
                             **kwargs)

    def _archive_link(self, paging=None, template='', category=None, absolute=False):
        args = {
            'template': template,
            'category': category if category is not None else self.category,
        }
        if paging == 'day':
            args['date'] = self.date.format(utils.DAY_FORMAT)
        elif paging == 'month':
            args['date'] = self.date.format(utils.MONTH_FORMAT)
        elif paging == 'year':
            args['date'] = self.date.format(utils.YEAR_FORMAT)
        elif paging == 'week':
            args['date'] = self.date.span('week')[0].format(utils.WEEK_FORMAT)
        elif paging == 'offset' or not paging:
            args['id'] = self._record.id
        else:
            raise ValueError("Unknown paging type '{}'".format(paging))

        return flask.url_for('category', **args, _external=absolute)

    @cached_property
    def title(self):
        """ Get the title of the entry. Accepts the following argument:

        markup -- If True, convert it from Markdown to HTML; otherwise, strip
            all markdown (default: True)
        """
        return CallableProxy(self._title)

    def _title(self, markup=True, no_smartquotes=False):
        return markdown.render_title(self._record.title, markup, no_smartquotes)

    @cached_property
    def image_search_path(self):
        """ The relative image search path for this entry """
        return [os.path.dirname(self._record.file_path)] + self.category.image_search_path

    @cached_property
    def _message(self):
        """ get the message payload """
        filepath = self._record.file_path
        try:
            return load_message(filepath)
        except FileNotFoundError:
            expire_record(self._record)
            return None

    @cached_property
    def _entry_content(self):
        body, _, more = self._message.get_payload().partition('\n.....\n')
        if not more and body.startswith('.....\n'):
            # The entry began with a cut, which failed to parse.
            # This rule is easier/faster than dealing with a regex from
            # hell.
            more = body[6:]
            body = ''

        _, ext = os.path.splitext(self._record.file_path)
        is_markdown = ext == '.md'

        return body, more, is_markdown

    @cached_property
    def body(self):
        """ Get the above-the-fold entry body text """
        body, _, is_markdown = self._entry_content
        return TrueCallableProxy(
            self._get_markup,
            body,
            is_markdown) if body else CallableProxy(None)

    @cached_property
    def more(self):
        """ Get the below-the-fold entry body text """
        _, more, is_markdown = self._entry_content
        return TrueCallableProxy(
            self._get_markup,
            more,
            is_markdown) if more else CallableProxy(None)

    @cached_property
    def card(self):
        """ Get the entry's OpenGraph card """
        body, more, is_markdown = self._entry_content
        return TrueCallableProxy(
            self._get_card,
            body or more) if is_markdown else CallableProxy(None)

    @cached_property
    def last_modified(self):
        """ Get the date of last file modification """
        if self.get('Last-Modified'):
            return arrow.get(self.get('Last-Modified'))
        return self.date

    def _get_markup(self, text, is_markdown, **kwargs):
        """ get the rendered markup for an entry

            is_markdown -- whether the entry is formatted as Markdown
            kwargs -- parameters to pass to the Markdown processor
        """
        if is_markdown:
            return markdown.to_html(
                text,
                config=kwargs,
                image_search_path=self.image_search_path)

        return flask.Markup(text)

    def _get_card(self, text, **kwargs):
        """ Render out the tags for a Twitter/OpenGraph card for this entry. """

        def og_tag(key, val):
            """ produce an OpenGraph tag with the given key and value """
            return utils.make_tag('meta', {'property': key, 'content': val}, start_end=True)

        tags = og_tag('og:title', self.title)
        tags += og_tag('og:url', self.link(absolute=True))

        card = cards.extract_card(text, kwargs, self.image_search_path)
        for image in card.images:
            tags += og_tag('og:image', image)
        if card.description:
            tags += og_tag('og:description', card.description)

        return flask.Markup(tags)

    def __getattr__(self, name):
        """ Proxy undefined properties to the backing objects """

        if hasattr(self._record, name):
            return getattr(self._record, name)

        return self._message.get(name)

    @staticmethod
    def _get_first(query):
        """ Get the first entry in a query result """
        query = query.limit(1)
        return Entry(query[0]) if query.count() else None

    def _pagination_default_spec(self, kwargs):
        category = kwargs.get('category', self._record.category)
        return {
            'category': category,
            'recurse': kwargs.get('recurse', category != self._record.category)
        }

    def _previous(self, **kwargs):
        """ Get the previous item in any particular category """
        spec = self._pagination_default_spec(kwargs)
        spec.update(kwargs)

        return self._get_first(model.Entry.select().where(
            queries.build_query(spec) &
            queries.where_before_entry(self._record)
        ).order_by(-model.Entry.local_date, -model.Entry.id))

    def _next(self, **kwargs):
        """ Get the next item in any particular category """
        spec = self._pagination_default_spec(kwargs)
        spec.update(kwargs)

        return self._get_first(
            model.Entry.select().where(
                queries.build_query(spec) &
                queries.where_after_entry(self._record)
            ).order_by(model.Entry.local_date, model.Entry.id))

    def get(self, name, default=None):
        """ Get a single header on an entry """
        return self._message.get(name, default)

    def get_all(self, name):
        """ Get all related headers on an entry, as an iterable list """
        return self._message.get_all(name) or []

    def __eq__(self, other):
        if isinstance(other, int):
            return other == self._record.id
        # pylint:disable=protected-access
        return isinstance(other, Entry) and (other is self or other._record == self._record)


def guess_title(basename):
    """ Attempt to guess the title from the filename """

    base, _ = os.path.splitext(basename)
    return re.sub(r'[ _-]+', r' ', base).title()


def get_entry_id(entry, fullpath, assign_id):
    """ Get or generate an entry ID for an entry """
    warn_duplicate = False

    if 'Entry-ID' in entry:
        entry_id = int(entry['Entry-ID'])
    else:
        entry_id = None

    # See if we've inadvertently duplicated an entry ID
    if entry_id:
        other_entry = model.Entry.get_or_none(model.Entry.id == entry_id)
        if (other_entry
                and other_entry.file_path != fullpath
                and os.path.isfile(other_entry.file_path)):
            warn_duplicate = entry_id
            entry_id = None

    # Do we need to assign a new ID?
    if not entry_id and not assign_id:
        # We're not assigning IDs yet
        return None

    if not entry_id:
        # See if we already have an entry with this file path
        by_filepath = model.Entry.get_or_none(file_path=fullpath)
        if by_filepath:
            entry_id = by_filepath.id

    if not entry_id:
        # We still don't have an ID; generate one pseudo-randomly, based on the
        # entry file path. This approach averages around 0.25 collisions per ID
        # generated while keeping the entry ID reasonably short. count*N+C
        # averages 1/(N-1) collisions per ID.

        # database=None is to shut up pylint
        limit = max(10, model.Entry.select().count(database=None) * 5)
        attempt = 0

        while not entry_id or model.Entry.get_or_none(model.Entry.id == entry_id):
            # Stably generate a quasi-random entry ID from the file path
            md5 = hashlib.md5()
            md5.update("{} {}".format(fullpath, attempt).encode('utf-8'))
            entry_id = int.from_bytes(md5.digest(), byteorder='big') % limit
            attempt = attempt + 1

    if warn_duplicate is not False:
        logger.warning("Entry '%s' had ID %d, which belongs to '%s'. Reassigned to %d",
                       fullpath, warn_duplicate, other_entry.file_path, entry_id)

    return entry_id


def save_file(fullpath, entry):
    """ Save a message file out, without mangling the headers """
    with tempfile.NamedTemporaryFile('w', delete=False) as file:
        tmpfile = file.name
        # we can't just use file.write(str(entry)) because otherwise the
        # headers "helpfully" do MIME encoding normalization.
        # str(val) is necessary to get around email.header's encoding
        # shenanigans
        for key, val in entry.items():
            print('{}: {}'.format(key, str(val)), file=file)
        print('', file=file)
        file.write(entry.get_payload())
    shutil.move(tmpfile, fullpath)


def scan_file(fullpath, relpath, assign_id):
    """ scan a file and put it into the index """
    # pylint: disable=too-many-branches,too-many-statements

    # Since a file has changed, the lrucache is invalid.
    load_message.cache_clear()

    try:
        entry = load_message(fullpath)
    except FileNotFoundError:
        # The file doesn't exist, so remove it from the index
        record = model.Entry.get_or_none(file_path=fullpath)
        if record:
            expire_record(record)
        return True

    with model.lock:
        entry_id = get_entry_id(entry, fullpath, assign_id)
        if entry_id is None:
            return False

        fixup_needed = False

        basename = os.path.basename(relpath)
        title = entry['title'] or guess_title(basename)

        values = {
            'file_path': fullpath,
            'category': entry.get('Category', os.path.dirname(relpath)),
            'status': model.PublishStatus[entry.get('Status', 'SCHEDULED').upper()],
            'entry_type': entry.get('Entry-Type', ''),
            'slug_text': make_slug(entry['Slug-Text'] or title),
            'redirect_url': entry['Redirect-To'],
            'title': title,
        }

        entry_date = None
        if 'Date' in entry:
            try:
                entry_date = arrow.get(entry['Date'], tzinfo=config.timezone)
            except arrow.parser.ParserError:
                entry_date = None
        if entry_date is None:
            del entry['Date']
            entry_date = arrow.get(
                os.stat(fullpath).st_ctime).to(config.timezone)
            entry['Date'] = entry_date.format()
            fixup_needed = True

        if 'Last-Modified' in entry:
            last_modified_str = entry['Last-Modified']
            try:
                last_modified = arrow.get(
                    last_modified_str, txinfo=config.timezone)
            except arrow.parser.ParserError:
                last_modified = arrow.get()
                del entry['Last-Modified']
                entry['Last-Modified'] = last_modified.format()
                fixup_needed = True

        values['display_date'] = entry_date.datetime
        values['utc_date'] = entry_date.to('utc').datetime
        values['local_date'] = entry_date.naive

        logger.debug("getting entry %s with id %d", fullpath, entry_id)
        record, created = model.Entry.get_or_create(
            id=entry_id, defaults=values)

        if not created:
            logger.debug("Reusing existing entry %d", record.id)
            record.update(**values).where(model.Entry.id ==
                                          record.id).execute()

        # Update the entry ID
        if str(record.id) != entry['Entry-ID']:
            del entry['Entry-ID']
            entry['Entry-ID'] = str(record.id)
            fixup_needed = True

        if not 'UUID' in entry:
            entry['UUID'] = str(uuid.uuid5(
                uuid.NAMESPACE_URL, 'file://' + fullpath))
            fixup_needed = True

        # add other relationships to the index
        for alias in entry.get_all('Path-Alias', []):
            path_alias.set_alias(alias, entry=record)
        for alias in entry.get_all('Path-Unalias', []):
            path_alias.remove_alias(alias)

        if fixup_needed:
            save_file(fullpath, entry)

        return record


def expire_record(record):
    """ Expire a record for a missing entry """
    load_message.cache_clear()

    with model.lock:
        # This entry no longer exists so delete it, and anything that references it
        # SQLite doesn't support cascading deletes so let's just clean up
        # manually
        model.PathAlias.delete().where(model.PathAlias.entry == record).execute()
        record.delete_instance(recursive=True)
