from textnode import *
from htmlnode import *

def main():


    node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev"})
    print(node)

    node2 = LeafNode("Click me!", "a", {"href": "https://boot.dev"})
    print(node2)

main()