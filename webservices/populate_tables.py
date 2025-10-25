import sqlite3
from datetime import datetime
import random

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def populate_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Populate 'work'
    for i in range(1, 21):
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO work (title, theme, created_at, updated_at) VALUES (?, ?, ?, ?)',
                       (f'Work Title {i}', f'Theme {i}', now, now))

    # Populate 'author'
    for i in range(1, 21):
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO author (full_name, created_at, updated_at) VALUES (?, ?, ?)',
                       (f'Author Name {i}', now, now))

    # Populate 'work_author'
    for i in range(1, 21):
        cursor.execute('INSERT INTO work_author (work_id, author_id) VALUES (?, ?)',
                       (i, i))

    # Populate 'edition'
    for i in range(1, 21):
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO edition (work_id, year, publisher, isbn, cover_url, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (i, random.randint(1900, 2025), f'Publisher {i}', f'ISBN-{i:05}', f'http://example.com/cover{i}.jpg', now, now))

    # Populate 'item'
    for i in range(1, 21):
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO item (edition_id, barcode, location, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                       (i, f'BARCODE-{i:05}', f'Location {i}', 'available', now, now))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_tables()
