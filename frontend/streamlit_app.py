import streamlit as st
import requests
import cv2
import pytesseract
from PIL import Image
import numpy as np

BASE_URL = "http://localhost:5000"

st.title("Sistema de Automatización y Clasificación de Libros")

# CU-1: Registrar libro nuevo
st.header("Registrar libro nuevo")
with st.form("register_book"):
    title = st.text_input("Título")
    author = st.text_input("Autor")
    theme = st.text_input("Tema")
    year = st.number_input("Año", min_value=1000, max_value=9999, step=1)
    publisher = st.text_input("Editorial")
    isbn = st.text_input("ISBN")
    cover_url = st.text_input("URL de la portada")
    submitted = st.form_submit_button("Registrar")

    if submitted:
        response = requests.post(f"{BASE_URL}/register_book", json={
            "title": title,
            "author": author,
            "theme": theme,
            "year": year,
            "publisher": publisher,
            "isbn": isbn,
            "cover_url": cover_url
        })
        if response.status_code == 201:
            st.success("Libro registrado exitosamente")
        else:
            st.error("Error al registrar el libro")

# CU-1: Registrar libro nuevo con OCR
st.header("Registrar libro nuevo con OCR")
with st.form("register_book_ocr"):
    uploaded_file = st.file_uploader("Sube la imagen de la portada del libro", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Procesar y Registrar")

    if submitted and uploaded_file is not None:
        # Leer la imagen subida
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Procesar la imagen con OpenCV y Tesseract
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="spa")

        # Extraer campos clave (título, autor, etc.) usando reglas simples
        st.write("Texto extraído:")
        st.text(text)

        # Aquí puedes implementar reglas para extraer título, autor, etc.
        title = st.text_input("Título detectado", value="")
        author = st.text_input("Autor detectado", value="")
        theme = st.text_input("Tema detectado", value="")
        year = st.number_input("Año detectado", min_value=1000, max_value=9999, step=1)
        publisher = st.text_input("Editorial detectada", value="")
        isbn = st.text_input("ISBN detectado", value="")

        if st.button("Registrar libro"):
            response = requests.post(f"{BASE_URL}/register_book", json={
                "title": title,
                "author": author,
                "theme": theme,
                "year": year,
                "publisher": publisher,
                "isbn": isbn,
                "cover_url": ""
            })
            if response.status_code == 201:
                st.success("Libro registrado exitosamente")
            else:
                st.error("Error al registrar el libro")

# CU-2: Verificar duplicados
st.header("Verificar duplicados")
with st.form("check_duplicates"):
    title = st.text_input("Título del libro")
    author = st.text_input("Autor del libro")
    submitted = st.form_submit_button("Verificar")

    if submitted:
        response = requests.post(f"{BASE_URL}/check_duplicates", json={
            "title": title,
            "author": author
        })
        if response.status_code == 200:
            data = response.json()
            if "duplicates" in data:
                st.warning("Se encontraron duplicados:")
                st.json(data["duplicates"])
            else:
                st.success("No se encontraron duplicados")
        else:
            st.error("Error al verificar duplicados")

# CU-3: Consultar catálogo
st.header("Consultar catálogo")
if st.button("Mostrar catálogo"):
    response = requests.get(f"{BASE_URL}/catalog")
    if response.status_code == 200:
        catalog = response.json()["catalog"]
        st.write("Catálogo de libros:")
        st.json(catalog)
    else:
        st.error("Error al consultar el catálogo")

# CU-4: Editar metadatos manualmente
st.header("Editar metadatos")
with st.form("edit_metadata"):
    book_id = st.number_input("ID del libro", min_value=1, step=1)
    title = st.text_input("Nuevo título")
    author = st.text_input("Nuevo autor")
    theme = st.text_input("Nuevo tema")
    submitted = st.form_submit_button("Actualizar")

    if submitted:
        response = requests.put(f"{BASE_URL}/edit_metadata/{book_id}", json={
            "title": title,
            "author": author,
            "theme": theme
        })
        if response.status_code == 200:
            st.success("Metadatos actualizados exitosamente")
        else:
            st.error("Error al actualizar metadatos")
