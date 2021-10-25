# Generated by Django 3.2.7 on 2021-10-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageldapusers', '0002_rename_isvalide_ldapuser_isvalid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldapuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ldapuser',
            name='classname',
            field=models.CharField(choices=[('toto', 'tata'), ('LIM', 'LIMART'), ('ING', 'Ingesup'), ('ANIM', 'Animation'), ('ISEE', 'ISEE'), ('AUDIO', 'Audiovisuel')], max_length=255),
        ),
    ]