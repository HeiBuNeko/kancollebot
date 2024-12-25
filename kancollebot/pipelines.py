# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from contextlib import ExitStack
import json
import os

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
        self.files = {}
        self.data = {}
        os.makedirs("time_list", exist_ok=True)

    def close_spider(self, spider):
        with ExitStack() as stack:
            for name, items in self.data.items():
                file_path = os.path.join("time_list", f"{name}.json")
                with stack.enter_context(open(file_path, "w", encoding="utf-8")) as f:
                    json.dump(items, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        name = item.get("name")
        if name not in self.data:
            self.data[name] = []
        self.data[name].append(dict(item))
        return item
