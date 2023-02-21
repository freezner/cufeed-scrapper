from django.urls import path
from collect import views

urlpatterns = [
    path('', view=views.collect_news, name='collect_news')
]