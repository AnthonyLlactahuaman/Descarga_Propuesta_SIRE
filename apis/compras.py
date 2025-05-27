import requests
from urllib3.exceptions import InsecureRequestWarning
import time
import os
import sys
from apis.api import api


class ApiCompras(api):
    # Función para generar ticket
    def generar_ticket(self, periodo):
        url = (f"https://api-sire.sunat.gob.pe/v1/contribuyente/migeigv/libros/rce/propuesta/web/propuesta/"
               f"{periodo}/exportacioncomprobantepropuesta?codTipoArchivo=0&codOrigenEnvio=1")
        headers = super().get_headers()

        response = super().attempt_request("get", url, headers, None, 3, 'get_tikect')
        if response and "numTicket" in response:
            ticket = response["numTicket"]
            super().set_ticket(ticket)
            super()._save_to_file("TICKET", ticket)
            print("Ticket generado y guardado con éxito.")
            sys.stdout.flush()
            return True
        return False

    def download_archivo(self, nomArchivo, codTipo):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        file_path = os.path.join(super().get_download(), nomArchivo)

        try:
            header = super().get_headers()
            url = (f"https://api-sire.sunat.gob.pe/v1/contribuyente/migeigv/libros/rvierce/"
                   f"gestionprocesosmasivos/web/masivo/archivoreporte?"
                   f"nomArchivoReporte={nomArchivo}&codTipoArchivoReporte={codTipo}&"
                   f"perTributario={super().get_periodo()}&codProceso=10&numTicket={super().get_ticket()}")

            msg_error = 'Descargar Archivo'

            response = requests.get(url, headers=header, verify=False)
            if response.status_code == 200:
                with open(file_path, 'wb') as archivo_local:
                    archivo_local.write(response.content)
                print("Archivo descargado exitosamente.")
            elif response.status_code == 500:
                resp = response.json()
                super()._show_message_error(msg_error, resp["msg"])
            elif response.status_code == 422:
                resp = response.json()
                super()._show_message_error(msg_error, resp["errors"][0]["msg"])
            else:
                print(f"Error al descargar archivo: {response.status_code}")
        except Exception as ex:
            print(f"Error en la descarga del archivo: {ex}")

    def esperar_estado_terminado(self):
        max_espera = 10  # Máximo de 10 minutos
        tiempo_por_iteracion = 30  # Un minuto por iteración
        iteraciones = max_espera * 60 // tiempo_por_iteracion
        time.sleep(2)

        for i in range(iteraciones):
            estados = super().estado_ticket()

            if estados is None:
                print("Error crítico al consultar el estado del ticket. Finalizando el monitoreo.")
                return None

            for estado in estados:
                if estado["desEstadoProceso"] == "Terminado" and estado.get("archivoReporte"):
                    print("\nProceso finalizado. Preparando para descargar archivo(s).")
                    sys.stdout.flush()
                    # Identificar si es un solo archivo o múltiples
                    if len(estado["archivoReporte"]) == 1:
                        return estado["archivoReporte"][0]  # Retorna el primer archivo si es único
                    return estado["archivoReporte"]  # Retorna toda la lista si son múltiples archivos

            # Barra de progreso
            api._mostrar_progreso(i + 1, iteraciones)
            time.sleep(tiempo_por_iteracion)

        print("\nTiempo máximo de espera alcanzado. No se completó el proceso.")
        return None

    def descargar_archivo(self, archivo):
        if archivo:
            nomArchivo = archivo.get("nomArchivoReporte")
            codTipo = archivo.get("codTipoAchivoReporte")
            if nomArchivo and codTipo:
                self.download_archivo(nomArchivo, codTipo)
                time.sleep(5)
                super().set_nArchivo(str(nomArchivo))
            else:
                print("El archivo no contiene la información necesaria para la descarga.")
        else:
            print("No se recibió información del archivo para descargar.")

    def descargar_archivos_multiples(self, archivos):
        nomUltArchivo = None
        for archivo in archivos:
            nomArchivo = archivo.get("nomArchivoReporte")
            codTipo = archivo.get("codTipoAchivoReporte")
            if nomArchivo and codTipo:
                print(f"Descargando archivo: {nomArchivo}")
                sys.stdout.flush()
                self.download_archivo(nomArchivo, codTipo)
                time.sleep(5)  # Pausa opcional entre descargas
            else:
                print("El archivo no contiene la información necesaria para la descarga.")
                sys.stdout.flush()
            nomUltArchivo = nomArchivo
        super().set_nArchivo(nomUltArchivo)

    def get_nomArchivo(self):
        return super().get_nArchivo()

    def Ejecucion_ApiCompras(self):
        print('\nGENERANDO TOKEN...')
        sys.stdout.flush()
        if not super().generar_token():
            print("Error al generar el token. No se puede continuar.")
            return False

        print('\nGENERANDO TICKET...')
        sys.stdout.flush()
        if not self.generar_ticket(super().get_periodo()):
            print("Error al generar el ticket. No se puede continuar.")
            return False

        print("\nESPERANDO QUE EL ARCHIVO ESTE LISTO PARA DESCARGAR...")
        sys.stdout.flush()
        archivo_o_archivos = self.esperar_estado_terminado()

        if archivo_o_archivos is None:
            print("No se pudo completar el proceso. Finalizando.")
            return False

        print("\nDESCARGANDO ARCHIVO(S)...")
        sys.stdout.flush()
        if isinstance(archivo_o_archivos, dict):  # Un solo archivo
            self.descargar_archivo(archivo_o_archivos)
            return True
        elif isinstance(archivo_o_archivos, list):  # Múltiples archivos
            self.descargar_archivos_multiples(archivo_o_archivos)
            return True
