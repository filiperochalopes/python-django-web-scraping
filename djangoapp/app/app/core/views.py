from django.contrib.auth.models import User, Group
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.core.serializers import UserSerializer, GroupSerializer

import requests
from bs4 import BeautifulSoup
from pprint import pprint

import os
import json
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import rpa as r


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_google(request, query):
    # https://www.dentalspeed.com/buscar?palavra=elastico e
    URL = f'https://www.dentalspeed.com/buscar?palavra={query}'
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'parser.html')
    results = soup.find(id='product-items')
    products = []
    product_elements = results.find_all('div', class_='product-item')
    for product_element in product_elements:
        name = product_element.find(
            'strong', class_='product-item-name').fin('a')
        print(name.text)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalspeed_selenium(request, query):
    # https://www.dentalspeed.com/buscar?palavra=elastico e
    URL = f'https://www.dentalspeed.com/buscar?palavra={query}'

    binary = '/usr/bin/firefox'
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.log.level = "trace"
    options.binary = binary
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = True

    res = []
    driver = webdriver.Firefox(
        firefox_options=options, capabilities=cap, executable_path="/usr/local/bin/geckodriver")
    print('Acessando a página')

    wait = WebDriverWait(driver, 30)
    print(driver.execute_script("return document.readyState"))
    element = wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    print('Página carregada')
    # driver.implicitly_wait(5)
    driver.get(URL)
    products = driver.find_elements_by_xpath(
        '//div[@id="prod-encontrados"]//div[contains(@class, "product-item")]')

    for product in products:
        print(product.find_element_by_xpath(
            './/span[contains(@class, "product-name")]').text)
        print(product.find_element_by_xpath('.//span[@itemprop="price"]').text)
        res.append({
            'site': 'https://dentalspeed.com',
            'name': product.find_element_by_xpath('.//span[contains(@class, "product-name")]').text,
            'link': product.find_element_by_xpath('.//a').get_attribute('href'),
            'price': product.find_element_by_xpath('.//span[@itemprop="price"]').text
        })
    pprint(res)
    time.sleep(1)

    return Response(res)
    # return Response(obj)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalspeed_scrapy(request, query):
    # https://www.dentalspeed.com/buscar?palavra=elastico e
    # URL = f'https://www.dentalspeed.com/buscar?palavra={query}'

    get = os.system(
        f'cd app/scrapyapp && pwd && scrapy crawl quotes -a output_filename=tmp.json -a query="{query}"')

    text = open(os.path.join(settings.MEDIA_ROOT, 'tmp.json'), 'rb').read()

    obj = json.loads(text)
    pprint(obj)

    return Response({'message': 'hello world'})
    # return Response(obj)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalspeed_rpa(request, query):
    # https://www.dentalspeed.com/buscar?palavra=elastico e
    # URL = f'https://www.dentalspeed.com/buscar?palavra={query}'

    r.init()
    r.url('https://www.google.com')
    r.type('//*[@name="q"]', 'decentralization[enter]')
    print(r.read('result-stats'))
    r.snap('page', 'results.png')
    r.close()

    return Response({'message': 'hello world'})
    # return Response(obj)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scraping_dentalcremer(request, query):
    URL = f'https://www.dentalcremer.com.br/chaordic/search/result/?origin=autocomplete&ranking=1&terms=+elastico&apikey=dentalcremer-v8&topsearch=1&q={query}'
    res = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('ol', class_='product-items')
    products = []
    product_elements = results.find_all('div', class_='product-item')
    for product_element in product_elements:
        site = 'https://www.dentalcremer.com.br'
        name = product_element.find(
            'strong', class_='product-item-name').find('a')
        link = name['href']
        price = product_element.find('span', class_='price')
        res.append({
            "site": site,
            "name": name.text,
            "link": link,
            "price": price.text
        })

    return Response(res)
