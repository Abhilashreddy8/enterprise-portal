# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):

    title = models.CharField(max_length=200)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    #file = models.FileField(upload_to='reports/')
    file = models.FileField(upload_to='reports/', null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50,
        default="Processing"
    )

    def __str__(self):
        return self.title