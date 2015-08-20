from django.conf.urls import patterns,include,url
from dashboard import views
from .views import init_files

urlpatterns = patterns('',
                       url(r"^$", views.index, name="config"),
                       url(r"^init_files/$", init_files, name="init_files"),
                    )
