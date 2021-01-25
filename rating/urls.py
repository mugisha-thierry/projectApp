from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('signup/',views.signup , name='signup'),
    path('profile/<username>/', views.profile, name='profile'),
    path('search',views.search_project,name = 'search_project'),
    path('project/<id>',views.project, name='project'),
    url(r'^api/profiles/$', views.ProfileList.as_view(), name='profile'),
    url(r'^api/projects/$', views.ProjectList.as_view(), name ='project'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)