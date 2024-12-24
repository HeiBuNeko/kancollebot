import json
import scrapy
from kancollebot.items import TimeItem


class TimeListSpider(scrapy.Spider):
    name = "time_list"
    custom_settings = {
        "ITEM_PIPELINES": {
            "kancollebot.pipelines.TimeListPipeline": 300,
        },
    }

    def start_requests(self):
        with open("ship_list.jsonl", encoding="utf-8") as f:
            for line in f:
                ship_item = json.loads(line.strip())
                yield scrapy.Request(ship_item["href"], self.parse)

    def parse(self, response):
        name = response.xpath('//h1[@id="firstHeading"]/text()').get()
        # 时报
        shibao_trs = response.xpath(
            '//h3[span[@id=".E6.97.B6.E6.8A.A5"]]/following-sibling::table[1]/tr'
        )
        # 报时
        baoshi_trs = response.xpath(
            '//h3[span[@id=".E6.8A.A5.E6.97.B6"]]/following-sibling::table[1]/tr'
        )
        # print(f"{name} {shibao_trs} 时报表格 {baoshi_trs} 报时表格")
        time_trs = shibao_trs if len(shibao_trs) > 0 else baoshi_trs
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
