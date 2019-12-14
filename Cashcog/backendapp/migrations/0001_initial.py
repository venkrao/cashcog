# Generated by Django 3.0 on 2019-12-14 14:55

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('currency', models.CharField(max_length=5)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendapp.Employee')),
            ],
        ),
    ]
