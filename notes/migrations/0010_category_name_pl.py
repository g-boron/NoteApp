# Generated by Django 4.0 on 2023-09-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_reminder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_pl',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
