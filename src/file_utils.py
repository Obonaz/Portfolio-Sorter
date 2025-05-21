import os
import shutil
from pathlib import Path

def get_source_files(source_dir: str, excluded_extensions: list[str]) -> list[str]:
    """
    Scans the source_dir (including subdirectories) and returns a list of full file paths,
    ignoring files whose extensions are in the excluded_extensions list (case-insensitive).
    """
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' not found.")

    source_files = []
    excluded_extensions_lower = [ext.lower() for ext in excluded_extensions]

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in excluded_extensions_lower:
                source_files.append(os.path.join(root, file))
    return source_files

def create_target_subdir(target_dir: str, subdir_name: str) -> str:
    """
    Creates a subdirectory named subdir_name inside target_dir.
    If the subdirectory already exists, it should not raise an error.
    Returns the full path to the created or existing subdirectory.
    """
    subdir_path = Path(target_dir) / subdir_name
    try:
        subdir_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {subdir_path}: {e}") # Or raise e
        raise
    return str(subdir_path)

def move_file_to_directory(source_file_path: str, target_dir_path: str) -> None:
    """
    Moves the file from source_file_path to the target_dir_path.
    The destination filename within target_dir_path should be the same as the original filename.
    """
    if not os.path.isfile(source_file_path):
        raise FileNotFoundError(f"Source file '{source_file_path}' not found.")
    if not os.path.isdir(target_dir_path):
        # Attempt to create it if it doesn't exist, or raise an error
        try:
            Path(target_dir_path).mkdir(parents=True, exist_ok=True)
            print(f"Target directory '{target_dir_path}' created.")
        except OSError as e:
            raise OSError(f"Target directory '{target_dir_path}' does not exist and could not be created: {e}")

    base_filename = os.path.basename(source_file_path)
    destination_path = os.path.join(target_dir_path, base_filename)

    try:
        shutil.move(source_file_path, destination_path)
    except Exception as e:
        print(f"Error moving file '{source_file_path}' to '{destination_path}': {e}")
        raise
