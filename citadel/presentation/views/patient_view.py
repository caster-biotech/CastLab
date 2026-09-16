from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit
from citadel.presentation.viewmodels.patient_viewmodel import PatientViewModel

class PatientView(QWidget):
    def __init__(self, viewmodel: PatientViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.national_id_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.birth_date_input = QDateEdit()
        self.sex_combo = QComboBox()
        self.sex_combo.addItems(["MALE", "FEMALE", "OTHER"])

        form.addRow("National ID:", self.national_id_input)
        form.addRow("First Name:", self.first_name_input)
        form.addRow("Last Name:", self.last_name_input)
        form.addRow("Birth Date:", self.birth_date_input)
        form.addRow("Biological Sex:", self.sex_combo)

        self.search_btn = QPushButton("Search")
        self.save_btn = QPushButton("Save Patient")

        layout.addLayout(form)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.save_btn)

    def connect_signals(self):
        self.search_btn.clicked.connect(lambda: self.viewmodel.search_patient(self.national_id_input.text()))
        # Additional connections omitted for brevity
