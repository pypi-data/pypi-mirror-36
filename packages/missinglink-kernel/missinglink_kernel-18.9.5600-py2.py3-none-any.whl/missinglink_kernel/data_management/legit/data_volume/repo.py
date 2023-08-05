# -*- coding: utf8 -*-
import logging

import os
from ..path_utils import has_moniker
from ..dulwich import objects
from ..dulwich.repo import Repo
from ..api import handle_api
from ..data_volume_config import DataVolumeConfig
from .. import BigQueryConnection, DatastoreConnection, BackendConnection
from .. import BigQueryMLIndex, BackendMLIndex
from .. import BackendMetadataDB, BigQueryMetadataDB
from .. import DatastoreRefContainer, BackendRefContainer


class MLIgnoreFilterManager(object):
    def is_ignored(self, relpath):
        return False


DEFAULT_ENCODING = 'utf-8'


def make_bytes(c):
    if not isinstance(c, bytes):
        return c.encode(DEFAULT_ENCODING)

    return c


class MlRepo(Repo):
    def __init__(self, config, repo_root, read_only=False, require_path=True, data_volume_config=None, **kwargs):
        if data_volume_config is None:
            general_config_path = config.config_file_abs_path if config is not None else None
            self.__data_volume_config = DataVolumeConfig(repo_root, general_config_path=general_config_path)
        else:
            self.__data_volume_config = data_volume_config

        self.__in_transactions = False
        self.__config = config
        self.__connections = {}
        self.__read_only = read_only
        self.__metadata = None
        self.__session = kwargs.pop('session', None)
        self.__extra_repo_params = kwargs

        super(MlRepo, self).__init__(repo_root, self.data_volume_config.data_path, require_path=require_path)

    @property
    def _config(self):
        return self.__config

    def close(self):
        for connection in self.__connections.values():
            connection.close()

        super(MlRepo, self).close()

    __connection_class_mapping = {
        'bq': BigQueryConnection,
        'datastore': DatastoreConnection,
    }

    def rel_path(self, full_path):
        local_path = not has_moniker(self.data_path)

        if local_path:
            return os.path.relpath(full_path, self.data_path)

        return full_path

    def full_path(self, rel_path):
        local_path = not has_moniker(self.data_path)

        if local_path:
            return os.path.join(self.data_path, rel_path)

        return self.data_path + '/' + rel_path

    def __create_connection(self, name, **kwargs):
        kwargs.update(self.data_volume_config.db_config)
        kwargs['read_only'] = self.__read_only
        kwargs['session'] = self.__session
        kwargs['data_volume_config'] = self.data_volume_config
        kwargs['user_id'] = self._config.user_id if self._config is not None else None

        kwargs.update(self.__extra_repo_params)

        connection_class = self.__connection_class_mapping.get(self.data_volume_config.db_type, BackendConnection)

        return connection_class(**kwargs)

    def start_transactions(self):
        for connection in self.__connections.values():
            connection.start_transactions()

        self.__in_transactions = True

    def end_transactions(self):
        for connection in self.__connections.values():
            connection.end_transactions()

        self.__in_transactions = False

    def rollback_transactions(self):
        for connection in self.__connections.values():
            connection.rollback_transactions()

        self.__in_transactions = False

    def _connection_by_name(self, name, **kwargs):
        if name not in self.__connections:
            connection = self.__create_connection(name, **kwargs)

            if self.__in_transactions:
                connection.start_transactions()

            self.__connections[name] = connection

        return self.__connections[name]

    def __create_metadata(self):
        if self.data_volume_config.db_type == 'bq':
            return BigQueryMetadataDB(self._connection_by_name('metadata'))

        return BackendMetadataDB(self._connection_by_name('metadata'), self._config, self.__session, handle_api, **self.__extra_repo_params)

    @property
    def metadata(self):
        if self.__metadata is None:
            self.__metadata = self.__create_metadata()

        return self.__metadata

    @property
    def data_volume_config(self):
        return self.__data_volume_config

    def open_index(self):
        if self.data_volume_config.db_type == 'bq':
            return BigQueryMLIndex(self._connection_by_name('main'))

        return BackendMLIndex(self._connection_by_name('main'), self._config, self.__session, handle_api)

    def create_ref_container(self):
        if self.data_volume_config.object_store_type == 'disk':
            return super(MlRepo, self).create_ref_container()

        if self.data_volume_config.db_type == 'bq':
            return DatastoreRefContainer(self._connection_by_name('datastore'))

        return BackendRefContainer(self._connection_by_name('main'), self._config, self.__session, handle_api)

    def create_object_store(self):
        from .. import GCSObjectStore, NullObjectStore, BackendGCSObjectStore

        if self.data_volume_config.object_store_type == 'disk':
            return super(MlRepo, self).create_object_store()

        if self.data_volume_config.object_store_type == 'null':
            return NullObjectStore()

        bucket_name = self.data_volume_config.object_store_config.get('bucket_name')

        processes = self.data_volume_config.object_store_config.get('processes', -1)
        use_multiprocess = self.data_volume_config.get_boolean('object_store', 'use_multiprocess', True)

        if bucket_name is None:
            return BackendGCSObjectStore(
                self._connection_by_name('backend'),
                self._config, self.__session, handle_api, use_multiprocess=use_multiprocess, processes=processes)

        return GCSObjectStore(self._connection_by_name('gcs'), use_multiprocess=use_multiprocess, processes=processes)

    def get_config_stack(self):
        return DataVolumeConfig(self.repo_root)

    def get_ignore_filter_manager(self):
        return MLIgnoreFilterManager()

    def _get_user_identity(self):
        import jwt

        data = jwt.decode(self._config.id_token, verify=False) if self.__config.id_token else {}

        return '{name} <{email}>'.format(**data).encode('utf8')

    def has_change_set(self, ref='HEAD'):
        ref = ref.encode('ascii')

        try:
            ref_sha = self.refs[ref]

            head_tree_sha = self[ref_sha].tree
        except KeyError:  # in case of empty tree
            head_tree_sha = objects.Tree().id

        index = self.open_index()

        commit_id = index.get_commit_id()

        return None if commit_id == head_tree_sha else commit_id

    def remote_commit(self, message, isolation_token):
        msg = {
            'message': message,
            'isolation_token': isolation_token,
        }

        url = "data_volumes/{volume_id}/commit".format(volume_id=self.data_volume_config.volume_id)

        return handle_api(self._config, self.__session, 'post', url, msg, async=True)

    def local_commit(self, message):
        tree_id = self.has_change_set()

        if not tree_id:
            return

        self.start_transactions()
        try:
            commit_hash = self.do_commit(message=make_bytes(message), tree=tree_id).decode('ascii')

            self.metadata.commit(commit_hash, tree_id)

            self.end_transactions()
        except Exception:
            logging.exception('failure doing commit, preforming rollback')
            self.rollback_transactions()
            raise

    def commit(self, message, isolation_token=None):
        if self.data_volume_config.is_local:
            return self.local_commit(message)

        return self.remote_commit(message, isolation_token)
