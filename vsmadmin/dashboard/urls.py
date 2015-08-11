from django.conf.urls import patterns,include,url
from dashboard import views
from .views import set_config

urlpatterns = patterns('',
                       url(r"^$", views.index, name="config"),
                       url(r"^setconfig/$", set_config, name="setconfig"),
                    )
