from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    # Establece una conexion con la base de datos SQLite
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tablas
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS work (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        theme TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS work_author (
        work_id INTEGER NOT NULL,
        author_id INTEGER NOT NULL,
        PRIMARY KEY (work_id, author_id),
        FOREIGN KEY (work_id) REFERENCES work(id) ON DELETE CASCADE,
        FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS edition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        work_id INTEGER NOT NULL,
        year INTEGER,
        publisher TEXT,
        isbn TEXT UNIQUE,
        cover_url TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (work_id) REFERENCES work(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edition_id INTEGER NOT NULL,
        barcode TEXT UNIQUE,
        location TEXT,
        status TEXT CHECK (status IN ('available','loaned','repair','lost')) DEFAULT 'available',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (edition_id) REFERENCES edition(id) ON DELETE CASCADE
    );
    ''')
    conn.commit()
    conn.close()

create_tables()

# Punto de entrada principal
@app.route('/', methods=['GET'])
def root():
    # Devuelve un mensaje de bienvenida y los endpoints disponibles
    return jsonify({"message": "Bienvenido a la API de la Biblioteca! Endpoints disponibles: /work, /author"})

# Operaciones CRUD para 'work'
@app.route('/work', methods=['GET', 'POST'])
def manage_works():
    # Maneja las operaciones CRUD para la tabla 'work'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener todos los registros de la tabla 'work'
        cursor.execute('SELECT * FROM work')
        works = cursor.fetchall()
        conn.close()
        return jsonify([dict(work) for work in works])

    if request.method == 'POST':
        # Insertar un nuevo registro en la tabla 'work'
        new_work = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO work (title, theme, created_at, updated_at) VALUES (?, ?, ?, ?)',
                       (new_work['title'], new_work.get('theme'), now, now))
        conn.commit()
        conn.close()
        return jsonify({'id': cursor.lastrowid}), 201

@app.route('/work/<int:work_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_work(work_id):
    # Maneja operaciones CRUD para un registro especifico de la tabla 'work'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener un registro especifico de la tabla 'work'
        cursor.execute('SELECT * FROM work WHERE id = ?', (work_id,))
        work = cursor.fetchone()
        conn.close()
        if work is None:
            return jsonify({'error': 'Trabajo no encontrado'}), 404
        return jsonify(dict(work))

    if request.method == 'PUT':
        # Actualizar un registro especifico de la tabla 'work'
        updated_work = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('UPDATE work SET title = ?, theme = ?, updated_at = ? WHERE id = ?',
                       (updated_work['title'], updated_work.get('theme'), now, work_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Trabajo actualizado'})

    if request.method == 'DELETE':
        # Eliminar un registro especifico de la tabla 'work'
        cursor.execute('DELETE FROM work WHERE id = ?', (work_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Trabajo eliminado'})

# Operaciones CRUD para 'author'
@app.route('/author', methods=['GET', 'POST'])
def manage_authors():
    # Maneja las operaciones CRUD para la tabla 'author'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener todos los registros de la tabla 'author'
        cursor.execute('SELECT * FROM author')
        authors = cursor.fetchall()
        conn.close()
        return jsonify([dict(author) for author in authors])

    if request.method == 'POST':
        # Insertar un nuevo registro en la tabla 'author'
        new_author = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO author (full_name, created_at, updated_at) VALUES (?, ?, ?)',
                       (new_author['full_name'], now, now))
        conn.commit()
        conn.close()
        return jsonify({'id': cursor.lastrowid}), 201

@app.route('/author/<int:author_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_author(author_id):
    # Maneja operaciones CRUD para un registro especifico de la tabla 'author'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener un registro especifico de la tabla 'author'
        cursor.execute('SELECT * FROM author WHERE id = ?', (author_id,))
        author = cursor.fetchone()
        conn.close()
        if author is None:
            return jsonify({'error': 'Autor no encontrado'}), 404
        return jsonify(dict(author))

    if request.method == 'PUT':
        # Actualizar un registro especifico de la tabla 'author'
        updated_author = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('UPDATE author SET full_name = ?, updated_at = ? WHERE id = ?',
                       (updated_author['full_name'], now, author_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Autor actualizado'})

    if request.method == 'DELETE':
        # Eliminar un registro especifico de la tabla 'author'
        cursor.execute('DELETE FROM author WHERE id = ?', (author_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Autor eliminado'})

# Operaciones CRUD para 'work_author'
@app.route('/work_author', methods=['GET', 'POST'])
def manage_work_authors():
    # Maneja las operaciones CRUD para la tabla 'work_author'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener todos los registros de la tabla 'work_author'
        cursor.execute('SELECT * FROM work_author')
        work_authors = cursor.fetchall()
        conn.close()
        return jsonify([dict(work_author) for work_author in work_authors])

    if request.method == 'POST':
        # Insertar un nuevo registro en la tabla 'work_author'
        new_work_author = request.get_json()
        cursor.execute('INSERT INTO work_author (work_id, author_id) VALUES (?, ?)',
                       (new_work_author['work_id'], new_work_author['author_id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Relacion Trabajo-Autor creada'}), 201

@app.route('/work_author/<int:work_id>/<int:author_id>', methods=['DELETE'])
def delete_work_author(work_id, author_id):
    # Eliminar un registro especifico de la tabla 'work_author'
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM work_author WHERE work_id = ? AND author_id = ?', (work_id, author_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Relacion Trabajo-Autor eliminada'})

# Operaciones CRUD para 'edition'
@app.route('/edition', methods=['GET', 'POST'])
def manage_editions():
    # Maneja las operaciones CRUD para la tabla 'edition'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener todos los registros de la tabla 'edition'
        cursor.execute('SELECT * FROM edition')
        editions = cursor.fetchall()
        conn.close()
        return jsonify([dict(edition) for edition in editions])

    if request.method == 'POST':
        # Insertar un nuevo registro en la tabla 'edition'
        new_edition = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO edition (work_id, year, publisher, isbn, cover_url, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (new_edition['work_id'], new_edition['year'], new_edition['publisher'], new_edition['isbn'], new_edition['cover_url'], now, now))
        conn.commit()
        conn.close()
        return jsonify({'id': cursor.lastrowid}), 201

@app.route('/edition/<int:edition_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_edition(edition_id):
    # Maneja operaciones CRUD para un registro especifico de la tabla 'edition'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener un registro especifico de la tabla 'edition'
        cursor.execute('SELECT * FROM edition WHERE id = ?', (edition_id,))
        edition = cursor.fetchone()
        conn.close()
        if edition is None:
            return jsonify({'error': 'Edicion no encontrada'}), 404
        return jsonify(dict(edition))

    if request.method == 'PUT':
        # Actualizar un registro especifico de la tabla 'edition'
        updated_edition = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('UPDATE edition SET work_id = ?, year = ?, publisher = ?, isbn = ?, cover_url = ?, updated_at = ? WHERE id = ?',
                       (updated_edition['work_id'], updated_edition['year'], updated_edition['publisher'], updated_edition['isbn'], updated_edition['cover_url'], now, edition_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Edicion actualizada'})

    if request.method == 'DELETE':
        # Eliminar un registro especifico de la tabla 'edition'
        cursor.execute('DELETE FROM edition WHERE id = ?', (edition_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Edicion eliminada'})

# Operaciones CRUD para 'item'
@app.route('/item', methods=['GET', 'POST'])
def manage_items():
    # Maneja las operaciones CRUD para la tabla 'item'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener todos los registros de la tabla 'item'
        cursor.execute('SELECT * FROM item')
        items = cursor.fetchall()
        conn.close()
        return jsonify([dict(item) for item in items])

    if request.method == 'POST':
        # Insertar un nuevo registro en la tabla 'item'
        new_item = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('INSERT INTO item (edition_id, barcode, location, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                       (new_item['edition_id'], new_item['barcode'], new_item['location'], new_item['status'], now, now))
        conn.commit()
        conn.close()
        return jsonify({'id': cursor.lastrowid}), 201

@app.route('/item/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_item(item_id):
    # Maneja operaciones CRUD para un registro especifico de la tabla 'item'
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Obtener un registro especifico de la tabla 'item'
        cursor.execute('SELECT * FROM item WHERE id = ?', (item_id,))
        item = cursor.fetchone()
        conn.close()
        if item is None:
            return jsonify({'error': 'Item no encontrado'}), 404
        return jsonify(dict(item))

    if request.method == 'PUT':
        # Actualizar un registro especifico de la tabla 'item'
        updated_item = request.get_json()
        now = datetime.now().isoformat()
        cursor.execute('UPDATE item SET edition_id = ?, barcode = ?, location = ?, status = ?, updated_at = ? WHERE id = ?',
                       (updated_item['edition_id'], updated_item['barcode'], updated_item['location'], updated_item['status'], now, item_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Item actualizado'})

    if request.method == 'DELETE':
        # Eliminar un registro especifico de la tabla 'item'
        cursor.execute('DELETE FROM item WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Item eliminado'})

# Operaciones CRUD adicionales para otras tablas pueden ser agregadas de manera similar

if __name__ == '__main__':
    # Inicia la aplicacion Flask en el puerto 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
