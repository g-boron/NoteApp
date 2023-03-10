# Generated by Django 4.1.7 on 2023-03-02 16:28

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('note_text', models.TextField()),
                ('add_date', models.DateTimeField(verbose_name='added date')),
                ('img', models.ImageField(blank=True, upload_to='images')),
                ('edit_dates', django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(blank=True, null=True, verbose_name='edit dates'), default=list, size=None)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
