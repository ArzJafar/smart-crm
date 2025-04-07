# urls.py
from django.urls import path
from . import views

app_name="hr"
urlpatterns = [
    path('', views.home, name='home'),
    path('view_pdfs/', views.view_pdfs, name='view_pdfs'),
    path('download_pdf/<int:pdf_id>/', views.download_pdf, name='download_pdf'),
]
