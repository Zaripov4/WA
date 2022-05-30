import requests
from django.shortcuts import render


def get_html(city):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 " \
                 "Safari/537.36 "
    language = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = user_agent
    session.headers['Accept-Language'] = language
    session.headers['Content-Language'] = language
    city = city.replace(' ', '+')
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):
    result = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_html(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        result['time'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
    return render(request, 'temp/home.html', {'result': result})
