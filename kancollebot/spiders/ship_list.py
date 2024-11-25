import scrapy


class ShipListSpider(scrapy.Spider):
    name = "ship_list"
    start_urls = [
        "https://zh.kcwiki.cn/wiki/舰娘列表",
    ]

    def parse(self, response):
        # 舰娘列表
        # 1级 99级 Table
        table = response.css(".wikitable.fixtable")[0]
        # 排除 class new 和 images
        links = table.xpath(
            './/a[not(contains(@class, "new") or contains(@class, "image"))]'
        )
        for link in links:
            name = link.xpath("text()").get()
            href = link.attrib["href"]
            print(href)
            yield {"name": name, "href": "https://zh.kcwiki.cn" + href}
