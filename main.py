import time
import os
from utils.validation import limpiar_consola
from utils.download import descomprimir_archivo_zip, renombrar_archivos
from colorama import Fore, Style, init
from apis.compras import ApiCompras
from apis.ventas import ApiVentas
from config import CLIENT_ID, CLIENT_SECRET, USER_ID, PASSWORD, DOWNLOAD

# Inicializa colorama
init(autoreset=True)


def mostrar_menu():
    # Colores personalizados
    cuadro_color = Fore.BLUE + Style.BRIGHT  # Azul para el cuadro
    texto_color = Fore.MAGENTA + Style.BRIGHT  # Morado claro para el texto

    # Cabecera
    print(cuadro_color + "\n╔════════════════════════════════════════════════════╗")
    print(cuadro_color + "║" + texto_color + "                KPMG PERU - POWER TAX               " + cuadro_color + "║")
    print(cuadro_color + "╠════════════════════════════════════════════════════╣")
    print(cuadro_color + "║" + texto_color + "  MENÚ PRINCIPAL                                    " + cuadro_color + "║")
    print(cuadro_color + "╠════════════════════════════════════════════════════╣")
    # Opciones del menú
    print(cuadro_color + "║" + texto_color + "  1. Descargar Ventas                               " + cuadro_color + "║")
    print(cuadro_color + "║" + texto_color + "  2. Descargar Compras                              " + cuadro_color + "║")
    print(cuadro_color + "║" + texto_color + "  3. Salir                                          " + cuadro_color + "║")
    # Pie del menú
    print(cuadro_color + "╚════════════════════════════════════════════════════╝")


def obtener_seleccion():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\nSeleccione una opción: "))
            if 1 <= opcion <= 3:
                return opcion
            else:
                print("Por favor, elija una opción válida (1-3).")
                time.sleep(1)
                limpiar_consola()
        except ValueError:
            print("Entrada inválida. Introduzca un número entre 1 y 3.")
            time.sleep(1)
            limpiar_consola()


def main():
    # Crear la carpeta si no existe
    if not os.path.exists(DOWNLOAD):
        os.makedirs(DOWNLOAD)
        return

    flag = False

    while True:
        opcion = obtener_seleccion()

        if opcion == 3:  # Salir
            break

        # Limpiar el menu
        limpiar_consola()
        # Solicitar datos necesarios para la API seleccionada
        periodo = input("\nPeriodo a descargar (Año\Periodo): ").strip()

        # Manejar la opción seleccionada
        if opcion == 1:
            Api = ApiVentas(periodo, CLIENT_ID, CLIENT_SECRET, USER_ID, PASSWORD, DOWNLOAD)
            flag = Api.Ejecucion_ApiVentas()
            ind = '14000'
        elif opcion == 2:
            Api = ApiCompras(periodo, CLIENT_ID, CLIENT_SECRET, USER_ID, PASSWORD, DOWNLOAD)
            flag = Api.Ejecucion_ApiCompras()
            ind = '0800'

        if flag:
            print("\nDESCOMPRIMIENDO ARCHIVO")
            time.sleep(1.5)
            nombre = Api.get_nomArchivo()
            list = descomprimir_archivo_zip(DOWNLOAD, nombre)
            renombrar_archivos(DOWNLOAD, nombre, list[0], periodo, ind)
        break


if __name__ == "__main__":
    main()
