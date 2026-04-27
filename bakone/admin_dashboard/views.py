
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404
from django.utils.encoding import smart_str
from .models import CompanyDocument, Department
from .forms import CompanyDocumentForm
import os

# @login_required
# @user_passes_test(is_admin)
# def delete_folder(request, dept_id):
#     # Placeholder for delete folder logic
#     messages.info(request, 'Delete folder feature coming soon!')
#     return redirect('admin_dashboard:dashboard_home')


# ...existing code...




def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def download_document(request, doc_id):
    document = get_object_or_404(CompanyDocument, id=doc_id)
    try:
        response = FileResponse(document.file.open('rb'), as_attachment=True, filename=smart_str(document.file.name))
        return response
    except Exception:
        raise Http404('File not found or inaccessible.')

@login_required
@user_passes_test(is_admin)
def folder_view(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    documents = CompanyDocument.objects.filter(department=department).order_by('-uploaded_at')
    departments = Department.objects.all().order_by('name')
    return render(request, 'admin_dashboard/folder_view.html', {
        'department': department,
        'documents': documents,
        'departments': departments,
    })

@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    documents = CompanyDocument.objects.select_related('department').all().order_by('department__name', '-uploaded_at')
    return render(request, 'admin_dashboard/dashboard_home.html', {'documents': documents})

@login_required
@user_passes_test(is_admin)
def upload_document(request):
    if request.method == 'POST':
        form = CompanyDocumentForm(request.POST, request.FILES)
        new_department = request.POST.get('new_department')
        if form.is_valid():
            if new_department:
                department, created = Department.objects.get_or_create(name=new_department)
            else:
                department = form.cleaned_data.get('department')
            files = request.FILES.getlist('file')
            for f in files:
                ext = os.path.splitext(f.name)[1].lower()
                if ext not in ['.pdf', '.doc', '.docx']:
                    messages.error(request, f'File {f.name} is not a PDF or Word document.')
                    continue
                CompanyDocument.objects.create(
                    title=form.cleaned_data['title'],
                    department=department,
                    file=f,
                    uploaded_by=request.user
                )
            messages.success(request, f'{len(files)} document(s) uploaded successfully!')
            return redirect('admin_dashboard:dashboard_home')
    else:
        form = CompanyDocumentForm()
    documents = CompanyDocument.objects.all().order_by('-uploaded_at')
    departments = Department.objects.all().order_by('name')
    return render(request, 'admin_dashboard/upload_document.html', {
        'form': form,
        'documents': documents,
        'departments': departments,
    })

@login_required
@user_passes_test(is_admin)
def move_document(request, doc_id):
    # Placeholder for move logic
    messages.info(request, 'Move document feature coming soon!')
    return redirect('admin_dashboard:dashboard_home')
def scan_document(request, doc_id):
    # Placeholder for scan logic (e.g., OCR or virus scan)
    messages.info(request, 'Scan feature coming soon!')
    return redirect('admin_dashboard:dashboard_home')
