# Generated by Django 4.2 on 2023-08-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageRepoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_name', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=255)),
                ('repo_status', models.CharField(max_length=255)),
                ('repo_type', models.CharField(max_length=255)),
                ('repo_permission', models.CharField(max_length=255)),
                ('repo_url', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'image_repository',
            },
        ),
    ]
