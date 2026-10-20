from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('cohorts', '0008_coach_payout_payment_preferences')]

    operations = [
        migrations.AddField(model_name='cohortcoachassignment', name='eligibility_status', field=models.CharField(choices=[('valid', 'Valid'), ('invalid', 'Invalid')], db_index=True, default='invalid', max_length=12)),
        migrations.AddField(model_name='cohortcoachassignment', name='eligibility_reason', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='cohortcoachassignment', name='improvement_delta', field=models.DecimalField(decimal_places=2, default=0, max_digits=6)),
        migrations.AddField(model_name='cohortcoachassignment', name='follow_up_completed', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='cohortcoachassignment', name='deployment_eligible', field=models.BooleanField(default=False)),
    ]
