import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

binary = '/usr/bin/firefox'
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.log.level = "trace"
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, **kwargs):
        self.driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="/usr/local/bin/geckodriver")
        self.driver.implicitly_wait(3)
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        print('...................................')
        print(self.output_filename)
        print(self.query)
        urls = [
            'https://www.dentalspeed.com/buscar?palavra=elastico',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open(f"../media/{self.output_filename}", "w") as file:
            file.write('[')
            product_elements = response.selector.xpath(
                '//div[@id="prod-encontrados"]//div[contains(@class, "product-item")]').getall()
            for index, product in product_elements:
                json.dump({
                    'site': 'https://dentalspeed.com',
                    'name': product.xpath('//span[@class="product-name"]/text()').get(),
                    'link': product.xpath('//a/@href').get(),
                    'price': product.xpath('//span[@itemprop="price"]').get()})
                if index < len(product_elements) - 1:
                    file.write(',')
            file.write(']')
