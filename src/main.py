from textnode import *
from htmlnode import *

def main():
    test = TextNode("This is a node", TextType.BOLD, "https://boot.dev")
    print(test)

    node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev"})
    print(node)

main()