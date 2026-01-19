import os
import sys
import time
from src.config import AUTO_CLOSE
from src.archive_utils import extract_and_delete_archives
from src.font_utils import rename_fonts
from src.file_cleaner import clean_non_font_files, remove_empty_folders


def main():
    print("==========================================")
    print("      Font Organizer Utility v2.1")
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

    # 1. 递归解压并清理压缩包
    extract_count = extract_and_delete_archives(work_dir)

    # 2. 清理非字体文件 (如图片、说明文档)
    clean_count = clean_non_font_files(work_dir)

    # 3. 字体识别与重命名
    rename_count = rename_fonts(work_dir)

    # 4. 清理空目录
    folder_count = remove_empty_folders(work_dir)

    print("\n==========================================")
    print("处理完成。统计信息:")
    print(f"解压数量: {extract_count}")
    print(f"清理文件: {clean_count}")
    print(f"重命名数: {rename_count}")
    print("==========================================")

    # 根据配置决定退出逻辑
    if not AUTO_CLOSE:
        input("按回车键退出程序...")
    else:
        # 停留简短时间以便用户确认结果，随后自动退出
        time.sleep(1.5)


if __name__ == "__main__":
    main()