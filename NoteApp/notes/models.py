from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.name

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
    members = ArrayField(
        models.CharField(max_length=200)
    )

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
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
