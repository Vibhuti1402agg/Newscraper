from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

requests.packages.urllib3.disable_warnings()

from datetime import timezone, datetime,timedelta
from .models import Headlines, Userprofile
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os


def home(request):
    return HttpResponse('home')

def newslist(request):
    user_p=Userprofile.objects.filter(user=request.user).first()
    now=datetime.now(timezone.utc)
    time_difference=now-user_p.last_scrape


    headlines=Headlines.objects.all()
    return render(request,'home.html',{'news':headlines})

def scrape(request):
    user_p=Userprofile.objects.filter(user=request.user).first()
    user_p.last_scrape=datetime.now(timezone.utc)
    user_p.save

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

    url = "https://www.theonion.com/latest"
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, 'html.parser')
    posts = soup.find_all('div', {'class': 'cw4lnv-11 hDSSIi'})


    for i in posts:
        link = i.find_all('a', {'class': 'js_link sc-1out364-0 fwjlmD'})[1].get('href')
        title = i.find_all('a', {'class': 'js_link sc-1out364-0 fwjlmD'})[1].text
        image_source=i.find('div', {'class': ['js_lazy-image sc-1xh12qx-2 kgfyHI']}).img.get('srcset')

        def download_image(image_source):
            local_filename = image_source.split('/')[-1].split("?")[0]

            r = session.get(image_source, stream=True, verify=False)
            with open('media', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            return local_filename

        if not image_source.startswith(("data:image", "javascript")):
                image_source=download_image(image_source)


        new_headline = Headlines
        new_headline.title = title
        new_headline.url = link
        new_headline.image=image_source
        new_headline.save


    return redirect(home)

