from django.shortcuts import render,redirect,Http404
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages
# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing = City.objects.filter(name = new_city).count()

            if existing == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                    messages.success(request,'City added succesfully!')
                else:
                    messages.warning(request,'City does not exist in the world!')
            else:
                messages.warning(request,'City already exists!')
    form = CityForm()
    cities = City.objects.all().order_by('-created')
    weather_data = []
    for city in cities:
        f = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : f['main']['temp'],
            'description' : f['weather'][0]['description'],
            'icon' : f['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' : weather_data, 
        'form' : form,
    }

    
    return render(request,'weather/weath.html',context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
