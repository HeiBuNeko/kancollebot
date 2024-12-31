# kancollebot

舰娘百科-舰娘列表-时报 Scrapy 项目

# 使用方法

**舰娘列表（Wiki中有具体页面且不为重定向页面）**

对 `https://zh.kcwiki.cn/wiki/舰娘列表` 进行爬取

1. 部分条目Wiki未收录 `new`
2. 部分条目为重定向页面 `改`
3. 排除表头，补全 `href`

```
scrapy crawl ship_list
```

如需全部舰娘列表请将对 `a` 标签的限制去除

```
        links = table.xpath(
            './/a[not(contains(@class, "new") or contains(@class, "image") or contains(text(), "改"))]'
        )
```

结果存放于根目录的 `ship_list.json` 中

**时报列表（Wiki中有具体时报内容的页面）**

对 `ship_list.json` 中的 `href` 进行爬取

1. Wiki部分页面中 `时报` 为 `报时`
2. 由单一ID选择器都会定位到两个相同的表格
3. 文本描述末尾带有 `\n` 需要处理

```
scrapy crawl time_list
```

结果存放于根目录的 `time_list` 文件夹

用于 `koishi-plugin-kancolle-time `插件，采用 `json` 格式存储便于 `JavaScript` `JSON.parse `解析

目前发现的问题：有且仅有 `朝潮.json`会有前两行多余数据，请手动排除
