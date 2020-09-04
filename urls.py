from django.conf import urls
from .views import home,scrape,newslist
from django.urls import path

urlpatterns = [
    path('',scrape,name='scrape'),
    path('home',home),
    path('nhome',newslist),
]

