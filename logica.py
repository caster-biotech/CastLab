# Importamos la librería para conectar con el archivo .db
import sqlite3
# Importamos el formato de fecha para registrar cuándo se crean las órdenes
from datetime import datetime

def registrar_paciente(cedula, nombre, apellido, edad, sexo):
    """
    Esta función recibe los datos del paciente e intenta guardarlos
    en la tabla 'pacientes' de nuestro archivo castlab.db
    """
    try:
        # 1. Conectamos al archivo
        conexion = sqlite3.connect("castlab.db")
        # 2. Creamos nuestro "dedo lector/escritor"
        dedo_lector = conexion.cursor()
        
        # 3. Preparamos la orden SQL para insertar datos.
        # Usamos los signos de interrogación '?' por seguridad (evita que hackeen la base de datos)
        sql = """
        INSERT INTO pacientes (cedula, nombre, apellido, edad, sexo)
        VALUES (?, ?, ?, ?, ?)
        """
        
        # 4. Le decimos al dedo que ejecute la orden inyectando los datos reales
        dedo_lector.execute(sql, (cedula, nombre, apellido, edad, sexo))
        
        # 5. Guardamos los cambios en el disco duro de forma permanente
        conexion.commit()
        print(f"   [ÉXITO] Paciente {nombre} {apellido} registrado correctamente.")
        
    except sqlite3.IntegrityError:
        # Este error específico salta si intentas registrar una cédula que YA existe
        print(f"   [ADVERTENCIA] La cédula {cedula} ya está registrada en el sistema.")
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo registrar en la base de datos: {e}")
    finally:
        # Cerramos la conexión pase lo que p ase
        conexion.close()

# Bloque de prueba inmediata
if __name__ == "__main__":
    print("--- PROBANDO REGISTRO DE PACIENTES EN CASTLAB ---")
    
    # Hacemos una prueba simulando que estos datos vienen de la recepción del laboratorio
    registrar_paciente("V-12345678", "Juan", "Pérez", 35, "M")
    registrar_paciente("V-87654321", "María", "Mendoza", 28, "F")
    
    # Si vuelves a correr el programa, la segunda vez debería darte la advertencia de cédula duplicada.