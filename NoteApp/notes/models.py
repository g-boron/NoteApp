from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    note_text = models.TextField()
    add_date = models.DateTimeField('added date')

    def __str__(self):
        return self.title