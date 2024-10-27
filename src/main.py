from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        html_node = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        html_node = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        html_node = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        html_node = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        html_node = LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        html_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Not valid type")

    return html_node

def main():

    node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev"})
    print(node)

    node2 = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
    print(node2)

main()