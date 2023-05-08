from django.urls import path
from cufeedScrapper import views

urlpatterns = [
    path('api/<site>/<keyword>', views.collect_news)
]