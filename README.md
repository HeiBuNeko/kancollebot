# kancollebot

舰娘百科-舰娘列表-时报 Scrapy 项目

# 使用方法

#### **舰娘列表（Wiki中有具体页面且不为重定向页面）**

对 `https://zh.kcwiki.cn/wiki/舰娘列表` 进行爬取

1. 部分条目Wiki未收录 `new`
2. 排除表头 `images`，补全 `href`
3. 部分条目为重定向页面 `改`

```
scrapy crawl ship_list
```

结果存放于根目录的 `ship_list.json` 中

#### **时报列表（Wiki中有具体时报内容的页面）**

对 `ship_list.json` 中的 `href` 进行爬取

1. Wiki部分页面中 `时报` 为 `报时`
2. Wiki部分页面中 `时报` 为折叠元素
3. 由单一ID选择器都会定位到两个相同的表格
4. 文本描述末尾带有 `\n` 需要处理
5. 有且仅有 `朝潮` 会有前两行多余数据

```
scrapy crawl time_list
```

结果存放于根目录的 `time_list.json` 中

用于 `koishi-plugin-kancolle-time `插件，采用 `json` 格式存储便于 `JavaScript` `JSON.parse `解析

# 更新日志

* v1.0.0 初始化
* v1.0.1 采用 json 格式存储便于 JSON.parse 解析
* v1.0.2 ship_list 改为 json 格式
* v1.0.3 time_list.json 单文件
* v1.0.4 时报表格不特定 h3
* v1.0.5 Wiki部分页面中 时报 为折叠元素
