from django.conf.urls import patterns,include,url
from manifest import views
from .views import set_cluster_basic_file

urlpatterns = patterns('',
                       url(r"^$", views.index, name="manifest"),
                       url(r"^set_cluster_basic_file/$", set_cluster_basic_file, name="set_cluster_basic_file"),
                    )
