from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from todoapp.models import Task
from tastypie.constants import ALL
from tastypie import fields

class TaskResource(ModelResource):
  parent = fields.ForeignKey('todoapp.api.TaskResource', attribute = 'parent', null=True)
  class Meta:
    queryset = Task.objects.all()
    resource_name = 'task'
    allowed_methods = ['get', 'post', 'put']
    authorization = Authorization()

    # No need to send deletion status
    # excludes = ['soft_deleted', 'delete_time']
    
    # Responses will be ordered by ascending due date
    ordering = ['due_date']

    # Will allow for filtering tasks which are due today, this week, next week or overdue.
    # Also will allow us to search by title
    filtering = { 
          'due_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
          'title': ALL
        }