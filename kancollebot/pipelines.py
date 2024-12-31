# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem

class KancollebotPipeline:
    def process_item(self, item, spider):
        return item


class ShipListPipeline:
    def process_item(self, item, spider):
        item["href"] = "https://zh.kcwiki.cn" + item["href"]
        return item


class TimeListPipeline:
    def process_item(self, item, spider):
        if item['name'] == '朝潮' and '时报' not in item['time']:
            raise DropItem('排除朝潮非时报项')
        return item
