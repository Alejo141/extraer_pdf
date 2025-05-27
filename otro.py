import streamlit as st
import os
import io
import zipfile

st.title("📂 Buscar y descargar archivos PDF con 'entrega'")

# Entrada para la ruta de la carpeta
carpeta_base = st.text_input("📁 Ingresa la ruta de la carpeta base", value=".")

# Mostrar ayuda
st.caption("Ejemplo de ruta válida en Windows: `C:\\Users\\TuUsuario\\Documents\\PDFs`")

if st.button("🔍 Buscar archivos y crear ZIP"):
    if carpeta_base.strip() == "":
        st.error("❌ No ingresaste ninguna ruta.")
    elif not os.path.exists(carpeta_base):
        st.error("🚫 La ruta ingresada no existe.")
    elif not os.path.isdir(carpeta_base):
        st.error("⚠️ La ruta ingresada no es una carpeta.")
    else:
        archivos_encontrados = []

        for root, dirs, files in os.walk(carpeta_base):
            for file in files:
                if file.lower().endswith(".pdf") and "entrega" in file.lower():
                    archivos_encontrados.append(os.path.join(root, file))

        cantidad = len(archivos_encontrados)
        if cantidad > 0:
            st.success(f"✅ Se encontraron {cantidad} archivo(s) PDF que contienen 'entrega'.")

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for ruta in archivos_encontrados:
                    nombre_archivo = os.path.basename(ruta)
                    zipf.write(ruta, arcname=nombre_archivo)
            zip_buffer.seek(0)

            st.download_button(
                label="📦 Descargar todos los archivos en un ZIP",
                data=zip_buffer,
                file_name="archivos_entrega.zip",
                mime="application/zip"
            )
        else:
            st.warning("⚠️ No se encontraron archivos PDF con 'entrega' en el nombre.")
