import os
from db.constants import DB_NAME, ROOT_DIR, DB_PATH


def check_db_exists():
    if not os.path.exists(DB_PATH):
        with open(os.path.join(ROOT_DIR, DB_NAME), 'w'):
            pass
    return True
