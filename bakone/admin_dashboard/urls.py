from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('folder/<int:dept_id>/', views.folder_view, name='folder_view'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download/<int:doc_id>/', views.download_document, name='download_document'),
    path('scan/<int:doc_id>/', views.scan_document, name='scan_document'),
    path('move/<int:doc_id>/', views.move_document, name='move_document'),
    # path('delete_folder/<int:dept_id>/', views.delete_folder, name='delete_folder'),
    # path('rename_folder/<int:dept_id>/', views.rename_folder, name='rename_folder'),
    # path('delete_doc/<int:doc_id>/', views.delete_document, name='delete_document'),
    # path('replace_doc/<int:doc_id>/', views.replace_document, name='replace_document'),
]
