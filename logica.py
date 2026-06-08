import sqlite3
from datetime import datetime

# ==========================================
# 1. FUNCIÓN PARA REGISTRAR (Ya la conoces)
# ==========================================
def registrar_paciente(cedula, nombre, apellido, edad, sexo):
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        sql = """
        INSERT INTO pacientes (cedula, nombre, apellido, edad, sexo)
        VALUES (?, ?, ?, ?, ?)
        """
        dedo_lector.execute(sql, (cedula, nombre, apellido, edad, sexo))
        conexion.commit()
        print(f"   [ÉXITO] Paciente {nombre} {apellido} registrado correctamente.")
        
    except sqlite3.IntegrityError:
        print(f"   [ADVERTENCIA] La cédula {cedula} ya está registrada en el sistema.")
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo registrar: {e}")
    finally:
        conexion.close()

# ==========================================
# 2. FUNCIÓN PARA MODIFICAR DATOS
# ==========================================
def modificar_paciente(id_paciente, nueva_edad, nuevo_apellido):
    """
    Busca a un paciente por su ID único y actualiza su edad y apellido.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        # SQL usa UPDATE para modificar filas existentes
        # SET indica qué columnas van a cambiar
        # WHERE es el filtro de seguridad para alterar SOLO a ese paciente
        sql = """
        UPDATE pacientes 
        SET edad = ?, apellido = ? 
        WHERE id_paciente = ?
        """
        
        # Pasamos los nuevos datos y el ID del paciente al final
        dedo_lector.execute(sql, (nueva_edad, nuevo_apellido, id_paciente))
        conexion.commit()
        print(f"   [ÉXITO] Paciente ID {id_paciente} actualizado correctamente.")
        
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo modificar el paciente: {e}")
    finally:
        conexion.close()

# ==========================================
# 3. FUNCIÓN PARA ELIMINAR REGISTROS
# ==========================================
def eliminar_paciente(id_paciente):
    """
    Elimina por completo a un paciente y todas sus órdenes asociadas (en cascada).
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        # Comprobamos que el soporte de claves foráneas esté encendido para el borrado en cascada
        dedo_lector.execute("PRAGMA foreign_keys = ON;")
        
        # DELETE FROM borra la fila completa que coincida con el WHERE
        sql = "DELETE FROM pacientes WHERE id_paciente = ?"
        
        # Nota: Cuando pasas un solo dato en la tupla, se debe poner una coma al final (id_paciente,)
        # para que Python sepa que sigue siendo una tupla y no un simple paréntesis matemático.
        dedo_lector.execute(sql, (id_paciente,))
        conexion.commit()
        print(f"   [ÉXITO] Paciente ID {id_paciente} eliminado del sistema.")
        
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo eliminar al paciente: {e}")
    finally:
        conexion.close()


# ==========================================
# BLOQUE DE PRUEBAS DE CASOS DE USO
# ==========================================
if __name__ == "__main__":
    print("--- EJECUTANDO PRUEBAS DE CASOS DE USO ---")
    
    # 1. Registramos un tercer paciente de prueba
    registrar_paciente("V-99999999", "Carlos", "Silva", 40, "M")
    
    # 2. Vamos a simular que Carlos cumplió años y se cambió el apellido.
    # Como es el tercer paciente, asumimos que su id_paciente es el 3.
    modificar_paciente(3, 41, "Silva Uzcátegui")
    
    # 3. Prueba de eliminación: Si quisieras borrarlo, descomenta la línea de abajo borrando el '#'
    #eliminar_paciente(3)