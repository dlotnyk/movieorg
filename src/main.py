from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from typing import List, Tuple

from logger import log_settings
from table_scheme import MainTable

app_log = log_settings()