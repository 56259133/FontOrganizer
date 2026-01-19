# src/file_cleaner.py
import os
import shutil
from .config import FONT_EXTENSIONS, ARCHIVE_EXTENSIONS, IGNORE_FILES


def clean_non_font_files(target_dir):
    """删除非字体、非压缩包的文件"""
    print(f"开始清理杂项文件...")
    deleted_count = 0

    for root, dirs, files in os.walk(target_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # 逻辑：如果不是字体，且不在白名单（如压缩包、忽略文件）里，就删
            if (file_ext not in FONT_EXTENSIONS) and \
                    (file_ext not in ARCHIVE_EXTENSIONS) and \
                    (file.lower() not in IGNORE_FILES):

                try:
                    os.remove(file_path)
                    # print(f"删除垃圾文件: {file}")
                    deleted_count += 1
                except Exception:
                    pass

    return deleted_count


def flatten_directory(target_dir):
    """
    目录扁平化：
    将所有子文件夹中的字体文件移动到根目录 (target_dir)，
    并处理文件名冲突。
    """
    print(f"开始扁平化目录 (提取所有字体到根目录)...")
    moved_count = 0

    # 遍历所有子目录
    for root, dirs, files in os.walk(target_dir):
        # 如果当前就是根目录，跳过
        if root == target_dir:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # 只移动字体文件
            if file_ext in FONT_EXTENSIONS:
                target_path = os.path.join(target_dir, file)

                # 如果根目录下已经有同名文件，添加 _1, _2 后缀
                if os.path.exists(target_path):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(os.path.join(target_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")

                try:
                    shutil.move(file_path, target_path)
                    moved_count += 1
                except Exception as e:
                    print(f"移动失败 {file}: {e}")

    return moved_count


def remove_empty_folders(target_dir):
    """递归删除空文件夹"""
    print(f"清理空文件夹...")
    removed_count = 0
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                # 只有当文件夹真的为空时才删除
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    removed_count += 1
            except OSError:
                pass
    return removed_count
