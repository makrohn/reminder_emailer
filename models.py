from __future__ import unicode_literals

from django.db import models
import settings

# Create your models here.

class separated_employee(models.Model):
    """Some task that needs periodic reminder emails sent"""
    name = models.CharField(max_length=200)
    manager_email = models.CharField(max_length=200)
    set_date = models.DateTimeField('Task Initiated Date')
    def __str__(self):
        return self.task_name
    def first_reminder(self):
        return (self.set_date + datetime.timedelta(days=settings.first_reminder))
    def second_reminder(self):
        return (self.set_date + datetime.timedelta(days=settings.second_reminder))
    def third_reminder(self):
        return (self.set_date + datetime.timedelta(days=settings.third_reminder))