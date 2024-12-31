import scrapy
from kancollebot.items import ShipItem


class ShipListSpider(scrapy.Spider):
    name = "ship_list"
    start_urls = [
        "https://zh.kcwiki.cn/wiki/舰娘列表",
    ]
    custom_settings = {
        "FEEDS": {
            "ship_list.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "fields": None,
                "indent": 4,
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {
            "kancollebot.pipelines.ShipListPipeline": 300,
        },
    }

    def parse(self, response):
        ship_item = ShipItem()
        # 舰娘列表
        # 1级 99级 Table
        table = response.css(".wikitable.fixtable")[0]
        # 排除 class new 和 images 和 "改"
        links = table.xpath(
            './/a[not(contains(@class, "new") or contains(@class, "image") or contains(text(), "改"))]'
        )
        for link in links:
            ship_item["name"] = link.xpath("text()").get()
            ship_item["href"] = link.attrib["href"]
            yield ship_item
