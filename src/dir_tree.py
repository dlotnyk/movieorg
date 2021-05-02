import os
from shutil import copy
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

    def copy_file(self, path_from):
        if not os.path.isfile(self.fullpath):
            copy(path_from, self.fullpath)
            app_log.info(f"File `{path_from}` copied")
        else:
            app_log.debug(f"File `{self.filename}` already exists")

    def main(self, path_from):
        self.create_dir()
        self.copy_file(path_from)


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
