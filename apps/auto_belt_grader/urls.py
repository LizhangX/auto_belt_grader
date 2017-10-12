from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^reg$', views.reg),
    url(r'^logout$', views.logout),
    url(r'^upload$', views.upload),
    url(r'^delete/(?P<upload_id>\d+)$', views.delete_upload),
    url(r'^analyze/(?P<upload_id>\d+)$', views.analyze)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)