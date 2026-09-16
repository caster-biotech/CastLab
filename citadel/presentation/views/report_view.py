from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QLabel
from citadel.presentation.viewmodels.report_viewmodel import ReportViewModel

class ReportView(QWidget):
    def __init__(self, viewmodel: ReportViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Export Patient Report"))
        
        self.sample_id_input = QLineEdit()
        self.sample_id_input.setPlaceholderText("Enter Sample ID")
        layout.addWidget(self.sample_id_input)
        
        self.export_btn = QPushButton("Export PDF Report")
        self.export_btn.clicked.connect(self.on_export)
        layout.addWidget(self.export_btn)
        
        self.viewmodel.report_generated.connect(self.on_success)
        self.viewmodel.error_occurred.connect(self.on_error)
        
    def on_export(self):
        sample_id_str = self.sample_id_input.text()
        if not sample_id_str.isdigit():
            QMessageBox.warning(self, "Error", "Invalid Sample ID")
            return
            
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.viewmodel.generate_report(int(sample_id_str), output_dir)
            
    def on_success(self, path: str):
        QMessageBox.information(self, "Success", f"Report successfully generated at:\n{path}")
        
    def on_error(self, message: str):
        QMessageBox.critical(self, "Error", f"Failed to generate report:\n{message}")
