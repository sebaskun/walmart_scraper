import scrapy
import re, ast, json, copy, html
from scrapers.items import ProductItem
import http.client 

class CaWalmartSpider(scrapy.Spider):
    name = "ca_walmart"
    allowed_domains = ["walmart.ca"]
    # start_urls = ["https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852",
    # "https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852/page-2"]
    base_url = "https://www.walmart.ca"
    headers = {
        'dnt': '1',
        'authority': 'www.walmart.ca',
        'method': 'GET',
        'path': '/en/grocery/fruits-vegetables/fruits/N-3852',
        'scheme': 'https',
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,es;q=0.9',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': None,
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': 1,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'referer': 'https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852',
        }

    cookies = {
        'walmart.shippingPostalCode':'P7B3Z7',
        'defaultNearestStoreId':'3124',
        'zone':9,
        'deliveryCatchment':3124,
        'walmart.csrf':'73996cac34766ec995777784',
        'wmt.c':0,
        'vtc':'ZAUFmHNTbFPrWyLrN8WTXA',
        'userSegment':'50-percent',
        'TBV':7,
        'rxVisitor':'1590552903550G5KJVCBIUCN3R32E3OSSVIKN9FTMDI5M',
        'dtSa':'-',
        '_ga':'GA1.2.1363574403.1590552905',
        '_gid':'GA1.2.85728116.1590552905',
        'walmart.id':'24be2423-225b-44d0-851c-9f83c8e47dff',
        'usrState':1,
        'walmart.nearestPostalCode':'P7B3Z7',
        's_ecid':'MCMID%7C17236695788713957075642593017320325404',
        'walmart.locale':'en',
        'AMCVS_C4C6370453309C960A490D44%40AdobeOrg':1,
        's_visit':1,
        's_cc':'true',
        'og_session_id':'af0a84f8847311e3b233bc764e1107f2.616221.1590552906',
        'og_session_id_conf':'af0a84f8847311e3b233bc764e1107f2.616221.1590552906',
        '_gcl_au':'1.1.482108716.1590552907',
        '_fbp':'fb.1.1590552907225.702607671',
        'og_autoship':0,
        'dtCookie':'3$1GS1LRIIKIBM595EBN2HIHIPCU4QVQ3H|5b6d58542e634882|0',
        'walmart.nearestLatLng':"48.4120872,-89.2413988",
        'dtLatC':3,
        'rxVisitor':'1590552903550G5KJVCBIUCN3R32E3OSSVIKN9FTMDI5M',
        'dtSa':'-',
        'DYN_USER_ID':'23c3e447-cab5-4a76-beec-86d431f09b30',
        'WM_SEC.AUTH_TOKEN':'MTAyOTYyMDE46M9ya4OWOAX9Ycj9G+/EtZZ2rrXYDwJUPMuf8aNPxGq6es3kBtQx/WxiXKAkaKfkoKbMqixeQFrYdB1W0oSN1wIIzkNIxIEmVq7cOUtRuTRSgSwdxAsAWBT8plmFWLKwj8OFN4dileb20bpDLeCIlSFd/Hsc7bnSe4+TLU2zbj06SQbscc1R1tIesXl4ioL4y1NvN1BBj6GkfAZCjCfhDTASAGkrw9upmzYhCz4UwRzb/SoGFgAYL9DGZ8K45WCXb/Ew67/GsLtdlJHpe1JgEG+jVJ7bQ3VTYSMGmHEYCS8c8IAFKTMeYOPXxSWUpSrKtEbQ9hG+J0B2+kHzA8jyKD+vhACQYbIqsOCISVNY3spUIeGCIOmGJLznpUXbYF3gVk3LktwueMY7RuHPZ68PyA==',
        'LT':'1590553091850',
        'BVImplmain_site':2036,
        'BVBRANDID':'20ae010b-0053-4a9f-902a-9197d72dc542',
        'DYN_USER_ID.ro':'23c3e447-cab5-4a76-beec-86d431f09b30',
        'cartId':'b6eb398f-ed49-46e8-8034-af8da418dd90',
        'NEXT_GEN.ENABLED':1,
        '_pin_unauth':'NTY4YjUyZDctYzNmOC00NzA5LWExOTYtOWQxOWZlOWVkYjFi',
        'TS011fb5f6':'01c5a4e2f941ffc623122b68eca74f3a27e0c416f7e2a5707b9417a73c048cb4be6507e9fd51df79c8015b3ba420dc6643bb0f8309',
        'TS0175e29f':'01c5a4e2f941ffc623122b68eca74f3a27e0c416f7e2a5707b9417a73c048cb4be6507e9fd51df79c8015b3ba420dc6643bb0f8309',
        'authDuration':{"lat":"1590555466230000","lt":"1590555466230000"},
        'headerType':'grocery',
        's_sq':'%5B%5BB%5D%5D',
        'previousBreakpoint':'desktop',
        'wmt.breakpoint':'d',
        'akaau_P1':'1590607795~id=484ae7f711ac9dd38dbda655bd6ca764',
        'TS01f4281b':'01c5a4e2f97a7d51551a734ebe2cb1fc4f7a86c4df28824fb5812f83c96f6df870698b389077cf6f5fd822d05324df82b802c7ad04',
        '_uetsid':'2127b16a-c523-20a6-d801-43923775d65e',
        '_derived_epik':'dj0yJnU9NC1yUFlPMF9IczhrTlFabmZpYWVTQ0NMZFl5blN2eEMmbj1wX2o0OFVpeUZLWjRUcGM3Rl9xaGFnJm09MSZ0PUFBQUFBRjdPdXpJJnJtPTEmcnQ9QUFBQUFGN091ekk',
        'dtPC':'3$6637950_447h-vAKCBSUJVQJIVFIAUKQCIVTJULXFWHTFQ-0',
        'rxvt':'1590610238206|1590608438206',
        's_gnr':'1590609571427-Repeat',
        'AMCV_C4C6370453309C960A490D44%40AdobeOrg':'-408604571%7CMCIDTS%7C18410%7CMCMID%7C17236695788713957075642593017320325404%7CMCAID%7CNONE%7CMCOPTOUT-1590616771s%7CNONE%7CvVersion%7C4.6.0',
        '_4c_':'rVJNbxoxEP0rkQ85sbv%2BXHuRooqkUdWqSZQmVY%2FIeL1gZWGRbdimEf89YyCQNqnUQzmYnfF7M5437wn1M7tAQyIqXOJKKEIIH6AH%2BxjQ8AmZZTrX6Vj5Fg3RLMZlGBZF3%2Fd5r9u59jE3urCLYuo7Y%2F1j0fiViyFb26mNetLasM8U1xlTgqIBMl1toRSpcpULiOMviDKGMXwvfVevTBzHx2XC9HZyEuoHuKjt2hk77l0dZ1syxcfszLrpLKY0Vtv00kOAc5nK925Rd%2F2BSUWJj9kjk%2FH0tonv%2BmAT%2B2Lmu7k9UQSyHYiBfmwZAUJvG%2Bv9FvU%2F9Agubmc90Pc5WAKkIbi5uv82Pr8cXdxcv2rZzRcurrzNQmhf954UIRT93Bm90LVOghak%2BHKX0ZziHGdfR3eqCIxgQZVUmNCSVx9Gt%2Bdn5HTu6jMiKSvLSkilJGHwj6UoORUVw0QyihkVHPPT0e3lWVJmCd5ASeW2M7pNY4CbBujTaPz988etrCUTknPM8mQxISgcLyNdXeww%2F9QSSPfeTafWX9k462og3ntdu%2Bi6hW7T0sHGYIhGr9qYwrRV0%2BoQnKlteIjdEm0G6Ofe61AcWjEJ9otgbFVynH6A8K7emx5Z1kwaymRGqagzXpY001KxTHJdlsLYpqyTCLuailFVYYkrstnpsq0hji1ZxSXH6p2WO9f9nVPxtxyYdA9nb%2BDiHfjiZaijRId3w7OBVQLMvaD0H%2FeCKZXE6feAw4USQv0OTRmArg%2B1aNVII7XMYPgq48aYTBtNM6Mbogzs2AqBjkNgxWGOqtwPQdRuhs3mGQ%3D%3D'
    }

    def start_requests(self):
        url = 'https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852'

        yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        pages = response.css('.page-select-list a::text').getall()
        for page in pages:
            page_url = 'https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852/page-%s' % (page)
            yield scrapy.Request(url=page_url, headers=self.headers, cookies=self.cookies, callback=self.page_parse)

    def page_parse(self, response):
        # get products urls
        products = response.css('.product-link::attr(href)').getall()
        for product in products:
            product_url = self.base_url + product
            yield scrapy.Request(url=product_url, headers=self.headers, cookies=self.cookies, callback=self.product_parse)

    def product_parse(self, response):
        item = ProductItem()

        # regex patterns
        description_pattern = re.compile(r'\"longDescription\":\"(.*?)\"', re.MULTILINE | re.DOTALL)
        brand_pattern = re.compile(r'\"brand\":\{\"name\"\:\"(.*?)\"\}', re.MULTILINE | re.DOTALL)
        sku_pattern = re.compile(r'\"activeSkuId\":\"(.*?)\"', re.MULTILINE | re.DOTALL)
        barcodes_pattern = re.compile(r'\"upc\":(\[.*?\])', re.MULTILINE | re.DOTALL)
        
        item['name'] = response.css('.e1yn5b3f7::text').get()
        item['category'] = '|'.join(response.css('.e16uoh2c4 .elkyjhv0::text').getall()[1:])
        
        # description = html.unescape(response.css('script').re(description_pattern)[0])
        # cleanr = re.compile('<.*?>')
        # item['description'] = re.sub(cleanr, ' ', description)

        item['description'] = response.css('script').re(description_pattern)[0].replace('\\u003Cbr>', ' ')
        item['brand'] = response.css('script').re(brand_pattern)[0]
        item['store'] = 'Walmart'
        item['url'] = response.url
        item['sku'] = response.css('script').re(sku_pattern)[0]
        item['package'] = response.css('.eudvd6x0::text').get()
        
        images = response.css('.css-128ipej::attr(style)').getall()
        if images:
            images = [image[image.index('(')+1:][:-1] for image in images]
        else:
            images = [response.css('.ervhxpq1::attr(src)').get()]
        item['image_url'] = str(images)

        item['barcodes'] = response.css('script').re(barcodes_pattern)[0]
        barcodes = ast.literal_eval(response.css('script').re(barcodes_pattern)[0])
        item['barcodes'] = barcodes[0]

        # establish https connection
        conn = http.client.HTTPSConnection(self.base_url.replace('https://',''))
        
        item2 = copy.copy(item)

        # thunder bay store
        store_base_url = '/api/product-page/find-in-store?latitude=43.6560592651&longitude=-79.434173584&lang=en&upc='
        item = self.get_store_info(3106, store_base_url, item, conn, response, "M6H")
        yield item

        # toronto store
        store_base_url = '/api/product-page/find-in-store?latitude=48.4114837646&longitude=-89.2452468872&lang=en&upc='
        item2 = self.get_store_info(3124, store_base_url, item2, conn, response, "P7B")
        yield item2
        

    def get_store_info(self, store_number, store_base_url, item, conn, response, store_fsa):
        req_url = store_base_url + item['barcodes']
        conn.request('GET', req_url)
        store_info = json.loads(conn.getresponse().read().decode('utf-8'))
        for elem in store_info['info']:
            if elem['id'] == store_number:
                item['stock'] = elem['availableToSellQty']
                if item['stock'] < 0:
                    item['stock'] = 0

                if 'sellPrice' in elem:
                    item['price'] = elem['sellPrice']
                else:
                    # get general price
                    price_url = '/api/product-page/price-offer'
                    body = {
                        "availabilityStoreId": str(store_number),
                        "fsa": store_fsa,
                        "lang": "en",
                        "products": [
                            {
                                "productId": response.url.split('/')[-1],
                                "skuIds": [
                                    item['sku']
                                    ]
                            }
                            ]
                    }
                    conn.request('POST', price_url, body=json.dumps(body), headers={"Content-Type":"application/json"})
                    general_price_info = json.loads(conn.getresponse().read().decode('utf-8'))

                    # item['price'] = general_price_info['offers'][list(general_price_info['offers'].keys())[0]]['currentPrice]
                    item['price'] = general_price_info['offers'][item['sku']]['currentPrice']
                item['branch'] = str(store_number)
                break

        return item



