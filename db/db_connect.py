from sqlite3 import connect, version
from db.constants import DB_NAME
import logging


def db_query(query: str):
    """Performs database commands."""
    db = connect(DB_NAME, check_same_thread=False)
    logging.info("Connected to SQLite database %s with version %s",
                 DB_NAME, version)
    with db:
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    if db:
        db.commit()
        cursor.close()
        logging.info("Database connection closed.")
    return result
