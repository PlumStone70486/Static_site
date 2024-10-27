import unittest

from textnode import *
from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is not a text node", TextType.ITALIC, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("Test one", TextType.BOLD)
        node2 = TextNode("Test two", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a textnode", TextType.ITALIC)
        node2 = TextNode("This is a textnode", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_eq (self):
        props = {
            "href": "https://boot.dev",
            "target": "blank"
        }
        node = HTMLNode("h1", "This is a test", None,  props)
        expected = ' href="https://boot.dev" target="blank"'
        self.assertEqual(node.props_to_html(), expected)
        
    def test_props_to_html_not_eq (self):
        props = {
            "href": "https://boot.dev",
            "target": "blank"
        }
        node = HTMLNode("h1", "This is a test", None,  props)
        expected = ' href="https://google.com" target="blank"'
        self.assertNotEqual(node.props_to_html(), expected)

    def test_value(self):
        node = HTMLNode("h1", "This is a test", None, None)
        expected = "This is a test"
        self.assertEqual(node.value, expected)

    def test_tag(self):
        node = HTMLNode("h1", "This is a test", None, None)
        expected = "h1"
        self.assertEqual(node.tag, expected)

    def test_props_empty(self):
        node = HTMLNode("h1", "This is a test", None, None)
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_eq(self):
        props = {
            "href": "https://boot.dev",
        }
        node = LeafNode("a", "Link to boot.dev", props)
        expected = '<a href="https://boot.dev">Link to boot.dev</a>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Text")
        expected = "Text"
        self.assertEqual(node.to_html(), expected)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", [])

    def test_to_html_eq(self):
        list_node = [
            LeafNode("b", "This is bold text"),
            LeafNode("i", "This is italic text"),
            LeafNode(None, "This is normal text"),
        ]
        node = ParentNode("p", list_node)
        expected = "<p><b>This is bold text</b><i>This is italic text</i>This is normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_url(self):
        list_node = [
            LeafNode("b", "This is bold text", {"href": "https://boot.dev"}),
            LeafNode("i", "This is italic text"),
            LeafNode(None, "This is normal text"),
        ]
        node = ParentNode("p", list_node)
        expected = '<p><b href="https://boot.dev">This is bold text</b><i>This is italic text</i>This is normal text</p>'
        self.assertEqual(node.to_html(), expected)


class TextToHTML(unittest.TestCase):
    def test_text_to_node_to_html_node_text(self):
        node = TextNode("This is just text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is just text")

    def test_text_to_node_to_html_node_bold(self):
        node = TextNode("This text is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This text is bold")

    def test_text_to_node_to_html_node_italic(self):
        node = TextNode("This text is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This text is italic")

    def test_text_to_node_to_html_node_code(self):
        node = TextNode("This text is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This text is code")

    def test_text_to_node_to_html_node_link(self):
        node = TextNode("This text is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This text is a link")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_text_to_node_to_html_node_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev", "alt": "alt text"})

    def test_text_to_node_to_html_node_error(self):
        with self.assertRaises(Exception):
            node = TextNode(None, None)
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
