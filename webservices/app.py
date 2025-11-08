import requests
import json

# URL base del servicio Flask
BASE_URL = "http://localhost:8000/author"

# ----------------------------------------------------
# A. GET: Obtener todos los autores
# ----------------------------------------------------
def get_all_authors():
    print("Fetching all authors...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            print("\nList of authors:")
            print(json.dumps(data, indent=4))
        else:
            print(f"\nFailed to fetch authors. Status code: {response.status_code}")
            print(f"Server response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nConnection error. Ensure the Flask service is running at http://localhost:8000")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# ----------------------------------------------------
# B. POST: Crear un nuevo autor
# ----------------------------------------------------
def create_author(full_name):
    print("\nCreating a new author...")
    try:
        payload = {
            "full_name": full_name
        }
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print("\nAuthor created successfully:")
            print(response.json())
        else:
            print(f"\nFailed to create author. Status code: {response.status_code}")
            print(f"Server response: {response.text}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# ----------------------------------------------------
# C. PUT: Actualizar un autor existente
# ----------------------------------------------------
def update_author(author_id, full_name):
    print(f"\nUpdating author with ID {author_id}...")
    try:
        payload = {
            "full_name": full_name
        }
        url = f"{BASE_URL}/{author_id}"
        response = requests.put(url, json=payload)
        if response.status_code == 200:
            print("\nAuthor updated successfully:")
            print(response.json())
        else:
            print(f"\nFailed to update author. Status code: {response.status_code}")
            print(f"Server response: {response.text}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# ----------------------------------------------------
# D. DELETE: Eliminar un autor
# ----------------------------------------------------
def delete_author(author_id):
    print(f"\nDeleting author with ID {author_id}...")
    try:
        url = f"{BASE_URL}/{author_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            print("\nAuthor deleted successfully:")
            print(response.json())
        else:
            print(f"\nFailed to delete author. Status code: {response.status_code}")
            print(f"Server response: {response.text}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == '__main__':
    # Uso de ejemplo de las operaciones CRUD

    # 1. Obtener todos los autores
    get_all_authors()

    # 2. Crear un nuevo autor
    create_author("MISAEL LOPEZ SANCHEZ")

    # 3. Actualizar un autor existente (ejemplo con ID 1)
    update_author(1, "Gabriel García Márquez")

    # 4. Eliminar un autor (ejemplo con ID 1)
    delete_author(2)

    # 5. Obtener todos los autores nuevamente para verificar los cambios
    get_all_authors()
