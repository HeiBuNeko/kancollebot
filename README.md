# kancollebot

**当前版本：v2.0.0**

从 [舰娘百科（zh.kcwiki.cn）](https://zh.kcwiki.cn) 抓取**舰娘列表**与**报时（时报）**数据的 [Scrapy](https://docs.scrapy.org) 项目。输出为根目录下的 JSON 文件，便于脚本或前端直接 `JSON.parse` 使用。

---

## 环境要求

- Python **≥ 3.14**（见仓库根目录 `.python-version`）
- 依赖：**Scrapy** 等（见 `pyproject.toml` / `requirements.txt`）

---

## 安装

**推荐（uv）：**

```bash
uv sync
```

**或 pip：**

```bash
pip install -r requirements.txt
```

---

## 使用方法

请在**项目根目录**（存在 `scrapy.cfg` 的根）执行命令，以便正确读写 JSON 与解析相对路径。

### 1. 舰娘列表 `ship_list`

**入口：** `start_urls` 固定为 [舰娘列表](https://zh.kcwiki.cn/wiki/舰娘列表)。

**解析逻辑（`parse`）：**

- 取页面中**第一个** `.wikitable.fixtable` 表格。
- 在表内选取所有 `<a>`，并**排除**满足任一条件的链接：
  - `class` 含 `new`（未建条目）；
  - `class` 含 `image`（图片列等）；
  - 链接文本含 **「改」**（改装舰等与主行区分）。
- 对每个保留的链接：`name` 取链接文本；`href` 取 `href` 属性，并把路径中的 **`wiki` 替换为 `zh-cn`**。
- 经 `ShipListPipeline` 后，`href` 会变为完整地址：`https://zh.kcwiki.cn` + 相对路径（见下表）。

**输出配置：** `FEEDS` 写入根目录 `ship_list.json`，JSON、UTF-8、缩进 4、每次覆盖。

```bash
scrapy crawl ship_list
```

---

### 2. 报时列表 `time_list`

**前置条件：** 根目录已有上一步生成的 `ship_list.json`（`time_list` 在 `start_requests` 中直接 `open("ship_list.json")`）。

**请求：** 逐条读取 JSON 中的 `href`，对每个 URL 发起请求并由 `parse` 处理。

**解析逻辑（`parse`）：**

- **舰娘名 `name`：** `//h1[@id="firstHeading"]/text()`。
- **时段：** 按固定列表依次匹配表格单元格文案，从 `〇〇〇〇时报` 到 `二三〇〇时报`（共 24 个整点时段）。
- 对每个时段，用 XPath `//td[normalize-space(.)='时段文案']` 定位单元格（仅取第一个匹配）。
  - **例外：** 若时段为 `二〇〇〇时报` 且未命中，再尝试匹配单元格正文为 **`二〇〇〇时报！`**（代码注释中的熊野丸等页面）。
- 若该时段格存在，则填充 `TimeItem` 并 `yield`：
  - **`time`：** 上述时段字符串（如 `〇三〇〇时报`）。
  - **`href`：** 同一行中，时段格**前一个** `td` 内，`ul.sm2-playlist-bd` 下第一个 `li a` 的 **`data-filesrc`**（音频地址）。
  - **`time_word_jp`：** 时段格**后一个**兄弟 `td`（`lang="ja"`）的文本，去首尾空白。
  - **`time_word_cn`：** 时段格所在 `tr` 的**下一行** `tr` 中**第一个** `td` 的文本，去首尾空白。

若页面缺少某时段行，该时段不会产生条目。若同一 `(name, time)` 因版面重复被多次写出，由 **`TimeListPipeline`** 按 `(name, time)` 去重（见下节）。

**输出配置：** `FEEDS` 写入根目录 `time_list.json`，JSON、UTF-8、缩进 4、每次覆盖。

```bash
scrapy crawl time_list
```

**建议顺序：** 先 `scrapy crawl ship_list`，再 `scrapy crawl time_list`。

---

## 管道行为摘要

| 管道 | 作用 |
|------|------|
| `ShipListPipeline` | 为 `href` 补全站点根 URL |
| `TimeListPipeline` | 按 `(name, time)` 去重，丢弃重复报时段 |

---

## 与下游项目的关系

数据格式面向 **[koishi-plugin-kancolle-time](https://www.npmjs.com/package/koishi-plugin-kancolle-time)** 等消费方：`time_list.json` 为单一 JSON 文件，便于在 JavaScript 中解析。

---

## 爬虫与下载设置说明

- `kancollebot/settings.py` 中 **`DOWNLOAD_DELAY`** 默认已注释；若需降低对站点的请求频率，可自行取消注释并调整秒数。
- `CONCURRENT_REQUESTS = 1`，避免并发过高。

---

## 更新日志

### v2.0.0

- 使用 **uv** 管理依赖，新增 `pyproject.toml`、`requirements.txt`、`uv.lock`、`.python-version`
- **时报管道**：按舰娘名与报时文本 `(name, time)` 去重，避免重复条目写入 `time_list.json`
- **舰娘列表爬虫**：每条链接单独 `yield` 新的 `ShipItem`，避免复用同一字典导致的数据污染
- 下载延迟默认关闭（保留在设置文件中可按需启用）
- 扩充与修正 `.gitignore`（与常见 Python 模板对齐）

### 历史版本

- **v1.1.2** — `ship_list` 使用 `zh-cn` 替换 `wiki`；修复 `time_list` 简繁随机出现的问题  
- **v1.1.1** — 数据更新（舰娘百科 v2025.02.25）  
- **v1.1.0** — 数据更新（舰娘百科 v2025.01.20）  
- **v1.0.6** — 上传产物用于校对差异  
- **v1.0.5** — 兼容 Wiki 中「时报」为折叠元素  
- **v1.0.4** — 时报表格不绑定特定 `h3`  
- **v1.0.3** — `time_list.json` 单文件输出  
- **v1.0.2** — `ship_list` 改为 JSON  
- **v1.0.1** — 采用 JSON 便于 `JSON.parse`  
- **v1.0.0** — 初始版本  

---

## 许可证

见仓库根目录 [`LICENSE`](LICENSE)。
