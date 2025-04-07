# views.py
import os
from django.shortcuts import render
from django.conf import settings
from .models import UserPDF
from datetime import datetime

def load_pdfs_from_directory():
    pdf_directory = 'D:/Pro/Smart/smartchekad/reports/'
    pdf_files = os.listdir(pdf_directory)
    
    for file_name in pdf_files:
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_directory, file_name)
            
            name, surname = file_name.replace('.pdf', '').split('-')
            
            created_at = datetime.fromtimestamp(os.path.getmtime(file_path))
            UserPDF.objects.get_or_create(
                name=name,
                surname=surname,
                file=file_path,
                created_at=created_at
            )

def view_pdfs(request):
    load_pdfs_from_directory()

    pdfs = UserPDF.objects.all().order_by('-created_at')
    return render(request, 'view_pdfs.html', {'pdfs': pdfs})

def download_pdf(request, pdf_id):
    pdf = UserPDF.objects.get(id=pdf_id)
    file_path = pdf.file

    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
def home(request):
    pdfs = UserPDF.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'pdfs': pdfs})