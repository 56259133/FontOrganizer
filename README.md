# FontOrganizer - 字体自动整理工具

## 项目简介
FontOrganizer 是一款基于 Python 开发的本地字体库自动化整理工具。它能够递归扫描指定目录，自动解压压缩包，清理无关文件，并基于 OpenType 元数据将字体文件重命名为标准的中文或英文名称。

该工具针对设计师和字体收藏者开发，解决了下载字体文件名混乱、包含广告后缀、或者是压缩包套娃等痛点。

## 核心功能

1.  **智能解压与清理**
    *   自动识别并解压 `.zip`, `.rar`, `.7z` 等多种格式压缩包。
    *   解压后自动删除源压缩包，释放空间。
    *   自动递归清理空文件夹及非字体文件（如图片、URL快捷方式、说明文档）。

2.  **元数据重命名**
    *   基于 `fonttools` 深度读取 TTF/OTF 文件内部元数据。
    *   **多语言回退机制**：优先提取简体中文名称 (Language ID 2052)，缺失时自动回退到英文名称。
    *   **组合命名策略**：针对“华光”等老旧字库元数据缺失 Full Name 的情况，自动采用 `Family Name` + `Subfamily Name` 进行拼接修复。

3.  **文件名深度清洗**
    *   **去干扰**：自动移除文件名头部的乱码编号（如 `A019-`）、厂商前缀（如 `Aa`、`SJ`）。
    *   **去推广**：强制移除文件名中所有括号及其包含的内容（如 `(非商用)`, `(个人版)`）。
    *   **样式简化**：支持将 `Regular`、`Bold` 等后缀映射为空白或中文。

## 目录结构

```text
FontOrganizer/
├── input_fonts/          # (默认) 待处理的字体/压缩包存放区
├── src/                  # 源代码目录
│   ├── __init__.py
│   ├── archive_utils.py  # 压缩包处理模块
│   ├── config.py         # 配置文件 (修改过滤规则在此处)
│   ├── file_cleaner.py   # 文件清理模块
│   └── font_utils.py     # 字体识别与命名核心模块
├── main.py               # 程序入口
├── requirements.txt      # 项目依赖
└── README.md             # 说明文档
快速开始
1. 安装依赖
需要 Python 3.x 环境。
code
Bash
pip install -r requirements.txt
注意：处理 RAR 文件可能需要系统安装 WinRAR 或 7-Zip 并配置环境变量，或者安装 unrar 命令行工具。
2. 运行
将待整理的字体文件或压缩包放入 input_fonts 文件夹（或者在运行后输入自定义路径）。
code
Bash
python main.py
3. 配置
在 src/config.py 中可以自定义以下选项：
KEYWORDS_TO_REMOVE: 需要屏蔽的关键词列表。
VENDOR_PREFIXES: 需要去除的字体厂商前缀。
PREFER_CHINESE_NAME: 是否优先使用中文命名。
AUTO_CLOSE: 执行结束后是否自动关闭窗口。
注意事项
本工具涉及文件删除和重命名操作，建议首次使用时在副本数据上测试。
对于加密或损坏的字体文件，程序会自动跳过并保留原样。