# -*- coding: utf8 -*-
import csv
import logging
import six

from ..api import default_api_retry
from .base_db_index import BaseMLIndex
from ..backend_mixin import BackendMixin


class BackendMLIndex(BackendMixin, BaseMLIndex):
    def __init__(self, connection, config, session, handle_api):
        super(BackendMLIndex, self).__init__(connection, config, session, handle_api)

    def _create_table_if_needed(self):
        pass

    def set_entries(self, entries, isolation_token=None):
        if not entries:
            return

        if isinstance(entries, six.string_types):
            self.set_entries_from_url(entries, isolation_token)
        else:
            self.set_entries_from_list(entries, isolation_token)

    def set_entries_from_url(self, file_name, isolation_token):
        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/index/stage' % self._volume_id

            msg = {
                'index_url': file_name,
                'isolation_token': isolation_token,
            }

            self._handle_api(self._config, session, 'post', url, msg, retry=default_api_retry(), async=True)

    def set_entries_from_list(self, entries, isolation_token):
        rows = []
        for name, sha, ctime, mtime, mode, uid, gid, size, url in self._decode_entries(entries):
            row = {
                'name': name,
                'sha': sha,
                'ctime': ctime,
                'mtime': mtime,
                'mode': mode,
                'uid': uid,
                'gid': gid,
                'size': size,
                'url': url,
            }

            rows.append(row)

        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/index/stage' % self._volume_id
            msg = {
                'entries': rows,
                'isolation_token': isolation_token,
            }

            self._handle_api(self._config, session, 'post', url, msg, retry=default_api_retry())

    class ChangeSetIter(object):
        def __init__(self, data, data_type=None):
            self.__data = data
            data_type = data_type or 'csv'

            if data_type.lower() == 'csv':
                self.__reader = csv.DictReader(data)

        def __iter__(self):
            return self

        def next(self):
            data = next(self.__reader)
            return data['name'], data['op']

        def __next__(self):
            return self.next()

    def get_changeset(self, index_url, isolation_token):
        if not index_url:
            logging.debug('no data provided')
            return

        logging.debug('add data %s', index_url)

        def decode_iter(gen):
            for line in gen:
                if not isinstance(line, six.string_types):
                    line = line.decode()

                yield line

        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/index/stage' % self._volume_id

            msg = {
                'index_url': index_url,
                'dry_mode': True,
                'isolation_token': isolation_token,
            }

            result = self._handle_api(self._config, session, 'post', url, msg, retry=default_api_retry())

            r = session.get(result['change_set_url'], stream=True)
            r.raise_for_status()

            return self.ChangeSetIter(decode_iter(r.iter_lines()))

    def begin_commit(self, commit_sha, tree_id, ts):
        raise NotImplementedError(self.begin_commit)

    def end_commit(self):
        raise NotImplementedError(self.end_commit)
