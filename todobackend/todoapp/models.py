# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

PENDING = 'Pending'
COMPLETED = 'Completed'
STATUS = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    )

class Task(models.Model):
  title = models.CharField(max_length=250)
  description = models.TextField(blank=True)
  due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
  parent = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
  status = models.CharField(
    max_length=10, 
    choices=STATUS, 
    default=PENDING
  )
  soft_deleted = models.BooleanField(default=False)
  delete_time = models.DateField(null=True, blank=True)

  def __str__(self):
    return self.title

  def __unicode__(self):
    return u'{.title}'.format(self)

  def to_json(self):
        return {
            'id': self.pk,
            'title': self.title,
            'due_date': self.due_date,
            'status': self.status
        }

  # This is to allow adding null values from django admin, https://stackoverflow.com/questions/6993780/how-can-i-allow-django-admin-to-set-a-field-to-null
  def save(self, *args, **kwargs):
        if not self.delete_time:
            self.delete_time = None
        if not self.parent:
            self.parent = None
        super(Task, self).save(*args, **kwargs)

  class Meta:
    ordering = ["-due_date"]

  class Admin:
    pass