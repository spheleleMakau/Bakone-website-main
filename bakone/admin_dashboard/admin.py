from django.contrib import admin
from .models import CompanyDocument

@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'uploaded_by')
    search_fields = ('title', 'uploaded_by__username')
