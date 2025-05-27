# Descarga de Propuesta SIRE

Este proyecto descarga la propuesta SIRE del período que se indique.

---

## Configuración

Para usar el proyecto, debes crear un archivo `.env` en la carpeta raíz con la siguiente estructura:

```

CLIENT_ID=
CLIENT_SECRET=
USER_ID=
PASSWORD=
TICKET=

```

- Los valores de `CLIENT_ID`, `CLIENT_SECRET` y `USER_ID` deben completarse con las credenciales que se generan a través del portal SUNAT.
- El campo `TICKET` debe permanecer vacío.

---

## Uso

1. Crear y configurar el archivo `.env` con las credenciales mencionadas.

2. Ejecutar el script indicando el período deseado para descargar la propuesta SIRE correspondiente.

---

## Estructura de carpetas

```

/ (carpeta raíz)
\|-- .env
\|-- apis/
\|-- utils/
\|-- config.py
\|-- main.py
\|-- README.md

```

---

## Notas

- Asegúrate de que las credenciales sean válidas y estén actualizadas.
- El campo `TICKET` se utilizará durante la ejecución del script, por lo que debe estar vacío inicialmente.

---

Si tienes dudas o sugerencias, no dudes en abrir un issue o contactarme.
```
