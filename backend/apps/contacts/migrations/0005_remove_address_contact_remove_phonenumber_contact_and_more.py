# Generated by Django 4.2.16 on 2025-02-24 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_address_phonenumber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='contact',
        ),
        migrations.RemoveIndex(
            model_name='public_contact',
            name='contacts_pu_first_n_3d0dbc_idx',
        ),
        migrations.RemoveIndex(
            model_name='public_contact',
            name='contacts_pu_organiz_b194dd_idx',
        ),
        migrations.RenameField(
            model_name='public_contact',
            old_name='latest_editor_log',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='latest_editor',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='linkedin',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='public_contact',
            name='telegram',
        ),
        migrations.AddField(
            model_name='public_contact',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='public_contact',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='public_contact',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
