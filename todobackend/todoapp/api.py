from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from todoapp.custom_filter import ModelResourceCustom, duedate_range_filter
from tastypie.authorization import Authorization
from todoapp.models import Task
from tastypie.constants import ALL
from tastypie import fields

class TaskResource(ModelResource):
  parent = fields.ForeignKey('todoapp.api.TaskResource', attribute = 'parent', null=True, full=True)
  class Meta:
    resource_name = 'task'
    queryset = Task.objects.exclude(soft_deleted=True)
    limit = 0
    allowed_methods = ['get', 'post', 'put']
    authorization = Authorization()

    # Responses will be ordered by ascending due date
    ordering = ['due_date']

    # Will allow for filtering tasks which are due today, this week, next week or overdue.
    # Also will allow us to search by title
    filtering = { 
          'due_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
          'title': ALL
        }

class SubTaskResource(ModelResource):
    subtasks = fields.ToManyField('todoapp.api.TaskResource', attribute=lambda bundle: Task.objects.filter(parent=bundle.obj, soft_deleted=False), null=True, blank=True, full=True)
    class Meta:
        resource_name = 'subtasks'
        queryset = Task.objects.exclude(soft_deleted=True)
        allowed_methods = ['get']
        filtering = {
            "subtasks": ALL_WITH_RELATIONS
        }
        ordering = ['due_date']

class FilteredResource(ModelResourceCustom):
    class Meta:
        resource_name = 'filter'
        queryset = Task.objects.exclude(soft_deleted=True)
        allowed_methods = ['get']
        filtering = {
            "during":ALL,
        }
        custom_filters = duedate_range_filter
        ordering = ['due_date']

class DeleteTaskResource(ModelResource):
    class Meta:
        resource_name = 'delete'
        queryset = Task.objects.exclude(soft_deleted=False)
        allowed_methods = ['get', 'delete']
        authorization = Authorization()
        filtering = {
            "delete_time":['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        ordering = ['due_date']