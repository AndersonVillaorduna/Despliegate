import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def conectar():
    try:
        urldatabase = os.getenv('urldatabase')
        if not urldatabase:
            raise ValueError("La variable de entorno 'urldatabase' no está configurada.")

        conexion = psycopg2.connect(urldatabase)
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos PostgreSQL: {e}")
        return None
