import os
from htmlnode import *
from blocks_markdown import *
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown_file = file.read()
        html_title = extract_title(markdown_file)
        html_node = markdown_to_html_node(markdown_file)
        html_text = html_node.to_html()

    with open(template_path, "r") as file:
        template_file = file.read()
        template_file = template_file.replace("{{ Title }}", html_title)
        template_file = template_file.replace("{{ Content }}", html_text)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path = os.listdir(dir_path_content)

    for name in dir_path:
        full_path = os.path.join(dir_path_content, name) 
        if os.path.isfile(full_path):
            source_path = Path(full_path)
            dest_file = source_path.with_suffix(".html").name
            new_dest_path = os.path.join(dest_dir_path, dest_file)
            generate_page(str(source_path), template_path, new_dest_path)

        if os.path.isdir(full_path):
            new_dest_path = os.path.join(dest_dir_path, name)
            os.makedirs(new_dest_path, exist_ok=True)
            generate_pages_recursive(full_path, template_path, new_dest_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Not valid title")