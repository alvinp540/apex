from django.contrib import admin
from .models import VendorJob, VendorRating

@admin.register(VendorJob)
class VendorJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'profession_required', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority')

admin.site.register(VendorRating)
