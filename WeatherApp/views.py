import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import City
# Create your views here.

from .forms import CityForm


def CityWeatherView(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=cbc6bf34a7e9e3a6e3d1bdc37ed9f80f"

    errmsg = ''
    msgclass = ''
    msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    errmsg = "The city is not in the world"
            else:
                errmsg = "Already city is added to database"
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg = "The city is successfully added in database"
            msgclass = 'is-success'

    form = CityForm()

    weather = []
    city = City.objects.all()
    for p in city:
        r = requests.get(url.format(p)).json()
        print(r)
        city_weather = {
            'city': p,
            'temparature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']

        }
        weather.append(city_weather)
        print(weather)

    context = {
        'weather': weather, 'form': form, 'msg': msg, 'msgclass': msgclass}
    return render(request, 'weather.html', context)


def City_delete(request, city_name):
    city = get_object_or_404(City, name=city_name)
    city.delete()
    return redirect('WeatherApp:city_weather')