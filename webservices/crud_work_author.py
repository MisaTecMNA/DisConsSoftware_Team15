#*************************************************************************
#
#             CONSUMIR SERVICIOS CRUD DESDE PYCHARM
# TABLA: WORK_AUTHOR
#*************************************************************************

# Librerias
import requests
import json

# URL DE CODESPACE EN PUERTO 8000
BASE_URL = "https://neglected-spooky-specter-7vv65xg7w7xv2pvqv-8000.app.github.dev"


#*************************************************************************
#
#                         FUNCIONES CRUD
#
#*************************************************************************

#*************************************************************************
#                         OBTENER TODAS LAS RELACIONES
#*************************************************************************

def get_all_relations():
    """Consume el servicio READ ALL (GET /work_author)"""
    url = f"{BASE_URL}/work_author"
    print(f"\n******************************************")
    print(f"\n*     Probando GET (Listar Todo)         *")
    print(f"\n******************************************")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx
        print(f"Estatus del servicio: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al listar relaciones: {e}")
        return None

#*************************************************************************
#                         CREAR UNA RELACIÓN
#*************************************************************************

def create_relation(work_id, author_id):
    """Consume el servicio CREATE (POST /work_author)"""
    url = f"{BASE_URL}/work_author"
    data = {"work_id": work_id, "author_id": author_id}
    print(f"\n**********************************************************")
    print(f"\n* Probando POST (Crear Relación: {work_id}, {author_id}) *")
    print(f"\n**********************************************************")
    try:
        response = requests.post(url, json=data)
        print(f"Estatus del servicio: {response.status_code}")
        # Intenta imprimir el mensaje JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al crear relación: {e}")
        return None

#*************************************************************************
#                         BUSCAR UNA RELACIÓN
#*************************************************************************

def search_relation(work_id, author_id):
    """Consume el servicio READ ONE (POST /work_author/search)"""
    url = f"{BASE_URL}/work_author/search"
    data = {"work_id": work_id, "author_id": author_id}
    print(f"\n******************************************************************")
    print(f"\n*   Probando SEARCH (Buscar Relación: {work_id}, {author_id})    *")
    print(f"\n******************************************************************")
    try:
        response = requests.post(url, json=data)
        print(f"Estatus del servicio: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar relación: {e}")
        return None

#*************************************************************************
#                         BORRAR UNA RELACIÓN
#*************************************************************************
def delete_relation(work_id, author_id):
    """Consume el servicio DELETE (DELETE /work_author)"""
    url = f"{BASE_URL}/work_author"
    data = {"work_id": work_id, "author_id": author_id}
    print(f"\n*******************************************************************")
    print(f"\n*   Probando DELETE (Eliminar Relación: {work_id}, {author_id})   *")
    print(f"\n*******************************************************************")
    try:
        response = requests.delete(url, json=data)
        print(f"Estatus del servicio: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar relación: {e}")
        return None


#*************************************************************************
#                         MAIN
#*************************************************************************

if __name__ == "__main__":
    # 1. PRUEBA DE CREACIÓN (POST)
    # Asumimos que los IDs 1 y 2 existen en work y author
    print("\n##### INICIANDO EJECUCIÓN DE PRUEBAS CRUD PARA TABLA WORK_AUTHOR #####")

    # Intenta crear una nueva relación (1, 2)
    create_result = create_relation(6, 6)
    print("Resultado POST:", create_result)

    # 2. PRUEBA DE LECTURA (GET ALL)
    relations = get_all_relations()
    print("Resultado GET ALL:", relations)

    # 3. PRUEBA DE BÚSQUEDA (SEARCH POST)
    search_result = search_relation(6, 6)
    print("Resultado SEARCH:", search_result)

    # 4. PRUEBA DE ELIMINACIÓN (DELETE)
    delete_result = delete_relation(6, 6)
    print("Resultado DELETE:", delete_result)

    # 5. VERIFICACIÓN FINAL (GET ALL)
    relations_after_delete = get_all_relations()
    print("Resultado GET ALL (Después de DELETE):", relations_after_delete)