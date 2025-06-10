import scrapy
from oliv.items import Product
from lxml import html
import urllib.parse
from datetime import date
class OlivSpider(scrapy.Spider):
    name = "oliv"
    # start_urls = ["https://example.com"]
    
    def start_requests(self):
        yield scrapy.Request(
            url='https://oliv.com/',  # Or any start URL
            callback=self.parse
        )

    def parse(self, response):
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://oliv.com',
            'Referer': 'https://oliv.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        data = '{"requests":[{"indexName":"production_CandidatesByLoggedInAtDesc","params":"query=nayana&hitsPerPage=9&maxValuesPerFacet=1000&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&filters=&facets=%5B%22city%22%2C%22visaStatus%22%2C%22majors.name%22%2C%22countryOfResidence%22%2C%22languages%22%2C%22degrees%22%2C%22universities%22%2C%22interestedIn%22%2C%22nationality%22%2C%22gender%22%2C%22ageGroup%22%2C%22hasVideoCv%22%2C%22driversLicence%22%5D&tagFilters="}]}'
        import chompjs
        import pandas as pd

        df = pd.read_csv('profiles.csv').to_dict('records')
        for i in df:
            json_data = chompjs.parse_js_object(i.get('pipl'))
            # print(json_data.get('search_term'), i.get('customer_name'))
            data.replace('nayana', f'{json_data.get('customer_name')}')
            yield scrapy.Request(
                url='https://7434lfw3po-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.29.0%3Breact%20(16.14.0)%3Breact-instantsearch%20(5.7.0)%3BJS%20Helper%202.26.1&x-algolia-application-id=7434LFW3PO&x-algolia-api-key=b1e68d317c29aa5783f657cd19f8e64d',
                method='POST',
                headers=headers,
                body=data,
                callback=self.parse_results
            )
            # break

    def parse_results(self, response):
        try:
            items = response.json().get('results', [])[0].get('hits', [])
        except Exception as error:
            print(error)
            items = []
        for item in items:
            url_slug = item.get('id', '')
            first_name = item.get('firstName', '')
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMWYwNDViYS1jZDE4LTcwZDAtYjcwMS1mMTUwMGE1ZDY1MDMiLCJpYXQiOjE3NDk1MzI5MzZ9.LzBZQZzDq2OhYYr1qSIPZToXWacAxlFtOY4Z8n3ZyzE',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://oliv.com/employer/candidate/11efc8ef-d148-73a0-973d-df0946b48abd',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
            }
            params = {
                'filter[include][0]': 'certificates',
                'filter[include][1]': 'education',
                'filter[include][2]': 'skills',
                'filter[include][3]': 'experience',
                'filter[include][4]': 'links',
                'filter[include][5]': 'interests',
                'filter[include][6]': 'languages',
                'filter[include][7]': 'files',
                'filter[include][8]': 'industries',
                'filter[include][9]': 'highSchoolLevelEducation',
            }
            headers['Referer'] = f'https://oliv.com/api/v1/candidates/{url_slug}'
            query_string = urllib.parse.urlencode(params, doseq=True)
            full_url = f'https://oliv.com/api/v1/candidates/{url_slug}?{query_string}'
            yield scrapy.Request(
                # url=f'https://oliv.com/api/v1/candidates/{url_slug}',
                url=full_url,
                headers=headers,
                # params=params,
                callback=self.parse_data
            )
    def parse_data(self, response):
        scrape_date = date.today()
        yield Product(
            **{
                'data': str(response.json()),
                'scrape_date': str(scrape_date)
                }
            )