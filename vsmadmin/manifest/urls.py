from django.conf.urls import patterns,include,url
from manifest import views
from .views import set_cluster_basic_file,set_cluster_storage_file,set_cluster_profile_file,set_cluster_cache_file,set_cluster_settings_file

urlpatterns = patterns('',
                       url(r"^$", views.index, name="manifest"),
                       url(r"^set_cluster_basic_file/$", set_cluster_basic_file, name="set_cluster_basic_file"),
                       url(r"^set_cluster_storage_file/$", set_cluster_storage_file, name="set_cluster_storage_file"),
                       url(r"^set_cluster_profile_file/$", set_cluster_profile_file, name="set_cluster_profile_file"),
                       url(r"^set_cluster_cache_file/$", set_cluster_cache_file, name="set_cluster_cache_file"),
                       url(r"^set_cluster_settings_file/$", set_cluster_settings_file, name="set_cluster_settings_file"),
                    )
