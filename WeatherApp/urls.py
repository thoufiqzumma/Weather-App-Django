from django.urls import path
from .views import CityWeatherView, City_delete
app_name = 'WeatherApp'
urlpatterns = [
    path('', CityWeatherView, name='city_weather'),
    path('remove/<city_name>/', City_delete, name='city_remove')

]