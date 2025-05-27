import os
from dotenv import load_dotenv

# Cargar las variables desde .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_ID = os.getenv('USER_ID')
PASSWORD = os.getenv('PASSWORD')
TICKET = os.getenv('TICKET', '')  # Permitir valores vacíos

# Rutas
CARPETA = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD = os.path.join(CARPETA, 'data')

# Validación de claves críticas
if not CLIENT_ID or not CLIENT_SECRET or not USER_ID or not PASSWORD:
    raise ValueError(
        "Faltan claves críticas en el archivo .env. "
        "Verifica que CLIENT_ID, CLIENT_SECRET, USER_ID y PASSWORD estén completos."
    )
