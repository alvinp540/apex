from django.db import models
import uuid
from apps.accounts.models import User


class Ranking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking')
    profession = models.CharField(max_length=100, db_index=True)
    global_rank = models.PositiveIntegerField(null=True, db_index=True)
    profession_rank = models.PositiveIntegerField(null=True, db_index=True)
    country_rank = models.PositiveIntegerField(null=True)
    previous_global_rank = models.PositiveIntegerField(null=True)
    rank_movement = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rankings'
        indexes = [models.Index(fields=['profession', 'profession_rank'])]
