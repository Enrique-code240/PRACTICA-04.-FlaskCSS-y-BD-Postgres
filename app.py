import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Carga segura de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def f_conectar():
    return psycopg2.connect(
        host=(os.environ.get("DB_HOST") or "").strip(),
        port=int((os.environ.get("DB_PORT") or "14117").strip()),
        database=(os.environ.get("DB_NAME") or "taller").strip(),
        user=(os.environ.get("DB_USER") or "avnadmin").strip(),
        password=(os.environ.get("DB_PASSWORD") or "").strip(),
        sslmode=(os.environ.get("DB_SSLMODE") or "require").strip()
    )

def f_agregar_cliente(nombre, ap_paterno, ap_materno, correo, telefono):
    conexion = None
    try:
        conexion = f_conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, correo, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, ap_paterno, ap_materno, correo, telefono))
        conexion.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error al agregar cliente: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()

def f_listar_clientes():
    conexion = None
    registros = []
    try:
        conexion = f_conectar()
        # RealDictCursor permite acceder a los datos en HTML como cliente.nombre o cliente['nombre']
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        sql = "SELECT id_cliente, nombre, apellido_paterno, apellido_materno, correo, telefono, fecha_registro FROM clientes ORDER BY id_cliente DESC"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(f"Error al listar clientes: {e}")
    finally:
        if conexion:
            conexion.close()
    return registros
