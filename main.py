import os
import re
from concurrent.futures import ThreadPoolExecutor
import trash_info
import time  # Import the time module for measuring execution time

def modify_filename(file_name, patterns_to_remove):
    """使用预编译的正则表达式批量删除匹配的字符串"""
    for pattern in patterns_to_remove:
        file_name = re.sub(pattern, '', file_name)
    return file_name


def process_file(root, file, patterns_to_remove, files_to_remove):
    """处理单个文件并执行重命名"""
    original_file_path = os.path.join(root, file)  # 获取原始文件路径
    print(file)
    # Check if the file is in the list of files to remove
    if file in files_to_remove:
        print(f"Attempting to delete: {original_file_path}")
        try:
            os.remove(original_file_path)  # 删除文件
            print(f"Deleted: {original_file_path}")
        except PermissionError:
            print(f"Permission denied: {original_file_path}")
        except FileNotFoundError:
            print(f"File not found: {original_file_path}")
        except Exception as e:
            print(f"Error deleting {original_file_path}: {e}")
        return  # Skip renaming after deleting the file

    modified_name = modify_filename(file, patterns_to_remove)  # 修改文件名
    modified_file_path = os.path.join(root, modified_name)  # 获取修改后的文件路径

    if original_file_path != modified_file_path:  # 确保文件名修改了
        try:
            os.rename(original_file_path, modified_file_path)  # 执行重命名操作
            print(f'Renamed: {original_file_path} -> {modified_file_path}')  # 输出文件重命名的消息
        except Exception as e:
            print(f"Error renaming {original_file_path}: {e}")


def rename_files_in_directory(directory, patterns_to_remove, files_to_remove, num_threads=4):
    """遍历目录中的文件并并发地重命名"""
    # 编译正则表达式，避免重复编译
    compiled_patterns = [re.compile(pattern) for pattern in patterns_to_remove]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for root, dirs, files in os.walk(directory):
            for file in files:
                try:
                    # Submit the file processing task to the executor
                    executor.submit(process_file, root, file, compiled_patterns, files_to_remove)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")


if __name__ == "__main__":
    start_time = time.time()  # Start the timer

    # 获取当前脚本所在的目录路径
    directory_path = os.path.dirname(os.path.realpath(__file__))
    print(f"Directory to process: {directory_path}")

    # 逐个处理文件并重命名
    rename_files_in_directory(directory_path, trash_info.patterns_to_remove, trash_info.files_to_remove)

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Process completed in {elapsed_time:.2f} seconds")  # Print the elapsed time
