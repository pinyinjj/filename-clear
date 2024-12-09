import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import trash_info

def modify_filename(file_name, patterns_to_remove):
    for pattern in patterns_to_remove:
        file_name = re.sub(pattern, '', file_name)
    return file_name

def process_file(root, file, patterns_to_remove, files_to_remove):
    original_file_path = os.path.join(root, file)

    if file in files_to_remove:
        try:
            os.remove(original_file_path)
            print(f"Deleted: {original_file_path}")
            return
        except Exception as e:
            print(f"Error deleting {original_file_path}: {e}")
        return

    modified_name = modify_filename(file, patterns_to_remove)
    modified_file_path = os.path.join(root, modified_name)

    if original_file_path != modified_file_path:
        try:
            os.rename(original_file_path, modified_file_path)
            print(f'Renamed: {original_file_path} -> {modified_file_path}')
        except Exception as e:
            print(f"Error renaming {original_file_path}: {e}")

def rename_files_in_directory(directory, patterns_to_remove, files_to_remove, num_threads=4):
    """遍历目录中的文件并并发地重命名"""
    compiled_patterns = [re.compile(pattern) for pattern in patterns_to_remove]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for root, dirs, files in os.walk(directory):
            print(f"Entering directory: {root}")  # 打印当前进入的目录路径
            for file in files:
                try:
                    executor.submit(process_file, root, file, compiled_patterns, files_to_remove)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    directory_path = base_dir
    print(f"Directory to process: {directory_path}")

    start_time = time.time()

    rename_files_in_directory(directory_path, trash_info.patterns_to_remove, trash_info.files_to_remove)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Process completed in {elapsed_time:.2f} seconds")
    input("Press any key to exit...")
