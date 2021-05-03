import os
from shutil import copy
import time
from local_db import LocalDb, local_db_name
from logger import log_settings

app_log = log_settings()


class CreateTree:
    def __init__(self, tb_item, filename=None):
        self._new_local_path = "k:\\data\\paper_dtdt\\org_dir\\"
        self._name = tb_item.name
        self._surname = tb_item.surname
        self.filename = filename

    def __repr__(self):
       return "CreateTree_" + self.name + "_" + self.surname

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

    def copy_file(self, path_from, delete_from=False):
        try:
            if not os.path.isfile(self.fullpath):
                start_time = time.time()
                copy(path_from, self.fullpath)
                dur = time.time() - start_time
                app_log.info(f"File `{path_from}` copied for `{dur}` s")
            elif os.path.isfile(self.fullpath) and delete_from:
                os.remove(path_from)
                app_log.info(f"File `{path_from}` deleted")
            else:
                app_log.debug(f"File `{self.filename}` already exists")
        except (UnicodeEncodeError, UnicodeError):
            app_log.error(f"can not log the entry")

    def main(self, path_from, delete_from=False):
        self.create_dir()
        self.copy_file(path_from, delete_from)


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
