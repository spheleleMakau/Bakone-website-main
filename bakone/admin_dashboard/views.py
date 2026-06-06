
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.http import FileResponse, Http404
from django.urls import reverse
from django.utils.encoding import smart_str
from .models import CompanyDocument, Department
from .forms import CompanyDocumentForm, DepartmentForm, DocumentMoveForm
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
def preview_document(request, doc_id):
    document = get_object_or_404(CompanyDocument, id=doc_id)
    try:
        ext = os.path.splitext(document.file.name)[1].lower()
        content_type = 'application/pdf' if ext == '.pdf' else (
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document' if ext == '.docx' else
            'application/msword' if ext == '.doc' else 'application/octet-stream'
        )
        response = FileResponse(
            document.file.open('rb'),
            as_attachment=False,
            filename=smart_str(document.file.name),
            content_type=content_type
        )
        response['Content-Disposition'] = 'inline; filename="%s"' % smart_str(document.file.name)
        return response
    except Exception:
        raise Http404('File not found or inaccessible.')

@login_required
@user_passes_test(is_admin)
def view_document(request, doc_id):
    document = get_object_or_404(CompanyDocument, id=doc_id)
    ext = os.path.splitext(document.file.name)[1].lower()
    previewable = ext == '.pdf'
    preview_url = reverse('admin_dashboard:preview_document', args=[document.id])
    return render(request, 'admin_dashboard/view_document.html', {
        'document': document,
        'previewable': previewable,
        'preview_url': preview_url,
    })

@login_required
@user_passes_test(is_admin)
def folder_view(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    sort = request.GET.get('sort', 'date')
    if sort == 'name':
        documents = CompanyDocument.objects.filter(department=department).order_by('title')
    elif sort == 'oldest':
        documents = CompanyDocument.objects.filter(department=department).order_by('uploaded_at')
    else:
        documents = CompanyDocument.objects.filter(department=department).order_by('-uploaded_at')
    departments = Department.objects.all().order_by('name')
    return render(request, 'admin_dashboard/folder_view.html', {
        'department': department,
        'documents': documents,
        'departments': departments,
        'sort': sort,
    })

@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    sort = request.GET.get('sort', 'date')
    if sort == 'name':
        documents = CompanyDocument.objects.select_related('department').all().order_by('title')
    elif sort == 'oldest':
        documents = CompanyDocument.objects.select_related('department').all().order_by('uploaded_at')
    else:
        documents = CompanyDocument.objects.select_related('department').all().order_by('-uploaded_at')

    departments = Department.objects.annotate(doc_count=Count('companydocument')).order_by('name')
    folder_form = DepartmentForm()
    return render(request, 'admin_dashboard/dashboard_home.html', {
        'documents': documents,
        'departments': departments,
        'sort': sort,
        'folder_form': folder_form,
    })

@login_required
@user_passes_test(is_admin)
def create_folder(request):
    if request.method != 'POST':
        return redirect('admin_dashboard:dashboard_home')
    form = DepartmentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Folder created successfully.')
    else:
        messages.error(request, 'Unable to create folder. Please try again.')
    return redirect('admin_dashboard:dashboard_home')

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
            uploaded_count = 0
            for f in files:
                ext = os.path.splitext(f.name)[1].lower()
                if ext not in ['.pdf', '.doc', '.docx']:
                    messages.error(request, f'File {f.name} is not a PDF or Word document.')
                    continue
                CompanyDocument.objects.create(
                    title=form.cleaned_data['title'] or os.path.splitext(f.name)[0],
                    department=department,
                    file=f,
                    uploaded_by=request.user
                )
                uploaded_count += 1
            if uploaded_count:
                messages.success(request, f'{uploaded_count} document(s) uploaded successfully!')
            return redirect('admin_dashboard:dashboard_home')
    else:
        form = CompanyDocumentForm()
    departments = Department.objects.all().order_by('name')
    return render(request, 'admin_dashboard/upload_document.html', {
        'form': form,
        'departments': departments,
    })

@login_required
@user_passes_test(is_admin)
def move_document(request, doc_id):
    document = get_object_or_404(CompanyDocument, id=doc_id)
    if request.method == 'POST':
        form = DocumentMoveForm(request.POST, current_department=document.department)
        if form.is_valid():
            new_department = form.cleaned_data.get('new_department')
            target_department = form.cleaned_data.get('target_department')
            if new_department:
                target_department, _ = Department.objects.get_or_create(name=new_department)
            document.department = target_department
            document.save()
            messages.success(request, f'"{document.title}" moved to {target_department.name}.')
            return redirect('admin_dashboard:folder_view', dept_id=target_department.id)
    else:
        form = DocumentMoveForm(current_department=document.department)
    return render(request, 'admin_dashboard/move_document.html', {
        'document': document,
        'form': form,
    })

@login_required
@user_passes_test(is_admin)
def delete_document(request, doc_id):
    document = get_object_or_404(CompanyDocument, id=doc_id)
    if request.method == 'POST':
        department_id = document.department.id
        document.file.delete(save=False)
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('admin_dashboard:folder_view', dept_id=department_id)
    return render(request, 'admin_dashboard/delete_document.html', {
        'document': document,
    })

def scan_document(request, doc_id):
    messages.info(request, 'Scan feature coming soon!')
    return redirect('admin_dashboard:dashboard_home')
