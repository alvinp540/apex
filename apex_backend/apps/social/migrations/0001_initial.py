from django.db import migrations, models
import django.db.models.deletion
import uuid


def seed_field_notes(apps, schema_editor):
    Post = apps.get_model('social', 'Post')
    Post.objects.bulk_create([
        Post(author_name='Field Notes', author_role='Future of work', topic='Capability', body='The strongest professional signal is not a single certificate. It is a visible pattern of practice, feedback, and improvement.', source_name='World Economic Forum', source_url='https://www.weforum.org/publications/the-future-of-jobs-report-2025/'),
        Post(author_name='Field Notes', author_role='Learning science', topic='Learning', body='Deliberate practice works best when a person can see the gap, try again, and measure the change.', source_name='Harvard Business Review', source_url='https://hbr.org/2019/10/the-right-way-to-develop-your-talent'),
        Post(author_name='Field Notes', author_role='Professional growth', topic='Opportunity', body='A career compounds when each project leaves behind evidence that makes the next conversation more concrete.', source_name='MIT Sloan Management Review', source_url='https://sloanreview.mit.edu/'),
    ])


class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author_name', models.CharField(default='Apex Field Notes', max_length=120)),
                ('author_role', models.CharField(default='Capability research', max_length=120)),
                ('body', models.TextField()),
                ('source_url', models.URLField(blank=True)),
                ('source_name', models.CharField(blank=True, max_length=120)),
                ('topic', models.CharField(default='Capability', max_length=80)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_posts', to='accounts.user')),
            ],
            options={'db_table': 'social_posts', 'ordering': ('-created_at',)},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_comments', to='accounts.user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social.post')),
            ],
            options={'db_table': 'social_comments', 'ordering': ('created_at',)},
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='social.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_likes', to='accounts.user')),
            ],
            options={'constraints': [models.UniqueConstraint(fields=('post', 'user'), name='unique_social_post_like')]},
        ),
        migrations.RunPython(seed_field_notes, migrations.RunPython.noop),
    ]
