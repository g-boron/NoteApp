# Generated by Django 4.0 on 2023-03-18 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_note_doc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='doc',
            new_name='files',
        ),
        migrations.RemoveField(
            model_name='note',
            name='img',
        ),
    ]
