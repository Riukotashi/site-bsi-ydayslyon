# Generated by Django 3.2.8 on 2021-10-27 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageldapusers', '0003_auto_20211025_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ldapuser',
            old_name='isActivated',
            new_name='isValidated',
        ),
        migrations.RemoveField(
            model_name='ldapuser',
            name='isValid',
        ),
    ]
