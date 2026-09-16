from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QComboBox, QLineEdit, QMessageBox
from citadel.presentation.viewmodels.sample_viewmodel import SampleViewModel
from citadel.core.models.enums import OrderOrigin

class OrderEntryView(QWidget):
    def __init__(self, viewmodel: SampleViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Create New Diagnostic Order"))

        # Lookup section
        lookup_layout = QHBoxLayout()
        self.national_id_input = QLineEdit()
        self.national_id_input.setPlaceholderText("Enter National ID")
        self.lookup_btn = QPushButton("Lookup / Verify")
        lookup_layout.addWidget(QLabel("National ID:"))
        lookup_layout.addWidget(self.national_id_input)
        lookup_layout.addWidget(self.lookup_btn)
        layout.addLayout(lookup_layout)

        # Demographics info display
        self.patient_info_label = QLabel("Patient Info: Not verified")
        layout.addWidget(self.patient_info_label)

        self.origin_combo = QComboBox()
        self.origin_combo.addItems([OrderOrigin.OUTPATIENT.value, OrderOrigin.EMERGENCY.value, OrderOrigin.HOSPITALIZATION.value])
        layout.addWidget(self.origin_combo)

        self.test_list = QListWidget()
        self.test_list.addItems(["GLU", "CREA", "UREA"]) 
        layout.addWidget(self.test_list)

        self.create_order_btn = QPushButton("Generate Order & Barcodes")
        layout.addWidget(self.create_order_btn)

    def connect_signals(self):
        self.lookup_btn.clicked.connect(self.on_lookup)
        self.create_order_btn.clicked.connect(self.on_create_order)
        self.viewmodel.patient_found.connect(self.on_patient_found)
        self.viewmodel.order_created.connect(self.on_order_created)
        self.viewmodel.error_occurred.connect(self.on_error)

    def on_lookup(self):
        nid = self.national_id_input.text().strip()
        if nid:
            self.viewmodel.lookup_patient(nid)
        else:
            QMessageBox.warning(self, "Warning", "Please enter a National ID.")

    def on_patient_found(self, patient):
        self.patient_info_label.setText(f"Patient Info: {patient.first_name} {patient.last_name}, Age: {patient.age_in_years}, Sex: {patient.sex}")

    def on_create_order(self):
        nid = self.national_id_input.text().strip()
        if not nid:
            QMessageBox.warning(self, "Warning", "National ID is required.")
            return
        
        origin_val = self.origin_combo.currentText()
        origin = OrderOrigin(origin_val)
        # Mocking test_ids for demo
        self.viewmodel.create_order(national_id=nid, physician="Dr. House", origin=origin, test_ids=[1])

    def on_order_created(self, order, samples):
        QMessageBox.information(self, "Success", f"Order {order.order_id} created successfully!")

    def on_error(self, err):
        QMessageBox.critical(self, "Error", str(err))
