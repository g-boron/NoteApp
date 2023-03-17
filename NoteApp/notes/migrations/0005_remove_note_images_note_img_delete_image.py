# Generated by Django 4.0 on 2023-03-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_image_remove_note_img_alter_note_add_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='images',
        ),
        migrations.AddField(
            model_name='note',
            name='img',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]