# Generated by Django 3.2.9 on 2021-11-13 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sto',
            old_name='sto_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='sto',
            name='new_field',
        ),
    ]
