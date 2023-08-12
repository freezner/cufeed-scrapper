from django.urls import path
from cufeedScrapServer import views

urlpatterns = [
    path('api/<site>/<keyword>', views.collect_news)
]