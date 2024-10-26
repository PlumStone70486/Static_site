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

if __name__ == "__main__":
    unittest.main()
