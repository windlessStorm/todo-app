from django.db import models

class Task(models.Model):
  title = models.TextField()
  description = models.TextField(blank=True, null=True)
  due_date = models.DateField()
  parent = models.ForeignKey('Task', null=True, related_name='subtasks', on_delete=models.SET_NULL)
  status = models.CharField(max_length = 10)
  soft_deleted = models.BooleanField(default=False)
  delete_time = models.DateField(null=True)

  class Meta:
    ordering = ["-due_date"]

  class Admin:
    pass