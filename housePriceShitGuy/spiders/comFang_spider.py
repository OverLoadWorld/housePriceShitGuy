import scrapy


class ComFangSpider(scrapy.Spider):
    name = "fang"

    def start_requests(self):
        urls = [
            'http://newhouse.datong.fang.com/house/s/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for infoItem in response.xpath("//div[@class='nl_con clearfix']/ul/li/div[@class='clearfix']/div[@class='nlc_details']"):
            yield{
                'name' : infoItem.xpath("div[@class='house_value clearfix']/div[@class='nlcd_name']/a/text()").extract_first(),
                'type' : infoItem.xpath("//div[@class='house_type clearfix']//a/text()").extract_first(),
                'address' : infoItem.xpath("//div[@class='address']//a/text()").extract_first(),
                'tel' : infoItem.xpath("//div[@class='tel']//p//text()").extract_first(),
                'price' : infoItem.xpath("//div[@class='nhouse_price']//text()").extract()
            }

#        response.xpath("//div[@class='nl_con clearfix']/ul/li//div[@class='nlc_details']/div[@class='house_value clearfix']/div[@class='nlcd_name']/a/text()")
#        page = response.url.split("/")[-2]
#        filename = 'quotes-%s.html' % page
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)
