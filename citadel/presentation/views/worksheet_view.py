from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtGui import QColor
from citadel.presentation.viewmodels.worksheet_viewmodel import WorksheetViewModel
from citadel.core.models.enums import ResultStatus

class WorksheetView(QWidget):
    def __init__(self, viewmodel: WorksheetViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Result ID", "Test", "Value", "Status"])
        layout.addWidget(self.table)
        
        self.submit_btn = QPushButton("Submit Bulk Results")
        layout.addWidget(self.submit_btn)
        
    def highlight_panic(self, row: int, is_panic: bool):
        if is_panic:
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("red"))
