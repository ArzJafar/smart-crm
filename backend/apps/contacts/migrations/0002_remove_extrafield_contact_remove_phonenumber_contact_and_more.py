# Generated by Django 4.2.16 on 2025-02-23 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrafield',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='contact',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='ExtraField',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
