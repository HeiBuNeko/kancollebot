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
        self.stack = ExitStack()
        self.files = {}
        if not os.path.exists("time_list"):
            os.makedirs("time_list")

    def close_spider(self, spider):
        self.stack.close()

    def process_item(self, item, spider):
        name = item.get("name")
        file_path = os.path.join("time_list", f"{name}.jsonl")
        if name not in self.files:
            self.files[name] = self.stack.enter_context(
                open(file_path, "w", encoding="utf-8")
            )
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.files[name].write(line)
        return item
