import os
from shutil import copy
import time
from concurrent.futures import ThreadPoolExecutor
from local_db import LocalDb, local_db_name
from logger import log_settings
from typing import List, Dict, Set

app_log = log_settings()


class CreateTree:
    _new_list: List = list()
    _old_set: Set = set()
    _name = None
    _surname = None
    p_from: str = "path_from"
    p_to: str = "path_to"

    def __init__(self):
        self._new_local_path: str = "k:\\data\\paper_dtdt\\org_dir\\"
        self._new_list: List[Dict] = list()
        self._old_set: Set = set()

    def __repr__(self):
        return "CreateTree_" + self.name + "_" + self.surname

    def parse_tb(self, tb_item, filename):
        self._name = tb_item.name
        self._surname = tb_item.surname
        self.filename = filename

    @property
    def old_set(self) -> Set:
        return self._old_set

    @property
    def new_list(self) -> List:
        return self._new_list

    @property
    def fullpath(self):
        return os.path.join(self.get_dir_name, self.filename)

    @property
    def name(self):
        return self._name.lower()

    @property
    def surname(self):
        return self._surname.lower()

    @property
    def get_dir_name(self):
        current_dir = self.name + "_" + self.surname
        return os.path.join(self._new_local_path, current_dir)

    def create_dir(self):
        if not os.path.exists(self.get_dir_name):
            app_log.info(f"Directory `{self.get_dir_name}` does not exists")
            os.makedirs(self.get_dir_name)
            app_log.info(f"Directory `{self.get_dir_name}` created")
        else:
            app_log.debug(f"Directory `{self.get_dir_name}` already exists")

    def create_copy_list(self, path_from):
        path_log = path_from.encode("utf-8")
        try:
            if not os.path.isfile(self.fullpath):
                self._new_list.append({self.p_from: path_from,
                                       self.p_to: self.fullpath})
                app_log.info(f"File `{path_log}` added to list")
            self._old_set.add(path_from)
        except (UnicodeEncodeError, UnicodeError):
            app_log.error(f"can not log the entry")

    def copy_file(self, items: Dict):
        try:
            path_from = items.get(self.p_from)
            path_to = items.get(self.p_to)
            path_log = path_from.encode("utf-8")
            if not os.path.exists(path_to):
                start_time = time.time()
                copy(path_from, path_to)
                dur = time.time() - start_time
                app_log.info(f"File {path_log}: is copied for `{dur}` sec")
            else:
                app_log.info(f"File `{path_log}` already exists")
        except (UnicodeEncodeError, UnicodeError):
            app_log.error(f"can not log the entry")
        except Exception as ex:
            app_log.error(f"Error while copy: {ex}")

    def copy_pool(self):
        if self.new_list:
            app_log.info("Starting copying")
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(self.copy_file, self.new_list)
            app_log.info("Ends copying")
        else:
            app_log.info("Nothing to copy")

    def remove_set(self):
        if self.old_set:
            app_log.info("Starting removing")
            try:
                for fr in self.old_set:
                    path_log = fr.encode("utf-8")
                    os.remove(fr)
                    app_log.info(f"File `{path_log}` deleted")
                app_log.info("Ends removing")
            except (UnicodeEncodeError, UnicodeError):
                app_log.error(f"can not log the entry")
            except Exception as ex:
                app_log.error(f"Error while remove: {ex}")
        else:
            app_log.info("Nothing to remove")

    def main(self, tb_item, filename, path_from: str, delete_from=False):
        self.parse_tb(tb_item, filename)
        self.create_dir()
        self.create_copy_list(path_from)


if __name__ == "__main__":
    app_log.info("Create Dir Tree app starts.")
    datab = LocalDb(db_name=local_db_name)
    datab.open_session()
    for item in datab.select_all:
        a = CreateTree(tb_item=item)
        a.create_dir()
    datab.close_session()
    datab.close_engine()
    app_log.info("Create Dir Tree app ends.")
