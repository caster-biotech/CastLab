# (Esto va abajo de las funciones anteriores, antes del bloque 'if __name__')

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
        
    except sqlite3.ForeignKeyConstraintError:
        # Este error salta si intentas crear una orden para un id_paciente que NO existe en el sistema
        print(f"   [ERROR] No se puede crear la orden. El Paciente ID {id_paciente} no existe.")
    except sqlite3.Error as e:
        print(f"   [ERROR CRÍTICO] No se pudo crear la orden: {e}")
    finally:
        conexion.close()