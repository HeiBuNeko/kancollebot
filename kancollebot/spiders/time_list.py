import json
import scrapy
from kancollebot.items import TimeItem


class TimeListSpider(scrapy.Spider):
    name = "time_list"
    custom_settings = {
        "FEEDS": {
            "time_list.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "fields": None,
                "indent": 4,
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {
            "kancollebot.pipelines.TimeListPipeline": 300,
        },
    }

    def start_requests(self):
        with open("ship_list.json", encoding="utf-8") as file:
            ship_list = json.load(file)
            for ship_item in ship_list:
                yield scrapy.Request(ship_item["href"], self.parse)

    def parse(self, response):
        name = response.xpath('//h1[@id="firstHeading"]/text()').get()

        # 折叠
        collapse_trs = response.xpath(
            '//span[@id=".E6.97.B6.E6.8A.A5"]/../following-sibling::div[contains(@class,"mw-collapsible")][1]/div[contains(@class,"mw-collapsible-content")]/table/tr'
        )
        # 时报
        shibao_trs = response.xpath(
            '//span[@id=".E6.97.B6.E6.8A.A5"]/../following-sibling::table[1]/tr'
        )
        # 报时
        baoshi_trs = response.xpath(
            '//span[@id=".E6.8A.A5.E6.97.B6"]/../following-sibling::table[1]/tr'
        )
        time_trs = collapse_trs or shibao_trs or baoshi_trs

        # 表格
        for time_tr_i in range(1, len(time_trs), 2):
            time_item = TimeItem()
            time_item["name"] = name
            # 包含语音和日文文本的混合内容
            mix_content = time_trs[time_tr_i]
            time_item["time"] = mix_content.xpath(".//td[2]/text()").get().strip(" \n")
            time_item["time_word_jp"] = (
                mix_content.xpath(".//td[3]/text()").get().strip(" \n")
            )
            time_item["href"] = mix_content.xpath(
                './/ul[contains(@class,"sm2-playlist-bd")]/li/a'
            ).attrib["data-filesrc"]
            # 中文文本
            time_item["time_word_cn"] = (
                time_trs[time_tr_i + 1].xpath("./td/text()").get().strip(" \n")
            )
            yield time_item
