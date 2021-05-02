import os
from typing import List, Tuple

from logger import log_settings
from local_db import LocalDb, local_db_name
app_log = log_settings()
local_path = "k:\\data\\paper_dtdt\\some_other\\"


class ParseFiles:
    def __init__(self, db_item):
        self._name = db_item.name
        self._surname = db_item.surname
        self._files: str = ""
        print(f" parsing for {db_item.name}, {db_item.surname}")

    def __repr__(self):
        return "ParseFiles_" + self.name + "_" + self.surname

    @property
    def name(self):
        return self._name.lower()

    @property
    def surname(self):
        return self._surname.lower()

    @staticmethod
    def walk_files():
        for root, dirs, file_list in os.walk(local_path):
            for files in file_list:
                yield files

    @property
    def get_title(self):
        return self._files.split(".mp4")[0].lower()

    def find_equals(self):
        app_log.info(f"parsing for {repr(self)}")
        for self._files in self.walk_files():
            if self.name in self.get_title and self.surname in self.get_title:

                print(self.get_title)


if __name__ == "__main__":
    app_log.info("Main app starts.")
    datab = LocalDb(db_name=local_db_name)
    datab.open_session()
    for item in datab.select_all:
        a = ParseFiles(item)
        a.find_equals()
    datab.close_session()
    datab.close_engine()
    app_log.info("Main app ends.")

