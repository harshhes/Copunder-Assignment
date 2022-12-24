import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class UnderdogSpider(CrawlSpider):
    name = 'underdog'
    allowed_domains = ['www.copunderdog.com']
    # start_urls = ['http://copunderdog.com/']
    url = 'https://www.copunderdog.com/product-category/sneakers/'
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            # wait_time=3,
            # callback=self.parse_item,
            headers={'User-Agent':self.user_agent})

    rules=(
        Rule(LinkExtractor(restrict_xpaths="//div[@class='product-header']/a"),callback='parse_item', follow=True, process_request='get_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='page-numbers']/li[position()=last()]/a"), process_request='get_user_agent')
    )

    def get_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        # driver = response.meta['driver']

        # html = driver.page_source
        # response_obj = Selector(text=html)

        name = response.xpath("//h1/text()").get()
        rupee = response.xpath("//bdi/span/text()").get()
        price =response.xpath("//bdi/text()").get()
        sizes = response.xpath("//li[contains(@class,'variable-item button-variable-item')]/div/span/text()").getall()
        sku = response.xpath("//span[@class='sku']/text()").get()
        categories = response.xpath("//span[@class='posted_in']/a/text()").getall()
        description = response.xpath("//div[@class='woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab']/div/p/text()").getall()
        images = response.xpath("//div[@class='woocommerce-product-gallery__image woocommerce-main-image']/a/@href").getall()


        yield {
            "Item_url": response.url,
            "Name": name,
            "Price":rupee+price[1:],
            "Sizes_Available": ','.join(sizes),
            "SKU":sku,
            "Categories":','.join(categories),
            "Description":",".join(description),
            "All_image_URLs":''.join(images),
        }