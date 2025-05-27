import streamlit as st
import os
import io
import zipfile

st.title("📂 Buscar y descargar archivos PDF con 'entrega'")

# Ingresar la ruta de la carpeta base
carpeta_base = st.text_input("Ruta de la carpeta base", value=".")

if st.button("🔍 Buscar archivos y crear ZIP"):
    if os.path.isdir(carpeta_base):
        archivos_encontrados = []

        # Buscar recursivamente archivos PDF que contengan "entrega"
        for root, dirs, files in os.walk(carpeta_base):
            for file in files:
                if file.lower().endswith(".pdf") and "entrega" in file.lower():
                    ruta_completa = os.path.join(root, file)
                    archivos_encontrados.append(ruta_completa)

        # Verificar si se encontraron archivos
        cantidad = len(archivos_encontrados)
        if cantidad > 0:
            st.success(f"✅ Se encontraron {cantidad} archivo(s) PDF que contienen 'entrega'.")

            # Crear ZIP en memoria
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for ruta in archivos_encontrados:
                    nombre_archivo = os.path.basename(ruta)
                    zipf.write(ruta, arcname=nombre_archivo)  # Usa el nombre original
            zip_buffer.seek(0)

            # Descargar ZIP
            st.download_button(
                label="📦 Descargar todos los archivos en un ZIP",
                data=zip_buffer,
                file_name="archivos_entrega.zip",
                mime="application/zip"
            )
        else:
            st.warning("⚠️ No se encontraron archivos PDF con 'entrega'.")
    else:
        st.error("🚫 La ruta ingresada no es válida.")
