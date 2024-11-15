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
        trs = table.css("tr")
        # 排除表头
        for trs_i in range(1, len(trs)):
            tds = trs[trs_i].css("td")
            # 数据可能存在于前两个 td 中
            for tds_i in range(2):
                name = tds[tds_i].css("a::text").get()
                href = tds[tds_i].css("a::attr(href)").get()
                if name is not None and href is not None:
                    yield {"name": name, "href": "https://zh.kcwiki.cn" + href}
                    break

        # MP3链接
        # trs = response.xpath('//*[@id="mw-content-text"]/div/table[4]/tr')
        # urls = []
        # for i in range(1, len(trs), 2):
        #     url = trs[i].xpath('td[1]/div/div[2]/div[2]/ul/li/a').attrib['data-filesrc']
        #     urls.append(url)
        # yield {'urls': urls}
