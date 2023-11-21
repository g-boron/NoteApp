from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
import os
from django.utils.translation import get_language


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    name_pl = models.CharField(max_length=200, default='none')
    slug = models.SlugField()

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            return self.name
        elif lang == 'pl':
            return self.name_pl

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note', null=True)
    title = models.CharField(max_length=200)
    note_text = models.TextField()
    add_date = models.DateTimeField('added date', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=7)
    edit_dates = ArrayField(
        models.DateTimeField('edit dates', blank=True, null=True),
        default=list,
    )
    edit_authors = ArrayField(
        models.CharField(max_length=200),
        default=list,
    )
    members = ArrayField(
        models.CharField(max_length=200)
    )
    allow_edits = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files', blank=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    message_pl = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


class Reminder(models.Model):
    title = models.CharField(max_length=250)
    remind_date = models.DateTimeField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
