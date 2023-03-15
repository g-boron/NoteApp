from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import os

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note', null=True)
    title = models.CharField(max_length=200)
    note_text = models.TextField()
    add_date = models.DateTimeField('added date', auto_now_add=True)
    img = models.ImageField(upload_to='images', blank=True)
    doc = models.FileField(upload_to='files', blank=True)
    edit_dates = ArrayField(
        models.DateTimeField('edit dates', blank=True, null=True),
        default=list,
    )

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.doc.name)