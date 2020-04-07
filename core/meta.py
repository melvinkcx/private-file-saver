import os
import sqlite3
from typing import Union, Tuple


class MetaStore:
    def __init__(self, db_path, target_path, db_name=".pfs_metadata"):
        # Keep metastore backed up in the S3 bucket
        self._store_path = os.path.join(db_path, db_name)
        self._store_rel_path = os.path.relpath(self._store_path, target_path)

        # Connecting it will auto create an empty DB,
        # if not already exists
        self._conn = sqlite3.connect(self._store_path, check_same_thread=False)

        # Initialize DB if necessary
        if not self._is_db_initialized():
            self._initialize_db()

    @property
    def path(self):
        return self._store_path

    @property
    def rel_path(self):
        return self._store_rel_path

    def is_metastore(self, abs_path):
        return self._store_path == abs_path

    def _is_db_initialized(self):
        """
        Check if DB is created with tables initialized
        """
        cur = self._conn.cursor()
        cur.execute(''' 
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name='last_sync' 
        ''')
        record = cur.fetchone()
        if record and len(record) > 0 and record[0] == 1:
            return True
        return False

    def _initialize_db(self):
        """
        Create db file and tables
        """
        cur = self._conn.cursor()
        cur.execute('''
        CREATE TABLE last_sync (
            rel_file_path varchar,
            last_synced float 
        )
        ''')
        self._conn.commit()

    def get_last_synced(self, rel_file_path) -> Tuple[str, Union[float, None]]:
        cur = self._conn.cursor()
        cur.execute('''
            SELECT rel_file_path, last_synced
            FROM last_sync
            WHERE rel_file_path=?
        ''', (rel_file_path,))
        record = cur.fetchone()
        cur.close()
        return record or (rel_file_path, 0.0)

    def set_last_synced(self, rel_file_path, last_synced):
        # FIXME Should be Upsert
        cur = self._conn.cursor()
        cur.execute('''
                INSERT INTO last_sync(rel_file_path, last_synced)
                VALUES (?, ?)
                ''', (rel_file_path, last_synced))
        self._conn.commit()
        cur.close()
