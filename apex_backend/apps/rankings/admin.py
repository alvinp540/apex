from django.contrib import admin
from .models import Ranking

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'global_rank', 'profession_rank', 'rank_movement', 'last_updated')
    ordering = ('global_rank',)
