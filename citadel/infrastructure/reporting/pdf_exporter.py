import os
from citadel.core.ports.report_exporter import ReportExporterPort
from citadel.core.models.patient import Patient
from citadel.core.models.sample import Sample
from citadel.core.models.result import Result
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

class PdfReportExporter(ReportExporterPort):
    def generate_patient_report(self, patient: Patient, sample: Sample, results: list[Result], output_path: str) -> str:
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Citadel Laboratory Information System", styles['Title']))
        elements.append(Paragraph("Official Clinical Report", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        patient_info = [
            f"Patient Name: {patient.first_name} {patient.last_name}",
            f"National ID: {patient.national_id}",
            f"Age (Years): {patient.age_in_years}",
            f"Biological Sex: {patient.sex.value}",
        ]
        for info in patient_info:
            elements.append(Paragraph(info, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        table_data = [["Test ID", "Result Value", "Status", "Flag"]]
        for res in results:
            flag = "PANIC" if res.is_panic else "NORMAL"
            table_data.append([str(res.test_id), str(res.obtained_value), res.status.value, flag])
            
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))
        
        elements.append(Paragraph("Validated By: Bioanalyst", styles['Heading3']))
        elements.append(Paragraph("License Number: 123456", styles['Normal']))
        
        doc.build(elements)
        return output_path
