from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QComboBox
from citadel.presentation.viewmodels.sample_viewmodel import SampleViewModel
from citadel.core.models.enums import OrderOrigin

class OrderEntryView(QWidget):
    def __init__(self, viewmodel: SampleViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Create New Diagnostic Order"))

        self.origin_combo = QComboBox()
        self.origin_combo.addItems([OrderOrigin.OUTPATIENT.value, OrderOrigin.EMERGENCY.value, OrderOrigin.HOSPITALIZATION.value])
        layout.addWidget(self.origin_combo)

        self.test_list = QListWidget()
        self.test_list.addItems(["GLU", "CREA", "UREA"]) # Mock items
        layout.addWidget(self.test_list)

        self.create_order_btn = QPushButton("Generate Order & Barcodes")
        layout.addWidget(self.create_order_btn)

        self.create_order_btn.clicked.connect(self.on_create_order)

    def on_create_order(self):
        # Using dummy patient ID and test IDs for UI demo
        self.viewmodel.create_order(patient_id=1, physician="Dr. House", origin=OrderOrigin.OUTPATIENT, test_ids=[1])
