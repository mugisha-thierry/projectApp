from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('signup/',views.signup , name='signup'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)