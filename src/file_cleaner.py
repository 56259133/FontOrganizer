# src/file_cleaner.py
import os
from .config import FONT_EXTENSIONS, ARCHIVE_EXTENSIONS, IGNORE_FILES


def clean_non_font_files(target_dir):
    """删除非字体、非压缩包的文件"""
    print(f"开始清理杂项文件...")
    deleted_count = 0

    for root, dirs, files in os.walk(target_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            # 如果不是字体，也不是压缩包（虽然压缩包应该已经被删了），且不在忽略列表中
            if (file_ext not in FONT_EXTENSIONS) and \
                    (file_ext not in ARCHIVE_EXTENSIONS) and \
                    (file.lower() not in IGNORE_FILES):

                try:
                    os.remove(file_path)
                    print(f"删除垃圾文件: {file}")
                    deleted_count += 1
                except Exception as e:
                    print(f"删除失败: {e}")

    return deleted_count


def remove_empty_folders(target_dir):
    """递归删除空文件夹"""
    print(f"清理空文件夹...")
    removed_count = 0
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                if not os.listdir(dir_path):  # 目录为空
                    os.rmdir(dir_path)
                    removed_count += 1
            except OSError:
                pass
    return removed_count