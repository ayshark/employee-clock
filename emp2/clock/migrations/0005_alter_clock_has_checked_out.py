# Generated by Django 4.1.5 on 2023-01-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0004_alter_clock_has_checked_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clock',
            name='has_checked_out',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
