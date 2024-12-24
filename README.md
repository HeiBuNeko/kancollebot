# kancollebot

舰娘百科-舰娘列表-时报 Scrapy 项目

# 使用方法

**舰娘列表（Wiki中有具体页面且不为重定向页面）**

```
scrapy crawl ship_list
```

例如：排除名称中带有‘“改”的舰娘，如需全部舰娘列表请将对 ``a``标签的限制去除

```
        links = table.xpath(
            './/a[not(contains(@class, "new") or contains(@class, "image") or contains(text(), "改"))]'
        )
```

结果存放于根目录的 ``ship_list.jsonl`` 中

**时报列表（Wiki中有具体时报内容的页面）**

```
scrapy crawl time_list
```

结果存放于根目录的 ``time_list`` 文件夹中
