import os
import sqlite3
from datetime import datetime

import config


def init_db():
    db_dir = os.path.dirname(config.DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(config.DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS prices
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            date DATETIME)"""
    )
    conn.close()


def save_price(name, price):
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute(
        "INSERT INTO prices (name, price, date) VALUES (?, ?, ?)",
        (name, price, datetime.now()),
    )
    conn.commit()
    conn.close()
