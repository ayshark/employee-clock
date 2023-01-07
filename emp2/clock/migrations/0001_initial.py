# Generated by Django 4.1.5 on 2023-01-04 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('checkin', models.DateTimeField(auto_now_add=True)),
                ('checkout', models.DateTimeField(blank=True)),
                ('has_checked_out', models.BooleanField(blank=True, default=False, null=True)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clock.employee')),
            ],
        ),
    ]
