import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from typing import List, Tuple

from logger import log_settings
from table_scheme import MainTable, main_table_name, Base

app_log = log_settings()


class LocalDb:
    """
    local db based of sqlite3
    """
    _table_name = main_table_name
    _local_path = "k:\\data\\paper_dtdt\\some_other\\"

    def __init__(self, db_name: str) -> None:
        try:
            self.db_name = db_name
            cur_path = os.path.dirname(os.getcwd())
            self.db_path = os.path.join(cur_path, db_name)
            connector = "sqlite:///" + self.db_path
            self._db_engine = db.create_engine(connector)
            app_log.debug(f"Engine creates for {db_name}")
        except Exception as ex:
            app_log.error(f"Can not create an engine: `{ex}`")

    @property
    def db_engine(self):
        return self._db_engine

    def create_main_table(self):
        metadata = db.MetaData()
        self.main_tb = db.Table(self._table_name, metadata,
                                db.Column("id", db.Integer, primary_key=True, autoincrement=True),
                                db.Column("name"), db.String,
                                db.Column("surname")
                                )
        try:
            Base.metadate.create_all(self.db_engine)
            app_log.debug(f"Table `{self._table_name}` was created")
        except Exception as ex:
            app_log.error(f"Can not create table: `{ex}`")
