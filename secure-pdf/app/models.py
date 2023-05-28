from django.db import models
from django.core.validators import FileExtensionValidator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Vulnerability(models.Model):
    title = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)
    description = models.TextField()
    remediation = models.TextField()
    
    def __str__(self):
        return self.title


class pdfFile(models.Model):
    title = models.CharField(max_length=100)
    vulnerabilities = models.ManyToManyField(Vulnerability, related_name='reports')
    pdf = models.FileField(upload_to="pdf/", validators=[FileExtensionValidator(["pdf"])])

    def __str__(self):
        return self.title

    def generate_pdf_report(self):
        report_path = f"media/pdf/{self.title}.pdf"
        c = canvas.Canvas(report_path, pagesize=letter)
        c.setFont("Helvetica", 14)
        c.drawString(100, 700, "Vulnerability Assessment Penetration Testing Report")

        # Add report content
        c.setFont("Helvetica", 12)
        y_position = 650
        c.drawString(100, y_position, "Report Title:")
        c.drawString(250, y_position, self.title)

        y_position -= 30
        c.drawString(100, y_position, "Vulnerabilities:")
        for i, vulnerability in enumerate(self.vulnerabilities.all(), start=1):
            c.drawString(250, y_position, f"{i}. {vulnerability.title}")
            y_position -= 20
            c.drawString(270, y_position, "Severity:")
            c.drawString(380, y_position, vulnerability.severity)
            y_position -= 20
            c.drawString(270, y_position, "Description:")
            description_lines = vulnerability.description.split("\n")
            for line in description_lines:
                c.drawString(380, y_position, line)
                y_position -= 20
            c.drawString(270, y_position, "Remediation:")
            remediation_lines = vulnerability.remediation.split("\n")
            for line in remediation_lines:
                c.drawString(380, y_position, line)
                y_position -= 20
            y_position -= 10

        c.save()
        self.pdf.name = f"pdf/{self.title}.pdf"
        self.save()
