import os
import shutil
from textnode import *
from htmlnode import *
from inline_markdown import *
from blocks_markdown import *

def copy_static():
    src = "/home/tsbg/workspace/github.com/PlumStone70486/static_site_generator/static"
    dest = "/home/tsbg/workspace/github.com/PlumStone70486/static_site_generator/public"
    shutil.rmtree(dest, ignore_errors=True)
    os.mkdir(dest)
    return copy_files(src, dest)

def copy_files(src, dest):
    files = os.listdir(src)
    for file in files:
        full_path = os.path.join(src, file)
        if os.path.isfile(full_path):
            print(f"Copying file: {full_path} to {dest}")
            shutil.copy(full_path, dest)
        if os.path.isdir(full_path):
            new_src = os.path.join(src, file)
            new_dest = os.path.join(dest, file)
            print(f"Processing directory: {full_path}")
            os.mkdir(new_dest)
            copy_files(new_src, new_dest)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(from_path, "r") as file:
        markdown_file = file.read()
        html_title = extract_title(markdown_file)
        html_node = markdown_to_html_node(markdown_file)
        html_text = html_node.to_html()

    with open(template_path, "r") as file:
        template_file = file.read()
        template_file = template_file.replace("{{ Title }}", html_title)
        template_file = template_file.replace("{{ Content }}", html_text)

    with open(dest_path, "w") as file:
        file.write(template_file)
    

def main():

    node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev"})
    print(node)

    node2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
    print(node2)

    copy_static()
    generate_page("/home/tsbg/workspace/github.com/PlumStone70486/static_site_generator/content/index.md",
                  "/home/tsbg/workspace/github.com/PlumStone70486/static_site_generator/template.html",
                  "/home/tsbg/workspace/github.com/PlumStone70486/static_site_generator/public/index.html")

main()