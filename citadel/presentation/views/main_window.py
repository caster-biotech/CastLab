from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QStatusBar
from citadel.presentation.views.patient_view import PatientView
from citadel.presentation.views.order_entry_view import OrderEntryView
from citadel.presentation.views.worksheet_view import WorksheetView

class MainWindow(QMainWindow):
    def __init__(self, patient_view: PatientView, order_view: OrderEntryView, worksheet_view: WorksheetView, user_role: str):
        super().__init__()
        self.setWindowTitle("Citadel LIS")
        self.resize(1024, 768)
        
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        
        self.sidebar = QListWidget()
        self.sidebar.addItems(["Patients", "Order Entry", "Worksheets", "Reports"])
        self.sidebar.setMaximumWidth(200)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(patient_view)
        self.stack.addWidget(order_view)
        self.stack.addWidget(worksheet_view)
        
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)
        
        status = QStatusBar()
        status.showMessage(f"Active Session: BIOANALIST ({user_role})")
        self.setStatusBar(status)
