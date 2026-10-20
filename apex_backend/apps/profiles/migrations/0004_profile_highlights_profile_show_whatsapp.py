from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_is_online_profile_last_seen_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='highlights',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='profile',
            name='show_whatsapp',
            field=models.BooleanField(default=False),
        ),
    ]
