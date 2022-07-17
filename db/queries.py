from .db_connect import db_query
from src.constants import STATUS


def create_table_if_not_exists(name):
    db_query(
        f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), phone_number INTEGER(12), level VARCHAR(30), status VARCHAR(20))")


def add_new_user(id: int):
    db_query(
        f"INSERT INTO users (id, status) VALUES ({id}, 'new_user')")


def get_user(id: int, column: str = None):
    return db_query(f"SELECT {'*' if column is None else column} FROM users WHERE id = {id}")


def set_user(id: int, column: str, value):
    db_query(
        f"UPDATE users SET {column} = {value} WHERE id = {id}")