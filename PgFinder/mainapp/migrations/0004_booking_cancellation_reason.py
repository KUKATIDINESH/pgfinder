from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_booking_bookingreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancellation_reason',
            field=models.TextField(blank=True),
        ),
    ]
