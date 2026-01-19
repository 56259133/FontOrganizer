import os
import sys
import time
from src.config import AUTO_CLOSE
from src.archive_utils import extract_and_delete_archives
from src.font_utils import rename_fonts
from src.file_cleaner import clean_non_font_files, remove_empty_folders, flatten_directory


def main():
    print("==========================================")
    print("      Font Organizer Utility v2.2")
    print("==========================================")

    # 初始化工作目录
    default_path = os.path.join(os.getcwd(), 'input_fonts')
    print(f"默认工作路径: {default_path}")

    try:
        user_input = input("请输入目标文件夹路径 (直接回车使用默认路径): ").strip().strip('"')
    except KeyboardInterrupt:
        sys.exit(0)

    work_dir = user_input if user_input else default_path

    # 路径校验
    if not os.path.exists(work_dir):
        if work_dir == default_path:
            try:
                os.makedirs(work_dir)
                print(f"已创建默认文件夹: {work_dir}")
                print("请将待处理的字体文件放入该文件夹后重新运行程序。")
            except OSError as e:
                print(f"创建文件夹失败: {e}")
        else:
            print("错误: 指定的路径不存在。")
        time.sleep(2)
        return

    print(f"\n开始处理目录: {work_dir}\n")

    # 1. 解压所有压缩包
    extract_count = extract_and_delete_archives(work_dir)

    # 2. 清理非字体文件 (图片、txt等)
    clean_count = clean_non_font_files(work_dir)

    # 3. 扁平化处理：把子文件夹里的字体全抓出来放到根目录
    move_count = flatten_directory(work_dir)

    # 4. 字体识别与重命名
    rename_count = rename_fonts(work_dir)

    # 5. 清理剩下的空文件夹
    folder_count = remove_empty_folders(work_dir)

    print("\n==========================================")
    print("处理完成。")
    print(f"   - 解压数量: {extract_count}")
    print(f"   - 提取字体: {move_count}")
    print(f"   - 重命名数: {rename_count}")
    print(f"   - 删空文件夹: {folder_count}")
    print("==========================================")

    if not AUTO_CLOSE:
        input("按回车键退出程序...")
    else:
        time.sleep(1.5)


if __name__ == "__main__":
    main()
