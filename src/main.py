import os
from shutil import rmtree

from copy_content import copy_content
from generate_page import generate_page_recursive


def main():
    source_dir = os.path.abspath("static")
    target_dir = os.path.abspath("public")

    if os.path.exists(target_dir):
        rmtree(target_dir)
    os.mkdir(target_dir)

    copy_content(source_dir, target_dir)
    generate_page_recursive(
        "content", "template.html", "public")


if __name__ == "__main__":
    main()
