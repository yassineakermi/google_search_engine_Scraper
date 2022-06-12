import json
import urllib.parse
import requests
import scrapy
from google_search_engine.items import GoogleSearchEngineItem
from scrapy.http import JsonRequest
from datetime import datetime
from scrapy.selector import Selector
class GoogleSpider(scrapy.Spider):
    name = 'Google'
    allowed_domains = ['google.com']
    def __init__(self, keyword=None, id=None, language=None, country=None, *args, **kwargs):
        self.country = "&cr=country"+country.upper() if country else ""
        self.language = "&lr=lang_"+language.lower() if language else ""
        self.keyword = urllib.parse.quote_plus(keyword)
        self.id=id
        self.scrapfly_token=""
        super(GoogleSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        url=f"https://www.google.com/search?q={self.keyword}{self.country}{self.language}"
        print(url)
        yield JsonRequest(url=f"https://api.scrapfly.io/scrape?key={self.scrapfly_token}&url={url}", callback=self.parse)    

    def parse(self, response):
        json_resp = json.loads(response.text)
        html_body = json_resp['result']['content']
        results = Selector(text=html_body).xpath('//br/ancestor::a[@data-ved]')
        second_version = False
        if(len(results) <= 0):
            results = response.xpath('//div[contains(@class,"ZINbbc")]//a[contains(@href,"/url?")]/h3')
            second_version = True
        questions = []
        search_results = []
        for index,result in enumerate(results,start=1):
            heading = result.xpath('.//text()').get()
            link =  result.xpath('./@href').get() if(not second_version) else result.xpath('./ancestor::a[contains(@href,"/url?")]/@href').get()
            item = GoogleSearchEngineItem()
            item['title'] = heading
            item['link'] = link
            item['keyword']=self.id
            item['createdAT']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['rank']=index

            if(result.xpath('./ancestor::div[contains(@id,"RELATED_QUESTION_LINK")]')):
                item['resultType']="QUESTION"
                questions.append(item)
                yield 
            else:
                item['resultType']="SEARCH_RESULT"
                search_results.append(item)

            yield item
    def closed(self,reason):
        url = f"http://localhost:3001/update_keyword/{self.id}"

        response = requests.request("GET", url)

        print(response.text)
