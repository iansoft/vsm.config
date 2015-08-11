from django.conf.urls import patterns,include,url
from manifest import views

urlpatterns = patterns('',
                       url(r"^$", views.index, name="manifest"),
                    )
