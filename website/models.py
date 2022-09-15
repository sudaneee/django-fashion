from audioop import maxpp
from django.db import models

class Picture(models.Model):
    tag = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return self.tag