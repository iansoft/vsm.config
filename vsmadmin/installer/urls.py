from django.conf.urls import patterns,include,url
from installer import views
urlpatterns = patterns('',
                       url(r"^$", views.index, name="installer"),
                    )
