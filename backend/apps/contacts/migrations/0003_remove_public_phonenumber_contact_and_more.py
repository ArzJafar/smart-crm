# Generated by Django 4.2.16 on 2025-02-24 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_remove_extrafield_contact_remove_phonenumber_contact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='public_phonenumber',
            name='contact',
        ),
        migrations.DeleteModel(
            name='Public_ExtraField',
        ),
        migrations.DeleteModel(
            name='Public_PhoneNumber',
        ),
    ]
