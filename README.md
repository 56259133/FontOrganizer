# 🎨 FontOrganizer - 字体文件重命名整理工具

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-orange.svg)

> **拒绝杂乱！** 一键自动解压、清洗、重命名字体文件或字体压缩包，让你的字体库井井有条。 ✨

## 📖 项目简介

**FontOrganizer** 是一个基于 Python 的强大自动化工具，专为阅读器用户、字体设计师和字体收藏爱好者打造。它能深入读取字体文件的元数据（Metadata），将它们还原为最纯净的中文或英文名称，并清理其余垃圾信息。

---

## 🚀 核心功能

### 1. 📦 智能解压与清理
- **全格式支持**：自动识别并解压 `.zip`, `.rar`, `.7z`, `.tar`, `.gz` 等格式。
- **自动去重**：解压后自动删除源压缩包，不占硬盘空间。
- **垃圾扫除**：递归删除非字体文件（如 `.jpg` 预览图、`.txt` 说明书、`.url` 快捷方式），只保留 `.ttf`, `.otf` 等字体文件。

### 2. 🏷️ 深度元数据重命名
- **中文优先**：优先提取字体内部的 **中文全名 (Full Name)**。
- **智能回退**：如果字体没有中文名，自动回退到英文名。
- **组合修复策略**：针对 **“华光” (Huaguang)** 等老旧字库元数据缺失的问题，自动采用 `Family Name` + `Subfamily Name` 拼接修复，确保名字正确显示（例如：`华光钢铁直黑 超粗黑`）。

### 3. 🧹 文件名深度清洗 (V2.1 新特性)
- **去干扰前缀**：自动切除文件名头部的乱码编号（如 `A019-`）和厂商前缀（如 `Aa`, `SJ`, `HF`）。
- **去括号/去推广**：**强制移除** 文件名中所有的括号 `()` `（）` 及其内部的所有文字。
    - *Before:* `Aa舒黑(个人非商用).ttf`
    - *After:* `舒黑.ttf`
- **样式简化**：支持将 `Regular`, `Bold` 等英文后缀映射为空白或中文（如“粗体”）。

---

## 📂 项目结构

```text
FontOrganizer/
├── input_fonts/          # 📥 (默认) 把你要整理的乱七八糟的字体/压缩包扔这里
├── src/                  # ⚙️ 核心源码目录
│   ├── __init__.py
│   ├── archive_utils.py  # 解压逻辑
│   ├── config.py         # 📝 配置文件 (在这里修改过滤规则)
│   ├── file_cleaner.py   # 清理逻辑
│   └── font_utils.py     # 字体识别与命名核心算法
├── main.py               # ▶️ 程序启动入口
├── requirements.txt      # 📦 依赖库列表
└── README.md             # 📖 说明文档

