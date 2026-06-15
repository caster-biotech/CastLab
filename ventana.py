import sys
from logica import registrar_paciente

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, 
    QLineEdit, QDateEdit, QComboBox, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import QDate

class VentanaRecepcion(QWidget):
    def __init__(self):
        super().__init__()
        # 1. Configuración básica de la ventana
        self.setWindowTitle("CastLab - Registro de Pacientes")
        self.setMinimumWidth(450)
        
        # 2. Creamos el Layout Principal (Vertical)
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)
        
        # 3. Título visual en la parte superior
        self.etiqueta_titulo = QLabel("REGISTRO DE NUEVO PACIENTE")
        self.etiqueta_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #3b82f6; margin-bottom: 10px;")
        self.layout_principal.addWidget(self.etiqueta_titulo)
        
        # 4. Creamos el Formulario (Layout de dos columnas)
        self.formulario = QFormLayout()
        self.layout_principal.addLayout(self.formulario)
        
        # --- CAMPOS DEL FORMULARIO ---
        
        # Cédula
        self.caja_cedula = QLineEdit()
        self.caja_cedula.setPlaceholderText("Ej: V-12345678")
        self.formulario.addRow("Cédula:", self.caja_cedula)
        
        # Nombre
        self.caja_nombre = QLineEdit()
        self.formulario.addRow("Nombre:", self.caja_nombre)
        
        # Apellido
        self.caja_apellido = QLineEdit()
        self.formulario.addRow("Apellido:", self.caja_apellido)
        
        # Fecha de Nacimiento (Componente Inteligente)
        self.caja_fecha_nac = QDateEdit()
        self.caja_fecha_nac.setCalendarPopup(True) # Activa el calendario desplegable
        self.caja_fecha_nac.setMaximumDate(QDate.currentDate()) # No permite fechas futuras
        self.caja_fecha_nac.setDate(QDate(2000, 1, 1)) # Fecha por defecto
        self.formulario.addRow("F. Nacimiento:", self.caja_fecha_nac)
        
        # Sexo (Menú Desplegable)
        self.combo_sexo = QComboBox()
        self.combo_sexo.addItems(["Masculino", "Femenino"])
        self.formulario.addRow("Sexo:", self.combo_sexo)
        
        # 5. Botón de Registro
        self.boton_registrar = QPushButton("REGISTRAR PACIENTE")
        self.boton_registrar.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        # Conectamos el clic del botón a nuestra función lógica
        self.boton_registrar.clicked.connect(self.ejecutar_registro)
        self.layout_principal.addWidget(self.boton_registrar)

    def ejecutar_registro(self):
        # 1. Extraemos los textos de la pantalla
        cedula = self.caja_cedula.text().strip()
        nombre = self.caja_nombre.text().strip()
        apellido = self.caja_apellido.text().strip()
        sexo = self.combo_sexo.currentText()
        
        # 2. Validación de seguridad básica
        if not cedula or not nombre or not apellido:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, llene Cédula, Nombre y Apellido.")
            return

        # 3. MÁGIA MATEMÁTICA TEMPORAL: Calcular edad basándonos en el año
        año_nacimiento = self.caja_fecha_nac.date().year()
        año_actual = QDate.currentDate().year()
        edad_calculada = año_actual - año_nacimiento

        # 4. LLAMADA AL BACKEND REAL
        # Enviamos los datos directos a la función de tu archivo logica.py
        exito = registrar_paciente(cedula, nombre, apellido, edad_calculada, sexo)

        print(f"--- ESPÍA: Lo que recibió la ventana fue: {exito} ---")
        
        # 5. Respuesta visual al usuario
        if exito:
            QMessageBox.information(self, "Éxito", f"¡Paciente {nombre} {apellido} guardado en la Base de Datos!")
            
            # Limpiamos las cajas para el siguiente paciente
            self.caja_cedula.clear()
            self.caja_nombre.clear()
            self.caja_apellido.clear()
            self.caja_fecha_nac.setDate(QDate(2000, 1, 1))
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar. Posiblemente la cédula ya existe.")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRecepcion()
    ventana.show()
    sys.exit(app.exec())

### Explicación rápida de las líneas clave:

### 1.  **`QFormLayout`**: Es el que hace el trabajo sucio de poner la etiqueta (ej: "Cédula:") al lado de la caja de texto. Si usáramos `QVBoxLayout`, saldría uno arriba del otro.
### 2.  **`setCalendarPopup(True)`**: Esta es la línea mágica. Sin ella, el usuario tendría que escribir la fecha con los numeritos. Con ella, sale el calendario de Windows/Mac.
### 3.  **`setMaximumDate(QDate.currentDate())`**: Es el **Guardián Visual**. Evita que alguien registre a un paciente nacido en el año 2030.
### 4.  **`setStyleSheet`**: Aquí es donde aplicas tu conocimiento de CSS. Fíjate que la sintaxis es casi idéntica: `background-color`, `border-radius`, `padding`.
### 5.  **`self.boton_registrar.clicked.connect(...)`**: Es el cable. Le dice al botón: "Cuando te toquen, corre a buscar la función `ejecutar_registro`". ###

# Qué te parece este diseño? Si lo ejecutas ahora mismo, verás una ventana profesional, azul y gris, lista para recibir pacientes. Pruébalo y dime si el calendario funciona como esperabas. ¡A por ello!