from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),  # Keep this one
    path('search/', views.search_items, name='search_items'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
]
    # Removed the duplicate path for 'upload/'