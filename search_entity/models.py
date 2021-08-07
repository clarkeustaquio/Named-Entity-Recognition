from django.db import models

# Create your models here.

class PDF(models.Model):
    file_name = models.TextField()
    file = models.FileField(default=None, upload_to='pdf_collection')
    entity = models.JSONField(default=list)

    def __str__(self):
        return self.file_name