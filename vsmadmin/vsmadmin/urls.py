from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
                        url(r"^$", include('dashboard.urls', namespace="cluster")),
                        url(r"^home/$", include('dashboard.urls', namespace="home")),
                        url(r"^manifest/$", include('manifest.urls', namespace="manifest")),
                       )

