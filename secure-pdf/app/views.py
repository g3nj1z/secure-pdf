from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
import os
from .models import pdfFile, Vulnerability

@login_required(login_url='login')
def index(request):
    obj = pdfFile.objects.all()
    return render(request, "index.html", {"obj": obj})

@login_required(login_url='login')
def securePdf(request, file):
    document = get_object_or_404(pdfFile, pdf="pdf/" + file)
    path, file_name = os.path.split(file)
    response = FileResponse(document.pdf)
    return response

@login_required(login_url='login')
def generate_pdf(request):
    if request.method == "POST":
        title = request.POST.get("title")
        vulnerabilities = []
        for i in range(1, 6):
            vuln_title = request.POST.get(f"vuln_title_{i}")
            severity = request.POST.get(f"severity_{i}")
            description = request.POST.get(f"description_{i}")
            remediation = request.POST.get(f"remediation_{i}")
            if vuln_title and severity and description and remediation:
                vulnerability = Vulnerability.objects.create(
                    title=vuln_title,
                    severity=severity,
                    description=description,
                    remediation=remediation,
                )
                vulnerabilities.append(vulnerability)

        new_pdf = pdfFile.objects.create(title=title)
        new_pdf.vulnerabilities.set(vulnerabilities)
        new_pdf.generate_pdf_report()
        return redirect("index")

    return render(request, "generate_pdf.html", {"reports": pdfFile.objects.all()})
