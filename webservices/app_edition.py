import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'crud_dr.db'

# --- Funciones de Utilidad de Base de Datos ---

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    conn = sqlite3.connect(DATABASE)
    # Habilita el acceso por nombre de columna
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la tabla 'edition' si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Nota: También deberías crear la tabla 'work' para que la FOREIGN KEY funcione
    # Creamos 'work' solo como placeholder para la relación
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    """)
    
    # Creación de la tabla 'edition'
    cursor.execute("""
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
    """)
    conn.commit()
    conn.close()

# Inicializa la base de datos al inicio
init_db()

# --- Servicios Web CRUD (API RESTful) ---

## 1. CREATE: Crear una nueva edición (POST /editions)

@app.route('/editions', methods=['POST'])
def create_edition():
    """Inserta un nuevo registro de edición."""
    data = request.get_json()
    # Campos requeridos para la inserción
    required_fields = ['work_id', 'year', 'publisher', 'isbn']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos (work_id, year, publisher, isbn)"}), 400

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO edition (work_id, year, publisher, isbn, cover_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (
            data['work_id'],
            data['year'],
            data['publisher'],
            data['isbn'],
            data.get('cover_url') # cover_url es opcional en el cuerpo
        ))
        conn.commit()
        # Devuelve el ID del registro insertado (para un mejor feedback)
        edition_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return jsonify({"message": "Edición creada con éxito", "id": edition_id}), 201
    
    except sqlite3.IntegrityError as e:
        # Captura errores de unicidad (como ISBN duplicado) o clave foránea
        return jsonify({"error": f"Error de integridad: {e}"}), 409
    
    except Exception as e:
        return jsonify({"error": f"Error interno: {e}"}), 500
    
    finally:
        conn.close()

## 2. READ: Obtener todas las ediciones (GET /editions)

@app.route('/editions', methods=['GET'])
def get_all_editions():
    """Obtiene una lista de todas las ediciones."""
    conn = get_db_connection()
    editions = conn.execute("SELECT * FROM edition ORDER BY year DESC").fetchall()
    conn.close()
    
    # Convierte las filas de sqlite3.Row a diccionarios
    editions_list = [dict(row) for row in editions]
    return jsonify(editions_list), 200

## 3. READ: Obtener una edición por ID (GET /editions/<id>)

@app.route('/editions/<int:edition_id>', methods=['GET'])
def get_edition(edition_id):
    """Obtiene una edición específica por su ID."""
    conn = get_db_connection()
    edition = conn.execute("SELECT * FROM edition WHERE id = ?", (edition_id,)).fetchone()
    conn.close()

    if edition is None:
        return jsonify({"message": f"Edición con ID {edition_id} no encontrada"}), 404
    
    # Convierte a diccionario y devuelve
    return jsonify(dict(edition)), 200

## 4. UPDATE: Actualizar una edición (PUT /editions/<id>)

@app.route('/editions/<int:edition_id>', methods=['PUT'])
def update_edition(edition_id):
    """Actualiza los campos de una edición existente."""
    data = request.get_json()
    conn = get_db_connection()

    # Primero, comprueba si la edición existe
    existing_edition = conn.execute("SELECT id FROM edition WHERE id = ?", (edition_id,)).fetchone()
    if existing_edition is None:
        conn.close()
        return jsonify({"message": f"Edición con ID {edition_id} no encontrada"}), 404

    # Prepara la consulta de actualización dinámicamente
    fields_to_update = []
    values = []
    
    # Mapeo de campos permitidos
    allowed_fields = ['work_id', 'year', 'publisher', 'isbn', 'cover_url']

    for field in allowed_fields:
        if field in data:
            fields_to_update.append(f"{field} = ?")
            values.append(data[field])

    if not fields_to_update:
        conn.close()
        return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400

    # Agrega la actualización de 'updated_at'
    fields_to_update.append("updated_at = datetime('now')")
    
    # Construye y ejecuta la sentencia SQL
    sql_query = "UPDATE edition SET " + ", ".join(fields_to_update) + " WHERE id = ?"
    values.append(edition_id)

    try:
        conn.execute(sql_query, tuple(values))
        conn.commit()
        return jsonify({"message": f"Edición con ID {edition_id} actualizada con éxito"}), 200

    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Error de integridad: {e}"}), 409
    
    except Exception as e:
        return jsonify({"error": f"Error interno: {e}"}), 500

    finally:
        conn.close()


## 5. DELETE: Eliminar una edición (DELETE /editions/<id>)

@app.route('/editions/<int:edition_id>', methods=['DELETE'])
def delete_edition(edition_id):
    """Elimina una edición específica por su ID."""
    conn = get_db_connection()
    
    # Ejecuta el borrado
    cursor = conn.execute("DELETE FROM edition WHERE id = ?", (edition_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": f"Edición con ID {edition_id} no encontrada para eliminar"}), 404
    
    conn.close()
    return jsonify({"message": f"Edición con ID {edition_id} eliminada con éxito"}), 200

# --- Ejecución de la Aplicación ---

if __name__ == '__main__':
    # Esto ejecuta el servidor de desarrollo de Flask
    # Accede a http://127.0.0.1:5000/
    app.run(host='0.0.0.0',port= 8000,debug=True)