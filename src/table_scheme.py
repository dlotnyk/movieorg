import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

main_table_name = "main_table"


class MainTable(Base):
    """
    The main Table
    """
    __tablename__ = main_table_name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return "Main Table"
