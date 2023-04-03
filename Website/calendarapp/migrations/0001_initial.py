# Generated by Django 4.1.7 on 2023-03-26 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.formation')),
                ('salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.salle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
