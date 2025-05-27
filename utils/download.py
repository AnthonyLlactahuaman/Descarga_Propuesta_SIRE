import os
import zipfile


def descomprimir_archivo_zip(carpeta, archivo_zip):
    # Verificar si la carpeta no está vacía
    if not os.listdir(carpeta):
        print(f"La carpeta '{carpeta}' está vacía. No hay archivos para procesar.")
        return

    # Construir la ruta completa del archivo .zip
    ruta_zip = os.path.join(carpeta, archivo_zip)

    # Verificar si el archivo especificado existe
    if not os.path.exists(ruta_zip):
        print(f"El archivo '{archivo_zip}' no existe en la carpeta '{carpeta}'.")
        return

    try:
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            # Obtener la lista de nombres de los archivos dentro del .zip
            nombres_archivos_zip = zip_ref.namelist()

            # Extraer todo el contenido del archivo .zip
            zip_ref.extractall(carpeta)

            # Devolver la lista de nombres de los archivos
            return nombres_archivos_zip

    except zipfile.BadZipFile:
        print(f"El archivo '{archivo_zip}' no es un archivo .zip válido.")
    except Exception as e:
        print(f"Error al procesar el archivo '{archivo_zip}': {e}")


def renombrar_archivos(carpeta, zip, txt, periodo, ind):
    ruta_zip = os.path.join(carpeta, zip)
    ruta_txt = os.path.join(carpeta, txt)

    if ind == '0800':
        # Obtener las rutas de los nuevos nombres
        nueva_ruta_zip = os.path.join(os.path.dirname(ruta_zip), f"{zip[:11]}-{periodo}-{ind}.zip")
        nueva_ruta_txt = os.path.join(os.path.dirname(ruta_txt), f"{zip[:11]}-{periodo}-{ind}.txt")
    else:
        nueva_ruta_zip = os.path.join(os.path.dirname(ruta_zip), f"{zip[2:13]}-{periodo}-{ind}.zip")
        nueva_ruta_txt = os.path.join(os.path.dirname(ruta_txt), f"{zip[2:13]}-{periodo}-{ind}.txt")

    try:
        # Renombrar los archivos
        os.rename(ruta_zip, nueva_ruta_zip)
        os.rename(ruta_txt, nueva_ruta_txt)
    except Exception as e:
        print(f"Error al renombrar los archivos: {e}")

    print("Proceso de extracción completado.")
