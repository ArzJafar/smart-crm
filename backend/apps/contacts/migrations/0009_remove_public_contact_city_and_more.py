# Generated by Django 4.2.16 on 2025-03-17 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_rename_email_public_contact_mobile_number_1_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='public_contact',
            name='city',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='province',
        ),
    ]
