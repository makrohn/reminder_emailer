from __future__ import unicode_literals

from django.db import models
import settings
import datetime

# Create your models here.

class separatedEmployee(models.Model):
    """Some task that needs periodic reminder emails sent"""
    name = models.CharField(max_length=200)
    manager_email = models.CharField(max_length=200)
    set_date = models.DateField('Task Initiated Date')
    def __str__(self):
        return self.name