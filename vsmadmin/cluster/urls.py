from django.conf.urls import patterns,include,url
from cluster import views

urlpatterns = patterns('',
                       url(r"^$", views.index, name="cluster"),
                    )
