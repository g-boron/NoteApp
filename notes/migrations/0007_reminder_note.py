# Generated by Django 4.0 on 2023-07-07 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='note',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='notes.note'),
            preserve_default=False,
        ),
    ]