import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="Gestion_de_turnos",
            user="postgres",
            password="GRUPO2",
            port=5435
        )
        return connection
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

