import os
from typing import List, Tuple

from logger import log_settings
from local_db import LocalDb, local_db_name
from dir_tree import CreateTree
app_log = log_settings()
local_path = "k:\\data\\paper_dtdt\\some_other\\"


class ParseFiles:
    def __init__(self, tb_item):
        self._root = local_path
        self._name = tb_item.name
        self._surname = tb_item.surname
        self._files: str = ""
        print(f" parsing for {tb_item.name}, {tb_item.surname}")

    def __repr__(self):
        return "ParseFiles_" + self.name + "_" + self.surname

    @property
    def name(self):
        return self._name.lower()

    @property
    def surname(self):
        return self._surname.lower()

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def full_path(self):
        return os.path.join(self.root, self._files)

    def walk_files(self):
        for self.root, dirs, file_list in os.walk(local_path):
            for files in file_list:
                yield files

    @property
    def get_title(self):
        return self._files.split(".mp4")[0].lower()

    def find_equals(self):
        app_log.info(f"parsing for {repr(self)}")
        for self._files in self.walk_files():
            if self.name in self.get_title and self.surname in self.get_title:
                yield self._files, self.full_path


if __name__ == "__main__":
    app_log.info("Main app starts.")
    datab = LocalDb(db_name=local_db_name)
    datab.open_session()
    for table_item in datab.select_all:
        # CreateTree(tb_item=table_item).create_dir()
        for movie in ParseFiles(tb_item=table_item).find_equals():
            CreateTree(tb_item=table_item,
                       filename=movie[0]).copy_file(movie[1])
    datab.close_session()
    datab.close_engine()
    app_log.info("Main app ends.")

