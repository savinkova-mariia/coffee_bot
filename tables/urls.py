from django.conf.urls import url
from django.contrib import admin
from posts.views import index, tables


urlpatterns = [
    url(r'^$', index),
    url(r'^tables/(?P<slug>[^/]+)/$', tables),
    url(r'^admin/', admin.site.urls),
]
