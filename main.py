import os
from shutil import rmtree

from src.copy_content import copy_content
from src.generate_page import generate_page


def main():
    source_dir = os.path.abspath("static")
    target_dir = os.path.abspath("public")

    if os.path.exists(target_dir):
        rmtree(target_dir)
    os.mkdir(target_dir)

    copy_content(source_dir, target_dir)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
