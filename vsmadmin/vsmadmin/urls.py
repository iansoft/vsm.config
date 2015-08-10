from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
                        url(r"^$", include('cluster.urls', namespace="cluster")),
                        url(r"^cluster/$", include('cluster.urls', namespace="cluster")),
                        url(r"^server/$", include('vsmserver.urls', namespace="server")),
                       )

