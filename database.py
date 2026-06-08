# Importamos el módulo nativo de Python para manejar bases de datos SQL.
import sqlite3

def inicializar_base_de_datos():
    # Usamos un bloque try (intentar) para capturar cualquier falla de hardware o permisos
    try:
        conexion = sqlite3.connect("castlab.db")
        cursor = conexion.cursor()

        # Activar el soporte de Claves Foráneas en SQLite (por defecto viene apagado)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. TABLA PACIENTES
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            sexo TEXT NOT NULL
        )
        """)

        # 2. TABLA ÓRDENES
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes (
            id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (id_paciente) REFERENCES pacientes (id_paciente) ON DELETE CASCADE
        )
        """)

        # 3. TABLA RESULTADOS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id_resultado INTEGER PRIMARY KEY AUTOINCREMENT,
            id_orden INTEGER NOT NULL,
            examen_nombre TEXT NOT NULL,
            parametro TEXT NOT NULL,
            valor_resultado TEXT,
            unidad TEXT,
            FOREIGN KEY (id_orden) REFERENCES ordenes (id_orden) ON DELETE CASCADE
        )
        """)

        conexion.commit()
        print("¡Arquitectura de CastLab blindada e inicializada con éxito!")

    except sqlite3.Error as error:
        # Si algo falla, el programa no muere; viene aquí y te explica detalladamente qué pasó
        print(f"ERROR CRÍTICO: No se pudo configurar la base de datos debido a: {error}")
    
    finally:
        # El bloque 'finally' se ejecuta SIEMPRE, haya habido error o no, para asegurar el cierre seguro
        if conexion:
            conexion.close()

if __name__ == "__main__":
    inicializar_base_de_datos()