import sys
from PyQt6.QtWidgets import QApplication
from citadel.infrastructure.database.connection import create_db_engine, init_db, get_session
from citadel.application.patient_service import PatientService
from citadel.application.sample_service import SampleService
from citadel.application.worksheet_service import WorksheetService
from citadel.presentation.viewmodels.patient_viewmodel import PatientViewModel
from citadel.presentation.viewmodels.sample_viewmodel import SampleViewModel
from citadel.presentation.viewmodels.worksheet_viewmodel import WorksheetViewModel
from citadel.presentation.views.patient_view import PatientView
from citadel.presentation.views.order_entry_view import OrderEntryView
from citadel.presentation.views.worksheet_view import WorksheetView
from citadel.presentation.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    engine = create_db_engine()
    init_db(engine)
    
    session = next(get_session(engine))
    
    patient_service = PatientService(session)
    sample_service = SampleService(session)
    worksheet_service = WorksheetService(session)
    
    patient_vm = PatientViewModel(patient_service)
    sample_vm = SampleViewModel(sample_service)
    worksheet_vm = WorksheetViewModel(worksheet_service)
    
    patient_view = PatientView(patient_vm)
    order_view = OrderEntryView(sample_vm)
    worksheet_view = WorksheetView(worksheet_vm)
    
    main_window = MainWindow(patient_view, order_view, worksheet_view, "BIOANALIST")
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
