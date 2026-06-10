import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
# Importamos TU motor de búsqueda del backend
from logica import buscar_paciente_por_cedula

class VentanaCastLab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CastLab - Módulo de Recepción (Tráiler)")
        self.setGeometry(500, 100, 800, 150)
        
        # Diseño Principal Vertical
        diseno_vertical = QVBoxLayout()
        
        # Diseño Horizontal para la búsqueda
        diseno_busqueda = QHBoxLayout()
        self.caja_cedula = QLineEdit()
        self.caja_cedula.setPlaceholderText("Ingrese cédula (Ej: V-88888888)")
        self.boton_buscar = QPushButton("Buscar Paciente")
        
        diseno_busqueda.addWidget(self.caja_cedula)
        diseno_busqueda.addWidget(self.boton_buscar)
        
        # Etiqueta para mostrar el resultado en la pantalla
        self.etiqueta_resultado = QLabel("Monitoreo del sistema: Esperando búsqueda...")
        self.etiqueta_resultado.setStyleSheet("font-size: 14px; color: blue; font-weight: bold;")
        
        # Unimos los Legos visuales
        diseno_vertical.addLayout(diseno_busqueda)
        diseno_vertical.addWidget(self.etiqueta_resultado)
        self.setLayout(diseno_vertical)
        
        # Conectamos el botón visual con nuestra lógica real del backend
        self.boton_buscar.clicked.connect(self.ejecutar_busqueda_visual)

    def ejecutar_busqueda_visual(self):
        cedula_ingresada = self.caja_cedula.text()
        
        # Llamamos a tu función del backend pasándole lo que el usuario escribió en la pantalla
        paciente = buscar_paciente_por_cedula(cedula_ingresada)
        
        if paciente:
            # paciente[1] es el nombre, paciente[2] es el apellido en tu tupla
            self.etiqueta_resultado.setText(f"✅ PACIENTE ENCONTRADO:\n{paciente[2]} {paciente[3]} (Edad: {paciente[4]})")
            self.etiqueta_resultado.setStyleSheet("color: green; font-size: 14px;")
        else:
            self.etiqueta_resultado.setText("❌ El paciente no existe en la base de datos.")
            self.etiqueta_resultado.setStyleSheet("color: red; font-size: 14px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCastLab()
    ventana.show()
    sys.exit(app.exec())