import os
import shutil
from textnode import *
from htmlnode import *
from inline_markdown import *
from blocks_markdown import *
from generate_page import *

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

def main():

    node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev"})
    print(node)

    node2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
    print(node2)

    copy_static()
    generate_pages_recursive("content", "template.html", "public")

main()