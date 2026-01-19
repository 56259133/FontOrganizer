# src/config.py

# ================= 文件过滤配置 =================
# 支持的字体文件扩展名
FONT_EXTENSIONS = {'.ttf', '.otf', '.ttc', '.wf'}

# 支持的压缩包扩展名
ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz'}

# 系统生成文件忽略列表
IGNORE_FILES = {'.ds_store', 'thumbs.db'}

# ================= 运行行为配置 =================
# 是否优先提取中文字体名称
PREFER_CHINESE_NAME = True

# 程序执行结束后是否自动关闭窗口
AUTO_CLOSE = True

# ================= 清洗规则配置 =================
# 1. 强制移除的特定关键词列表 (不区分大小写)
# 用于移除文件名中残留的非括号内的营销词汇
KEYWORDS_TO_REMOVE = [
    "非商用", "个人版", "免费版", "预览版",
    "Personal Use", "Demo", "Trial", "Preview",
    "Reference Only", "商用需授权", "For Commercial"
]

# 2. 字体厂商前缀列表 (用于从英文名中剥离厂商标识)
# 注意：仅在提取到的名称以这些字符开头时生效
VENDOR_PREFIXES = [
    "Aa", "HF", "SJ", "HGG", "HG", "Huaguang", # 增加 HGG, HG, Huaguang
    "YE", "QS", "Fc", "I.", "FZZJ", "FZ"
]

# 3. 样式词映射表
# 将英文样式词替换为空字符串或对应的中文
STYLE_MAPPING = {
    "Regular": "",
    "Bold": "粗体", # 可根据需要改为 ""
    "Italic": "斜体",
    "Medium": "中等",
    "Light": "细体",
    "Semibold": "半粗",
    "Black": "超粗"
}