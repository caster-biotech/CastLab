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
# 6. FUNCIÓN PARA ACTUALIZAR RESULTADOS DE EXÁMENES 
# ==========================================

def actualizar_resultado(id_resultado, nuevo_valor):
    """
    Actualiza el valor de un examen específico y cambia su estado a 'Listo'.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        cursor = conexion.cursor()
        
        # El plano del cambio: Modifica la tabla resultados,
        # cambia el valor y el estado, pero SOLO para ese ID.
        sql = """
            UPDATE resultados 
            SET valor_resultado = ?, parametro = 'Listo' 
            WHERE id_resultado = ?
        """
        
        # Pasamos los datos en el mismo orden de los signos de interrogación
        cursor.execute(sql, (nuevo_valor, id_resultado))
        
        # Como estamos ALTERANDO el archivo físico, necesitamos el commit
        conexion.commit()
        print(f"   [ÉXITO] Resultado ID {id_resultado} actualizado a: {nuevo_valor}")
        return True
        
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo actualizar el resultado: {e}")
        return False
    finally:
        conexion.close()


# ==========================================
# 7. FUNCIÓN PARA VALIDAR ORDENES
# ==========================================

def validar_orden(id_orden):
    """
    Cambia el estado de una orden completa a 'Validada', 
    lo que significa que todos sus exámenes están listos para entrega.
    """
    try:
        conexion = sqlite3.connect("castlab.db")
        cursor = conexion.cursor()
        
        # El plano: Modifica la tabla ordenes, cambia el estado,
        # pero SOLO para esa orden específica.
        sql = """
            UPDATE ordenes 
            SET estado = 'Validada' 
            WHERE id_orden = ?
        """
        
        cursor.execute(sql, (id_orden,))
        conexion.commit()
        
        print(f"   [SISTEMA] Orden N° {id_orden} ha sido VALIDADA COMPLETAMENTE para entrega.")
        return True
        
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo validar la orden: {e}")
        return False
    finally:
        conexion.close()

# ==========================================
# 8. FUNCIÓN PARA ANULAR ORDENES
# ==========================================


def anular_orden(id_orden):
    """
    Elimina una orden de la base de datos de forma definitiva.
    Por configuración de cascada, esto borrará también todos sus exámenes asociados.
    """
    try: 
        conexion = sqlite3.connect("castlab.db")
        cursor = conexion.cursor()

        sql = "DELETE FROM ordenes WHERE id_orden = ?"

        cursor.execute(sql, (id_orden,))
        conexion.commit()

        print(f"¨[SISTEMA] Orden N° {id_orden} ha sido anulada y eliminada con exito (y sus examenes tambien, en cascada)")
        return True
    
    except sqlite3.Error as e:
        print(f" [ERROR CRITICO] No se pudo anular la orden por: {e}")
        return False
    finally:     
        conexion.close()

        
# ==========================================
# BLOQUE DE PRUEBAS DE CASOS DE USO
# ==========================================

if __name__ == "__main__":
    print("=== SIMULANDO UN DÍA REAL EN CASTLAB (14 DE JUNIO) ===")
    
    # 1. RECEPCIÓN: Llega el paciente y lo buscamos/registramos
    cedula_paciente = "V-88888888"
    paciente = buscar_paciente_por_cedula(cedula_paciente)
    
    if paciente:
        print(f"   [RECEPCIÓN] Paciente encontrado: {paciente[2]} {paciente[3]}")
        id_paciente_real = paciente[0]
    else:
        print("   [RECEPCIÓN] Paciente nuevo. Registrando...")
        # Si no existiera, lo registramos aquí
        id_paciente_real = 1 

    # 2. FACTURACIÓN: Se genera la orden de trabajo
    print("\n--- PASO 2: Generando orden de trabajo ---")
    id_orden_nueva = crear_orden(id_paciente_real)
    
    if id_orden_nueva:
        # 3. RECEPCIÓN: Se le cargan los exámenes solicitados (nacen "En proceso")
        print("\n--- PASO 3: Cargando exámenes solicitados ---")
        registrar_resultado(id_orden_nueva, "Glicemia")
        # Imaginemos que el sistema nos asigna el ID de examen 1 para esta prueba
        
        # 4. ÁREA TÉCNICA: El bioanalista monta la muestra y carga el resultado
        print("\n--- PASO 4: Área Técnica procesa la muestra ---")
        id_examen_glicemia = 1 
        actualizar_resultado(id_examen_glicemia, "104 mg/dL")
        
        # 5. VALIDACIÓN: Como ya están listos los exámenes, se sella la orden completa
        print("\n--- PASO 5: Control de Calidad / Validación Final ---")
        validar_orden(id_orden_nueva)

    print("\n=== FIN DE LA SIMULACIÓN DE HOY ===")

    # 6. ERROR HUMANO: Nos damos cuenta de que la orden era de otro paciente. ¡La anulamos!
print("\n--- PASO 6: Se detecta error y se anula la orden ---")
anular_orden(id_orden_nueva)

