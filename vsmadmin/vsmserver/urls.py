from django.conf.urls import patterns,include,url
from vsmserver import views

urlpatterns = patterns('',
                       url(r"^$", views.index, name="vsmserver"),
                    )
