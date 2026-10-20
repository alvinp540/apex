from django.contrib import admin
from .models import FraudLog, AuditLog, Opportunity

@admin.register(FraudLog)
class FraudLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'severity', 'is_resolved', 'created_at')
    list_filter = ('severity', 'is_resolved')

admin.site.register(AuditLog)
admin.site.register(Opportunity)
