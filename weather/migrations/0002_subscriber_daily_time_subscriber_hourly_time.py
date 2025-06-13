from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='daily_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='hourly_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
