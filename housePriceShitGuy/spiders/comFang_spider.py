import scrapy


def extract_type(infoItem, speItem, split):
    ret = ''
    typeList = infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']").xpath(speItem)
    for type in typeList:
        ret += "%s%s" % (type.extract().strip(), split)
    return ret


class ComFangSpider(scrapy.Spider):
    name = "fang"
    start_urls = [
        'http://newhouse.datong.fang.com/house/s/',
        # 'http://newhouse.datong.fang.com/house/s/b92/',
        # 'http://newhouse.datong.fang.com/house/s/b93/',
    ]

    def parse(self, response):
        for infoItem in response.xpath(
                "//div[@class='nl_con clearfix']/ul/li"):
            name = infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']/div[@class='house_value clearfix']/div[@class='nlcd_name']/a/text()").extract_first()
            price = infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']/div[@class='nhouse_price']/span/text()").extract_first()
            unit = infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']/div[@class='nhouse_price']/em/text()").extract_first()
            if name is None or price is None:
                continue
            yield {
                'name': name.strip(),
                'type': "%s %s" % (extract_type(infoItem, "div[@class='house_type clearfix']/text()", "-"),
                                   extract_type(infoItem, "div[@class='house_type clearfix']/a/text()", "-")),
                'address': infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']/div[@class='relative_message clearfix']/div[@class='address']/a/text()").extract_first().strip(),
                'tel': "-".join(infoItem.xpath("div[@class='clearfix']/div[@class='nlc_details']/div[@class='relative_message clearfix']/div[@class='tel']/p/text()").extract()).strip(),
                'price': "%s %s" % (price.strip(), "" if unit is None else unit.strip())
            }

        next_page = response.xpath(
                "//div[@class='page']/ul/li[@class='fr']/a[@class='next']/@href").extract_first()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page))
