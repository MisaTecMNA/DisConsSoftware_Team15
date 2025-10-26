import requests
import json
import time

# URL base de tu API de Codespace (asegúrate de que esté corriendo en el puerto 8000)
BASE_URL = "https://squalid-cemetery-x557p4jg655jhppp7-8000.app.github.dev/editions"


# --- 1. CREATE (POST) ---
def create_edition():
    """Crea un nuevo registro de edición."""
    print("\n--- 1. CREAR una nueva Edición (POST) ---")

    # Asegúrate de usar un ISBN único cada vez que pruebes la creación.
    # Usamos la marca de tiempo para generar un ISBN único
    unique_isbn = f"978-PYC-{int(time.time())}"

    new_edition_data = {
        "work_id": 1,
        "year": 2025,
        "publisher": "PyCharm Publisher S.L.",
        "isbn": unique_isbn,
        "cover_url": "http://pycharm.dev/cover.jpg"
    }

    try:
        response = requests.post(BASE_URL, json=new_edition_data)
        response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx

        data = response.json()
        print(f"Estado: {response.status_code}")
        print(f"Respuesta: {data}")

        # Devolvemos el ID creado para usarlo en otras operaciones
        return data.get('id')

    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err}")
        print(f"Cuerpo del error: {response.json()}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error de conexión: {err}")
        return None


# --- 2. READ (GET) ---
def get_all_editions():
    """Obtiene y muestra todas las ediciones."""
    print("\n--- 2A. OBTENER TODAS las Ediciones (GET) ---")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        editions = response.json()
        print(f"Estado: {response.status_code}")
        print(f"Ediciones encontradas ({len(editions)}):")
        # Imprimir de forma más legible
        print(json.dumps(editions, indent=2))

    except requests.exceptions.RequestException as err:
        print(f"Error al obtener todas: {err}")


def get_edition_by_id(edition_id):
    """Obtiene y muestra una edición por su ID."""
    print(f"\n--- 2B. OBTENER Edición con ID {edition_id} (GET) ---")
    url = f"{BASE_URL}/{edition_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        edition = response.json()
        print(f"Estado: {response.status_code}")
        print(f"Edición: {edition}")

    except requests.exceptions.HTTPError as err:
        print(f"Edición no encontrada (o error): {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error de conexión: {err}")


# --- 3. UPDATE (PUT) ---
def update_edition(edition_id):
    """Actualiza campos específicos de una edición."""
    print(f"\n--- 3. ACTUALIZAR Edición con ID {edition_id} (PUT) ---")

    update_data = {
        "publisher": "PyCharm Updated Corp.",
        "year": 2026  # Actualizamos el año
    }

    url = f"{BASE_URL}/{edition_id}"
    try:
        response = requests.put(url, json=update_data)
        response.raise_for_status()

        print(f"Estado: {response.status_code}")
        print(f"Respuesta: {response.json()}")

    except requests.exceptions.HTTPError as err:
        print(f"Error al actualizar: {err}")
        print(f"Cuerpo del error: {response.json()}")
    except requests.exceptions.RequestException as err:
        print(f"Error de conexión: {err}")


# --- 4. DELETE (DELETE) ---
def delete_edition(edition_id):
    """Elimina una edición por su ID."""
    print(f"\n--- 4. ELIMINAR Edición con ID {edition_id} (DELETE) ---")
    url = f"{BASE_URL}/{edition_id}"
    try:
        response = requests.delete(url)
        response.raise_for_status()

        print(f"Estado: {response.status_code}")
        print(f"Respuesta: {response.json()}")

    except requests.exceptions.HTTPError as err:
        print(f"Error al eliminar: {err}")
        print(f"Cuerpo del error: {response.json()}")
    except requests.exceptions.RequestException as err:
        print(f"Error de conexión: {err}")


# --- Ejecución de las Pruebas ---
if __name__ == '__main__':
    # 1. Instala la librería 'requests' si no la tienes
    #    En PyCharm: File -> Settings -> Project -> Python Interpreter -> (+) -> busca 'requests' -> Install Package
    #    O en la terminal de PyCharm: pip install requests

    # 2. Crea la nueva edición y captura su ID para usarlo en las siguientes operaciones
    created_id = create_edition()

    if created_id is not None:
        # Espera un momento para asegurar la escritura en DB si es necesario
        time.sleep(0.5)

        # 3. Leer la edición recién creada
        get_edition_by_id(created_id)

        # 4. Actualizar la edición
        update_edition(created_id)

        # 5. Leer de nuevo para verificar la actualización
        get_edition_by_id(created_id)

        # 6. Leer todas las ediciones
        get_all_editions()

        # 7. Eliminar la edición
        delete_edition(created_id)

        # 8. Intentar leer de nuevo (debe fallar con 404)
        get_edition_by_id(created_id)