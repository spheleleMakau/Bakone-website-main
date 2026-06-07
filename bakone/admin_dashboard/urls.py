from django.urls import path
from . import views

app_name = 'admin_dashboard'
from django.urls import path
from .views import create_admin

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('folder/<int:dept_id>/', views.folder_view, name='folder_view'),
    path('upload/', views.upload_document, name='upload_document'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('view/<int:doc_id>/', views.view_document, name='view_document'),
    path('preview/<int:doc_id>/', views.preview_document, name='preview_document'),
    path('download/<int:doc_id>/', views.download_document, name='download_document'),
    path('scan/<int:doc_id>/', views.scan_document, name='scan_document'),
    path('move/<int:doc_id>/', views.move_document, name='move_document'),
    path('delete/<int:doc_id>/', views.delete_document, name='delete_document'),
    path("create-admin/", create_admin),
]
