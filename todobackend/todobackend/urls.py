from django.contrib import admin
from django.conf.urls import include, url
from tastypie.api import Api
from todoapp.api import TaskResource, FilteredResource, DeleteTaskResource, SubTaskResource
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(FilteredResource())
v1_api.register(SubTaskResource())
v1_api.register(DeleteTaskResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
]

urlpatterns += staticfiles_urlpatterns()
