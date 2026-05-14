import json
import scrapy
from scrapy.http import TextResponse

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
                yield scrapy.Request(ship_item["wiki_url"], self.parse)
        # yield scrapy.Request("https://zh.kcwiki.cn/zh-cn/U-511", self.parse)

    def parse(self, response: TextResponse):
        ship_name = response.xpath('//h1[@id="firstHeading"]/text()').get()

        time_texts = [
            "〇〇〇〇时报",
            "〇一〇〇时报",
            "〇二〇〇时报",
            "〇三〇〇时报",
            "〇四〇〇时报",
            "〇五〇〇时报",
            "〇六〇〇时报",
            "〇七〇〇时报",
            "〇八〇〇时报",
            "〇九〇〇时报",
            "一〇〇〇时报",
            "一一〇〇时报",
            "一二〇〇时报",
            "一三〇〇时报",
            "一四〇〇时报",
            "一五〇〇时报",
            "一六〇〇时报",
            "一七〇〇时报",
            "一八〇〇时报",
            "一九〇〇时报",
            "二〇〇〇时报",
            "二一〇〇时报",
            "二二〇〇时报",
            "二三〇〇时报",
        ]

        for time_text in time_texts:
            time_item = TimeItem(ship_name=ship_name, time_label=time_text)
            time_td = response.xpath(f"//td[normalize-space(.)='{time_text}']")[:1]
            # 个别页面（如熊野丸）该格为「二〇〇〇时报！」而非「二〇〇〇时报」
            if not time_td and time_text == "二〇〇〇时报":
                time_td = response.xpath("//td[normalize-space(.)='二〇〇〇时报！']")[
                    :1
                ]
            if time_td:
                # 播放器：<td>...</td>
                time_href_td = time_td.xpath("preceding-sibling::td[1]")[:1]
                time_href_a = time_href_td.xpath(
                    ".//ul[contains(@class,'sm2-playlist-bd')]/li/a[1]"
                )[:1]

                # 音频链接：<a data-filesrc="...">...</a>
                time_item["audio_url"] = time_href_a.xpath("@data-filesrc").get()

                # 日文文本：<td lang="ja">...</td>
                time_word_jp_td = time_td.xpath("following-sibling::td[@lang='ja']")[:1]
                time_item["voice_line_ja"] = (
                    time_word_jp_td.xpath("text()").get().strip()
                )

                # 中文文本：下一行 <tr> 的首个 <td>
                time_word_cn_td = time_td.xpath(
                    "parent::tr/following-sibling::tr[1]/td[1]"
                )[:1]
                time_item["voice_line_zh"] = (
                    time_word_cn_td.xpath("text()").get().strip()
                )
                yield time_item
