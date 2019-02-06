from django.urls import path
from home.views import HomeListView, add_games,delete_all


app_name = 'home'


urlpatterns = [
    path('update/', add_games, name='update'),
    path('delete/', delete_all, name='delete'),
    path('', HomeListView.as_view(), name='index')
]
