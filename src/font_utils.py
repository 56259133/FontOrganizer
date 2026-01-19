# src/font_utils.py
import os
import re
from fontTools.ttLib import TTFont
from .config import FONT_EXTENSIONS, PREFER_CHINESE_NAME, KEYWORDS_TO_REMOVE, VENDOR_PREFIXES, STYLE_MAPPING


def sanitize_filename(name):
    """
    去除文件名中的操作系统非法字符。
    :param name: 原始文件名
    :return: 合法的文件名字符串
    """
    if not name:
        return ""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def clean_filename(name):
    """
    对字体名称进行标准化清洗。
    规则：
    1. 移除首尾空格。
    2. 移除厂商前缀 (如 Aa, HGG)。
    3. 移除所有括号及其内部内容 (包括 '非商用' 等)。
    4. 移除特定的垃圾关键词。
    5. 移除文件名头部的数字编号。
    """
    if not name:
        return ""

    name = name.strip()

    # 1. 移除厂商前缀
    for prefix in VENDOR_PREFIXES:
        if name.lower().startswith(prefix.lower()):
            # 仅当去除前缀后仍有内容时才执行，避免误删全名
            if len(name) > len(prefix):
                name = name[len(prefix):].strip()
                # 某些前缀后可能跟有连接符，如 HGG-
                name = re.sub(r'^[\-_]+', '', name)
            break

    # 2. 移除头部干扰字符 (如 "01.", "A-")
    name = re.sub(r'^[A-Za-z0-9]{1,6}[\-_\.]+', '', name)
    name = re.sub(r'^\d+\.?', '', name)

    # 3. 强制移除所有括号及其内部内容 (核心需求)
    # 匹配中文或英文左括号开头，非右括号的任意字符，直到右括号结束
    name = re.sub(r'[\(（][^\)）]*[\)）]', '', name)

    # 4. 移除预定义的垃圾关键词
    for keyword in KEYWORDS_TO_REMOVE:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        name = pattern.sub('', name)

    # 5. 处理英文样式词 (如 Regular -> "")
    for eng_style, replacement in STYLE_MAPPING.items():
        pattern = re.compile(r'\b' + re.escape(eng_style) + r'\b', re.IGNORECASE)
        name = pattern.sub(replacement, name)

    # 6. 收尾清理：合并多余空格，去除首尾符号
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'^[\-_\.]+|[\-_\.]+$', '', name)

    return name.strip()


def get_name_record(font, name_id, lang_id, platform_id=3):
    """
    从字体的 name table 中提取特定记录。
    :param font: TTFont 对象
    :param name_id: Name ID (1=Family, 2=Subfamily, 4=Full Name)
    :param lang_id: Language ID (2052=Zh, 1033=En)
    :param platform_id: Platform ID (3=Windows)
    :return: 解码后的字符串或 None
    """
    for record in font['name'].names:
        if record.nameID == name_id and record.platformID == platform_id and record.langID == lang_id:
            try:
                decoded = record.toUnicode()
                # 过滤无效数据
                if decoded and len(decoded.strip()) > 0:
                    return decoded.replace('\x00', '')
            except UnicodeDecodeError:
                continue
    return None


def get_font_display_name(font_path):
    """
    获取最佳的字体显示名称。
    策略：
    1. 优先尝试读取中文 Full Name (ID 4)。
    2. 如果失败，尝试读取中文 Typographic Family (ID 16)。
    3. 如果失败，尝试拼接中文 Family (ID 1) + Subfamily (ID 2)。(适配华光等老旧字体)
    4. 如果无中文，回退到英文名称，重复上述步骤。
    """
    font = None
    try:
        font = TTFont(font_path)

        # 语言优先级配置
        langs = [2052, 1033] if PREFER_CHINESE_NAME else [1033, 2052]

        final_name = None

        for lang in langs:
            # 步骤 A: 尝试获取 ID 4 (Full Name)
            name = get_name_record(font, 4, lang)
            if name:
                final_name = name
                break

            # 步骤 B: 尝试获取 ID 16 (Typographic Family)
            # 注意：ID 16 通常不包含字重，需要慎重使用，或者仅作为 Family 部分
            name = get_name_record(font, 16, lang)
            if name:
                final_name = name
                break

            # 步骤 C: 尝试组合 ID 1 (Family) + ID 2 (Subfamily)
            # 华光系列字体的 ID 4 可能是英文，但 ID 1 是中文 "华光xx"
            family = get_name_record(font, 1, lang)
            subfamily = get_name_record(font, 2, lang)

            if family:
                # 如果子族名是 "Regular" 或 "Standard"，通常可以省略
                if subfamily and subfamily.lower() not in ['regular', 'standard', 'normal']:
                    final_name = f"{family} {subfamily}"
                else:
                    final_name = family
                break

        # 如果 Windows 平台 (ID 3) 没找到，尝试 Mac 平台 (ID 1) 的中文 (Lang 33)
        if not final_name and PREFER_CHINESE_NAME:
            final_name = get_name_record(font, 4, 33, platform_id=1)
            if not final_name:
                fam = get_name_record(font, 1, 33, platform_id=1)
                if fam:
                    final_name = fam

        # 最终回退：如果还是没名字，遍历所有记录找任何可读名称
        if not final_name:
            for record in font['name'].names:
                if record.nameID in [4, 1]:
                    try:
                        final_name = record.toUnicode()
                        break
                    except:
                        continue

        if final_name:
            return clean_filename(final_name)

        return None

    except Exception:
        # 文件可能损坏或非标准格式
        return None
    finally:
        if font:
            font.close()


def rename_fonts(target_dir):
    """
    遍历指定目录，对符合条件的字体文件进行重命名。
    """
    print(f"正在扫描并整理字体文件...")
    renamed_count = 0

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in FONT_EXTENSIONS:
                font_name = get_font_display_name(file_path)

                # 仅当成功提取到名称且名称不为空时执行
                if font_name:
                    safe_name = sanitize_filename(font_name)

                    # 避免生成空文件名
                    if not safe_name:
                        continue

                    new_filename = f"{safe_name}{file_ext}"
                    new_path = os.path.join(root, new_filename)

                    # 检查是否需要重命名 (忽略大小写差异)
                    if file_path.lower() != new_path.lower():
                        # 处理重名冲突：添加数字后缀
                        if os.path.exists(new_path):
                            counter = 1
                            name_base = safe_name
                            while os.path.exists(os.path.join(root, f"{name_base}_{counter}{file_ext}")):
                                counter += 1
                            new_path = os.path.join(root, f"{name_base}_{counter}{file_ext}")

                        try:
                            os.rename(file_path, new_path)
                            print(f"[重命名] {file} -> {os.path.basename(new_path)}")
                            renamed_count += 1
                        except OSError:
                            print(f"[错误] 无法重命名文件: {file}")

    return renamed_count