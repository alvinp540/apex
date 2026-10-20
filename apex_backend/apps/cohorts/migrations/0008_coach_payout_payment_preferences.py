from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0007_whatsappinviterequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohortcoachassignment',
            name='payment_details_submitted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cohortcoachassignment',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('mpesa', 'M-Pesa'), ('bank_transfer', 'Bank transfer'), ('paypal', 'PayPal'), ('other', 'Other')], max_length=32),
        ),
        migrations.AddField(
            model_name='cohortcoachassignment',
            name='payment_note',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='cohortcoachassignment',
            name='payment_recipient',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='cohortcoachassignment',
            name='payout_status',
            field=models.CharField(choices=[('awaiting_details', 'Awaiting payment details'), ('details_submitted', 'Payment details submitted'), ('paid', 'Paid')], db_index=True, default='awaiting_details', max_length=32),
        ),
    ]
