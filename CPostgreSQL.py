import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def f_conectar():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost").strip(),
        port=os.environ.get("DB_PORT", "5432").strip(),
        database=os.environ.get("DB_NAME", "taller").strip(),
        user=os.environ.get("DB_USER", "postgres").strip(),
        password=os.environ.get("DB_PASSWORD", "").strip(),
        sslmode=os.environ.get("DB_SSLMODE", "prefer").strip()
    )

def f_agregar_cliente(nombre, ap_paterno, ap_materno, correo, telefono):
    conexion = f_conectar()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, correo, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (nombre, ap_paterno, ap_materno, correo, telefono))
    conexion.commit()
    cursor.close()
    conexion.close()

def f_listar_clientes():
    conexion = f_conectar()
    cursor = conexion.cursor()
    sql = "SELECT id_cliente, nombre, apellido_paterno, apellido_materno, correo, telefono, fecha_registro FROM clientes ORDER BY id_cliente DESC"
    cursor.execute(sql)
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return registros