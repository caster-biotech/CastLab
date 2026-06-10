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
# 4. FUNCIÓN PARA REGISTRAR RESULTADOS DE EXÁMENES
# ==========================================

def registrar_resultado(id_orden, nombre_examen, valor_resultado="En proceso", parametro="General"):
    """
    Vincula un examen específico a una orden de trabajo existente.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        dedo_lector.execute("PRAGMA foreign_keys = ON;")
        
        # Copia esto tal cual: Tabla 'resultados', columnas correspondientes
        sql = """
        INSERT INTO resultados (id_orden, nombre_examen, valor_resultado, parametro)
        VALUES (?, ?, ?, ?)
        """
        
        dedo_lector.execute(sql, (id_orden, nombre_examen, valor_resultado, parametro))
        conexion.commit()
        print(f"   [ÉXITO] Examen '{nombre_examen}' agregado a la Orden N° {id_orden} ({valor_resultado}).")
        
    except sqlite3.IntegrityError as e:
        # Ahora el cartel nos dirá el motivo REAL del error de integridad
        print(f"   [ERROR DE INTEGRIDAD REAL]: {e}")
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo registrar el resultado: {e}")
    finally:
        conexion.close()

# ==========================================
# 5. FUNCIÓN PARA BUSCAR PACIENTES POR CÉDULA (ÚTIL PARA PRUEBAS)
# ==========================================

def buscar_paciente_por_cedula(cedula):
    """
    Busca un paciente en la base de datos por su número de cédula.
    Devuelve los datos del paciente si existe, o None si no lo encuentra.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        dedo_lector = conexion.cursor()
        
        # El comando SELECT le dice: "Trae todos los campos (*) de la tabla pacientes
        # pero FILTRA donde la cédula sea igual a la que te estoy pasando"
        sql = "SELECT * FROM pacientes WHERE cedula = ?"
        
        dedo_lector.execute(sql, (cedula,))
        
        # fetchone() es el comando que le dice a Python: "Tráeme la primera fila que encuentres"
        paciente = dedo_lector.fetchone()
        
        return paciente # Devuelve la tupla con los datos (ej. ('V-88888888', 'Daniel', ...))
        
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] Error al buscar paciente: {e}")
        return None
    finally:
        conexion.close()
# ==========================================
# BLOQUE DE PRUEBAS DE CASOS DE USO
# ==========================================

if __name__ == "__main__":
    print("--- SIMULANDO FLUJO FELIZ COMPLETO EN CASTLAB ---")
    
    print("\n--- PASO 1: Registrando / Verificando Paciente ---")
    cedula_prueba = "V-88888888"
    
    # Antes de registrar a lo loco, el sistema primero BUSCA
    paciente_encontrado = buscar_paciente_por_cedula(cedula_prueba)
    
    if paciente_encontrado:
        print(f"   [SISTEMA] El paciente ya existe en los archivos: {paciente_encontrado[1]} {paciente_encontrado[2]}")
        id_paciente_prueba = 1 # Ya sabemos que Daniel es el 1
    else:
        print("   [SISTEMA] Paciente nuevo. Registrando en la base de datos...")
        registrar_paciente(cedula_prueba, "Daniel", "Acabal", 35, "M")
        id_paciente_prueba = 1
        
    print(f"\n--- PASO 2: Creando Orden de Trabajo para el ID {id_paciente_prueba} ---")
    orden_generada = crear_orden(id_paciente_prueba)
    
    if orden_generada:
        print("\n--- PASO 3: Cargando Exámenes a la Orden ---")
        registrar_resultado(orden_generada, "Hematología Completa")
        registrar_resultado(orden_generada, "Glicemia", "105 mg/dL")