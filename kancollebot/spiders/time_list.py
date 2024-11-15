import json
import scrapy


class TimeListSpider(scrapy.Spider):
    name = "time_list"

    def start_requests(self):
        with open("ship_list.jsonl", encoding="utf-8") as f:
            ship_list = [json.loads(line.strip()) for line in f]
            print(ship_list)
            # for ship_item in ship_list:
            #     yield scrapy.Request(ship_item.href, self.parse)
        yield scrapy.Request(ship_list[0]['href'], self.parse)

    def parse(self, response):
        print("test")

        # MP3链接
        # trs = response.xpath('//*[@id="mw-content-text"]/div/table[4]/tr')
        # urls = []
        # for i in range(1, len(trs), 2):
        #     url = trs[i].xpath('td[1]/div/div[2]/div[2]/ul/li/a').attrib['data-filesrc']
        #     urls.append(url)
        # yield {'urls': urls}
