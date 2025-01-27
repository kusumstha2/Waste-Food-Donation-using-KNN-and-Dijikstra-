from django.urls import path
from .views import search_recipients

urlpatterns = [
    path('search-recipients/', search_recipients, name='search_recipients'),
]

