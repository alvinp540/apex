from django.contrib import admin
from .models import TrustScore, TrustScoreHistory

@admin.register(TrustScore)
class TrustScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'overall_merit_score', 'tier', 'last_calculated')
    list_filter = ('tier',)
    ordering = ('-overall_merit_score',)

admin.site.register(TrustScoreHistory)
