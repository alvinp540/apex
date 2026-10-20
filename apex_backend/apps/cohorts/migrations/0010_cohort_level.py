from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('cohorts', '0009_coach_assignment_eligibility')]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], db_index=True, default='beginner', max_length=20),
        ),
    ]