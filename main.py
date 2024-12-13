import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import trash_info


def process_file(root, file, files_to_remove_set):
    """
    Deletes the file if its name is in the files_to_remove_set.
    """
    original_file_path = os.path.join(root, file)

    if file in files_to_remove_set:
        try:
            os.remove(original_file_path)
            print(f"Deleted: {original_file_path}")
        except Exception as e:
            print(f"Error deleting {original_file_path}: {e}")


def delete_files_in_directory(directory, files_to_remove, num_threads=4):
    """
    Traverses the directory and deletes files that match any name in files_to_remove.

    Args:
        directory (str): The root directory to start deleting files from.
        files_to_remove (list): A list of exact filenames to delete.
        num_threads (int): Number of threads to use for concurrent deletion.
    """
    # Convert the list to a set for faster lookup
    files_to_remove_set = set(files_to_remove)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for root, dirs, files in os.walk(directory):
            print(f"Entering directory: {root}")  # Logs the current directory being processed
            for file in files:
                executor.submit(process_file, root, file, files_to_remove_set)


if __name__ == "__main__":
    # Determine the base directory based on how the script is executed
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    directory_path = base_dir
    print(f"Directory to process: {directory_path}")

    start_time = time.time()

    # Call the deletion function with the specified files to remove
    delete_files_in_directory(directory_path, trash_info.files_to_remove)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Process completed in {elapsed_time:.2f} seconds")
    input("Press any key to exit...")
