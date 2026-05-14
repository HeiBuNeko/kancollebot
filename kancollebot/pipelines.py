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
        item["wiki_url"] = "https://zh.kcwiki.cn" + item["wiki_url"]
        return item


class TimeListPipeline:
    def open_spider(self, spider):
        self._seen_keys = set()

    def process_item(self, item, spider):
        key = (item["ship_name"], item["time_label"])
        if key in self._seen_keys:
            raise DropItem(f"duplicate time slot: {key!r}")
        self._seen_keys.add(key)
        return item
