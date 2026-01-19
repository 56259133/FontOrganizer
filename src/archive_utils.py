# src/archive_utils.py
import os
import patoolib
from .config import ARCHIVE_EXTENSIONS


def extract_and_delete_archives(target_dir):
    """
    遍历目录，解压所有压缩包并删除源文件
    """
    print(f"始扫描压缩包: {target_dir}")
    extracted_count = 0

    # 使用 walk 遍历，但在解压时要小心修改了目录结构
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in ARCHIVE_EXTENSIONS:
                print(f"   正在解压: {file}")
                try:
                    # 解压到当前所在文件夹
                    patoolib.extract_archive(file_path, outdir=root, verbosity=-1)

                    # 解压成功后删除原文件
                    os.remove(file_path)
                    print(f"已解压并删除: {file}")
                    extracted_count += 1
                except Exception as e:
                    print(f"解压失败 {file}: {e}")

    return extracted_count