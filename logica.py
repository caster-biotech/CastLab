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

## ==========================================
# 3. FUNCIÓN PARA CREAR ORDENEISHONS
## ==========================================

def crear_orden(id_paciente):
    """
    Crea una nueva orden de trabajo para un paciente existente,
    registrando la fecha y hora exacta de forma automática.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        # Activamos las claves foráneas por seguridad
        dedo_lector.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Capturamos la fecha y hora actual del sistema
        # datetime.now() nos da un objeto con el segundo exacto.
        # .strftime("%Y-%m-%d %H:%M:%S") lo transforma en un texto limpio: "2026-06-08 19:15:30"
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Todas las órdenes nuevas nacen con el estado 'Pendiente'
        estado_inicial = "Pendiente"
        
        # 2. Preparamos el SQL. Nota que no insertamos 'id_orden' porque es autoincremental
        sql = """
        INSERT INTO ordenes (id_paciente, fecha, estado)
        VALUES (?, ?, ?)
        """
        
        dedo_lector.execute(sql, (id_paciente, fecha_actual, estado_inicial))
        conexion.commit()
        
        # 3. SQLite nos permite saber cuál fue el número de ID que se generó automáticamente
        # para esta última orden usando 'lastrowid'
        id_orden_generada = dedo_lector.lastrowid
        
        print(f"   [ÉXITO] Orden N° {id_orden_generada} creada para el Paciente ID {id_paciente} el {fecha_actual}.")
        
        # Devolvemos el número de orden porque lo necesitaremos para el siguiente paso: meter los exámenes
        return id_orden_generada
        
    except sqlite3.IntegrityError:
        # Este error salta si intentas crear una orden para un id_paciente que NO existe en el sistema
        print(f"   [ERROR] No se puede crear la orden. El Paciente ID {id_paciente} no existe.")
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo crear la orden: {e}")
    finally:
        conexion.close()
        
# ==========================================
# BLOQUE DE PRUEBAS DE CASOS DE USO
# ==========================================

if __name__ == "__main__":
    print("--- PROBANDO CREACIÓN DE ÓRDENES EN CASTLAB ---")
    
    # Simulamos que viene el Paciente ID 1 (Juan) y le creamos una orden
    id_nueva_orden = crear_orden(1)
    
    # Simulamos un error a propósito: intentamos crear una orden para el paciente ID 99 (que no existe)
    # Gracias a las claves foráneas que programamos, la base de datos debería rechazarlo
    crear_orden(99)


# if __name__ == "__main__":
    # print("--- EJECUTANDO PRUEBAS DE CASOS DE USO ---")
    
    # 1. Registramos un tercer paciente de prueba
    # registrar_paciente("V-99999999", "Carlos", "Silva", 40, "M")
    
    # 2. Vamos a simular que Carlos cumplió años y se cambió el apellido.
    # Como es el tercer paciente, asumimos que su id_paciente es el 3.
    # modificar_paciente(3, 41, "Silva Uzcátegui")
    
    # 3. Prueba de eliminación: Si quisieras borrarlo, descomenta la línea de abajo borrando el '#'
    #eliminar_paciente(3)