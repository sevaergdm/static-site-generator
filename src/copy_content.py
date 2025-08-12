import os
from shutil import copy


def copy_content(source_directory, target_directory):
    abs_path_source = os.path.abspath(source_directory)
    abs_path_target = os.path.abspath(target_directory)

    if not os.path.exists(abs_path_source):
        raise Exception("Error: Source directory does not exist")

    for item in os.listdir(abs_path_source):
        path = os.path.join(abs_path_source, item)
        print(f"Copying {path} to {abs_path_target}")
        try:
            if os.path.isfile(path):
                copy(path, abs_path_target)
                print("Copy successful!")
            elif os.path.isdir(path):
                new_target = os.path.join(abs_path_target, item)
                if not os.path.exists(new_target):
                    print(f"Creating directory: {new_target}")
                    os.mkdir(new_target)
                copy_content(path, new_target)
        except Exception as e:
            raise Exception(f"Error: an exception occurred: {e}")
