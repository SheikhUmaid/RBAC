# Generated by Django 5.1.3 on 2024-11-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_rename_views_file_viewers_file_is_deleted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
            ],
        ),
    ]