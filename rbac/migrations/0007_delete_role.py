# Generated by Django 5.1.3 on 2024-11-28 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]
