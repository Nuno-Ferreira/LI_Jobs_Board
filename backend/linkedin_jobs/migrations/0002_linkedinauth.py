# Generated by Django 5.1.3 on 2024-12-12 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkedin_jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedinAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
