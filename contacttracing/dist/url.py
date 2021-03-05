from . import views
import django.urls as urls
from django.urls import path,include
urlpatterns=[
path('',views.home,name='home'),
path('h',views.h,name='h'),
path('h1',views.h1,name='h1'),
path('h2',views.h2,name='h2'),
path('h3',views.h3,name='h3'),
path('h4',views.h4,name='h4'),
]