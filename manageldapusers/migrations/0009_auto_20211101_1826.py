# Generated by Django 3.2.8 on 2021-11-01 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageldapusers', '0008_alter_ldapuser_classname'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldapuser',
            name='date_activation_token',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ldapuser',
            name='date_validation_token',
            field=models.DateTimeField(null=True),
        ),
    ]
