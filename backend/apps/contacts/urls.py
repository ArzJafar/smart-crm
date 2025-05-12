from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.public_contacts_list, name='public_contacts_list'),
    path('add-public/', views.add_public_contact, name='add_public_contact'),
    path('search/', views.search_contacts, name='search_contacts'),
    path('public-search/', views.search_public_contacts, name='search_public_contacts'),
    path('public-export-csv/', views.public_export_contacts_csv, name='public_export_contacts_csv'),
    path('public-import-csv/', views.public_import_contacts_csv, name='public_import_contacts_csv'),
    path('delete-public-contact/<int:pk>/', views.delete_public_contact, name='delete_public_contact'),
    path('public-details/<int:pk>/', views.public_contact_details, name='public_contact_details'),
    path('colleagues/', views.colleagues, name='colleagues'),
    path('guide', views.guide, name='guide'),
    path("contact/<int:contact_id>/edit/", views.edit_contact, name="edit_contact"),
    path("contact/<int:contact_id>/update/", views.update_contact, name="update_contact"),
]
