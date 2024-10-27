import unittest

from textnode import *
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_inline_one_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_inline_two_delimiters(self):
        node = TextNode("This is **bold** and **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_inline_markdown_error(self):
        with self.assertRaises(ValueError):
            node = TextNode("This will raise an *error", TextType.TEXT)
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_inline_adjeacent_delemiters(self):
        node = TextNode("**This** is *text*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected)

    def test_inline_empty_list(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        expected = []
        self.assertEqual(new_nodes, expected)

    def test_inline_double_delimiter(self):
        node = TextNode("This is **bold** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
