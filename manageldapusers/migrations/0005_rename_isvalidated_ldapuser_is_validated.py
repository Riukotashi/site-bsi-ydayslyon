# Generated by Django 3.2.8 on 2021-10-27 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageldapusers', '0004_auto_20211027_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ldapuser',
            old_name='isValidated',
            new_name='is_validated',
        ),
    ]