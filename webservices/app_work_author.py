import sqlite3
from flask import Flask, jsonify, request

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DATABASE_NAME = 'crud_peme.db'

def get_db_connection():
    """Establece la conexión a la base de datos SQLite."""
    # La conexión NO requiere host, puerto, usuario o contraseña
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre
    return conn

app = Flask(__name__)

# --- SERVICIOS CRUD PARA work_author ---

# 1. CREATE (Crear una nueva relación)
@app.route('/work_author', methods=['POST'])
def create_work_author():
    data = request.get_json()
    work_id = data.get('work_id')
    author_id = data.get('author_id')

    if not work_id or not author_id:
        return jsonify({'error': 'work_id y author_id son requeridos.'}), 400

    try:
        conn = get_db_connection()
        # Insertar la nueva relación
        conn.execute(
            "INSERT INTO work_author (work_id, author_id) VALUES (?, ?)",
            (work_id, author_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Relación work_author creada con éxito', 'work_id': work_id, 'author_id': author_id}), 201
    except sqlite3.IntegrityError:
        # Se activa si la PK ya existe o si las FK son inválidas
        return jsonify({'error': 'La relación ya existe o work_id/author_id no son válidos.'}), 409
    except Exception as e:
        return jsonify({'error': f'Error al crear la relación: {e}'}), 500

# 2. READ All (Listar todas las relaciones)
@app.route('/work_author', methods=['GET'])
def get_all_work_authors():
    conn = get_db_connection()
    # Selecciona todos los registros
    relations = conn.execute("SELECT work_id, author_id FROM work_author").fetchall()
    conn.close()
    
    # Convierte los objetos Row de SQLite a una lista de diccionarios
    relations_list = [dict(relation) for relation in relations]
    
    return jsonify(relations_list), 200

# 3. READ One (Buscar una relación específica)
# Usamos los dos IDs en el cuerpo de la solicitud (Body) para ser más práctico para PK compuestas.
# Se podría hacer con query parameters, pero esta es una forma robusta.
@app.route('/work_author/search', methods=['POST'])
def get_single_work_author():
    data = request.get_json()
    work_id = data.get('work_id')
    author_id = data.get('author_id')
    
    if not work_id or not author_id:
        return jsonify({'error': 'work_id y author_id son requeridos para la búsqueda.'}), 400

    conn = get_db_connection()
    relation = conn.execute(
        "SELECT work_id, author_id FROM work_author WHERE work_id = ? AND author_id = ?",
        (work_id, author_id)
    ).fetchone()
    conn.close()

    if relation is None:
        return jsonify({'error': 'Relación no encontrada.'}), 404
    
    return jsonify(dict(relation)), 200

# 4. DELETE (Borrar una relación específica)
@app.route('/work_author', methods=['DELETE'])
def delete_work_author():
    data = request.get_json()
    work_id = data.get('work_id')
    author_id = data.get('author_id')
    
    if not work_id or not author_id:
        return jsonify({'error': 'work_id y author_id son requeridos para borrar.'}), 400

    conn = get_db_connection()
    # Borra la relación por sus dos claves primarias
    cursor = conn.execute(
        "DELETE FROM work_author WHERE work_id = ? AND author_id = ?",
        (work_id, author_id)
    )
    conn.commit()
    
    # Verifica si se eliminó alguna fila
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Relación no encontrada para borrar.'}), 404
    
    conn.close()
    return jsonify({'message': 'Relación work_author eliminada con éxito.'}), 200

if __name__ == '__main__':
    # Ejecuta la aplicación. En Codespaces, el host debe ser '0.0.0.0'
    app.run(host='0.0.0.0', port=8000, debug=True)