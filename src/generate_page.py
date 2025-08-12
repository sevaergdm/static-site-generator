import os

from block_markdown import extract_title
from htmlnode import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")

    abs_from_path = os.path.abspath(from_path)
    abs_template_path = os.path.abspath(template_path)
    abs_dest_path = os.path.abspath(dest_path)

    with open(abs_from_path, "r") as f:
        markdown = f.read()

    with open(abs_template_path, "r") as f:
        template = f.read()

    converted_markdown = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", converted_markdown)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="', f'src="{basepath}')

    dest_dir_path = os.path.dirname(abs_dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(abs_dest_path, "w") as f:
        f.write(template)


def generate_page_recursive(dir_path_content,
                            template_path,
                            dest_dir_path,
                            basepath="/"):
    abs_dir_path_content = os.path.abspath(dir_path_content)
    abs_template_path = os.path.abspath(template_path)
    abs_dest_dir_path = os.path.abspath(dest_dir_path)

    content_list = os.listdir(abs_dir_path_content)
    for item in content_list:
        path = os.path.join(abs_dir_path_content, item)
        if os.path.isfile(path):
            item_name = os.path.splitext(item)[0]
            item_html = item_name + ".html"
            output_path = os.path.join(abs_dest_dir_path, item_html)
            generate_page(path, abs_template_path, output_path)
        elif os.path.isdir(path):
            new_target = os.path.join(abs_dest_dir_path, item)
            if not os.path.exists(new_target):
                os.mkdir(new_target)
            generate_page_recursive(
                path, abs_template_path, new_target, basepath)
