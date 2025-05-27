import requests
from urllib3.exceptions import InsecureRequestWarning
import time
import sys


class api:
    def __init__(self, periodo, clientId, clientSecret, userId, password, download):
        self.__periodo = periodo
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__userId = userId
        self.__password = password
        self.__download = download
        self.__token = None
        self.__ticket = None
        self.__nArchivo = None

    # Función principal para manejar reintentos
    def attempt_request(self, method, url, headers=None, data=None, max_retries=3, indice=str):
        for intento in range(max_retries):
            try:
                response = self.send_request(method, url, headers, data)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code in [400, 401, 422, 500]:
                    self.handle_error_response(response, indice)
                else:
                    print(f"Código inesperado: {response.status_code}")
            except Exception as ex:
                print(f"Error en la solicitud: {ex}")

            time.sleep(1)

        return None

    # Enviar solicitudes HTTP
    def send_request(self, method, url, headers=None, data=None):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if method.lower() == "post":
            return requests.post(url, headers=headers, data=data, verify=False)
        elif method.lower() == "get":
            return requests.get(url, headers=headers, verify=False)
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")

    # Manejar respuestas de error específicas
    def handle_error_response(self, response, indice):
        if indice == 'get_ticket':
            msg_error = 'Generar Ticket'
            if response.status_code == 500:
                resp = response.json()
                self._show_message_error(msg_error, resp["msg"])
            elif response.status_code == 422:
                resp = response.json()
                self._show_message_error(msg_error, resp["errors"][0]["msg"])
        if indice == 'get_token':
            msg_error = 'Generar Token'
            if response.status_code == 400:
                resp = response.json()
                self._show_message_error(msg_error, resp["error_description"])

    # Función para obtener el token
    def generar_token(self):
        url = f"https://api-seguridad.sunat.gob.pe/v1/clientessol/{self.__clientId}/oauth2/token/"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "scope": "https://api-sire.sunat.gob.pe",
            "client_id": self.__clientId,
            "client_secret": self.__clientSecret,
            "username": self.__userId,
            "password": self.__password
        }

        response = self.attempt_request("post", url, headers, data, 3, 'get_token')
        if response and "access_token" in response:
            self.__token = response["access_token"]
            print("El token se ah generado y guardado con éxito.")
            sys.stdout.flush()
            return True
        return False

    # Obtener encabezados comunes
    def get_headers(self):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                   "Authorization": f"Bearer {self.__token}"}
        return headers

    # Consultar estado del ticket
    def estado_ticket(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        url = (f"https://api-sire.sunat.gob.pe/v1/contribuyente/migeigv/libros/rvierce/"
               f"gestionprocesosmasivos/web/masivo/consultaestadotickets?"
               f"perIni={self.__periodo}&perFin={self.__periodo}&page=1&perPage=20&numTicket={self.__ticket}")
        headers = self.get_headers()

        msg_error = 'Consultar Ticket'

        try:
            response = self.send_request("get", url, headers, None)
            if response.status_code == 200:
                return response.json().get("registros", [])
            elif response.status_code == 500:
                resp = response.json()
                self._show_message_error(msg_error, resp["msg"])

            elif response.status_code == 422:
                resp = response.json()
                cod = resp["errors"][0]["cod"]
                msg = resp["errors"][0]["msg"]
                self._show_message_error(msg_error, f"{cod}, {msg}")
            else:
                print(f"Error al consultar el estado del ticket. Código: {response.status_code}")
                return None  # Devuelve None para indicar que hubo un error
        except Exception as ex:
            print(f"Error en la solicitud de estado: {ex}")
            return None  # Devuelve None para indicar que hubo un error

    def set_ticket(self, ticket):
        self.__ticket = ticket

    def get_ticket(self):
        return self.__ticket

    def get_periodo(self):
        return self.__periodo

    def get_download(self):
        return self.__download

    def set_nArchivo(self, Archivo):
        self.__nArchivo = Archivo

    def get_nArchivo(self):
        return self.__nArchivo

    # Guardar valores en archivo
    def _save_to_file(self, key, value):
        try:
            with open('.env', 'r') as env_file:
                lines = env_file.readlines()

            # Buscar y actualizar la clave específica
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    updated = True
                    break

            if not updated:
                lines.append(f"{key}={value}\n")

            with open('.env', 'w') as env_file:
                env_file.writelines(lines)
        except Exception as ex:
            print(f"Error al guardar {key}: {ex}")

    def _show_message_error(self, tipo_error, mensaje):
        print("FALLÓ al " + tipo_error + ". Error: " + mensaje + "!")

    @staticmethod
    def _mostrar_progreso(actual, total, barra_longitud=40):
        progreso = int(barra_longitud * actual / total)
        barra = f"[{'#' * progreso}{'.' * (barra_longitud - progreso)}]"
        calculo = total/(total-actual)
        sys.stdout.write(f"\r{barra} {calculo:.2f}/100 %")
        sys.stdout.flush()
