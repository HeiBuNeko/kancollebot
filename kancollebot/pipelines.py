# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from contextlib import ExitStack
import json

from itemadapter import ItemAdapter


class KancollebotPipeline:
    def process_item(self, item, spider):
        return item


class ShipListPipeline:
    def process_item(self, item, spider):
        item["href"] = "https://zh.kcwiki.cn" + item["href"]
        return item


class TimeListPipeline:
    def open_spider(self, spider):
        self.stack = ExitStack()
        self.files = {}

    def close_spider(self, spider):
        self.stack.close()

    def process_item(self, item, spider):
        name = item.get("name")
        if name not in self.files:
            self.files[name] = self.stack.enter_context(
                open(f"{name}.jsonl", "w", encoding="utf-8")
            )
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.files[name].write(line)
        return item
