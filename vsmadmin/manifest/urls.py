from django.conf.urls import patterns,include,url
from manifest import views
from .views import read_server_manifest
from .views import save_cluster_manifest
from .views import save_server_manifest
from .views import download_manifest_zip
urlpatterns = patterns('',
                       url(r"^$", views.index, name="manifest"),
                       url(r"^read_server_manifest/$", read_server_manifest, name="read_server_manifest"),
                       url(r"^save_cluster_manifest/$", save_cluster_manifest, name="save_cluster_manifest"),
                       url(r"^save_server_manifest/$", save_server_manifest, name="save_server_manifest"),
                       url(r"^download_manifest_zip/$", download_manifest_zip, name="download_manifest_zip"),
                    )
