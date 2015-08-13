from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
                        url(r"^$", include('dashboard.urls', namespace="dashboard")),
                        url(r"^config/", include('dashboard.urls', namespace="config")),
                        url(r"^manifest/", include('manifest.urls', namespace="manifest")),
                       )

