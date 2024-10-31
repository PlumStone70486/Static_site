import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        new_text = old_node.text.split(delimiter)
        if len(new_text) % 2 == 0:
            raise ValueError("Invalid markdown")
        for i in range(len(new_text)):
            if new_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(new_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(new_text[i], text_type))
        new_nodes.extend(split_nodes)  
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            images = extract_markdown_images(old_node.text)
            content = old_node.text
            split_nodes = []
            for alt, link in images:
                sections = content.split(f"![{alt}]({link})", 1)
                if sections[0]:
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(alt, TextType.IMAGE, link))
                content = sections[1]
            if content:
                split_nodes.append(TextNode(content, TextType.TEXT))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(old_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            links = extract_markdown_links(old_node.text)
            content = old_node.text
            split_nodes = []
            for link_text, link in links:
                sections = content.split(f"[{link_text}]({link})", 1)
                if sections[0]:
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(link_text, TextType.LINK, link))
                content = sections[1]
            if content:
                split_nodes.append(TextNode(content, TextType.TEXT))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(old_node)
    return new_nodes
