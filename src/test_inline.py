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

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_link_and_image(self):
        text = "This is a text with an a link [to boot dev](https://boot.dev) and an image ![boots the bear](boots.jpg)"
        result_link = extract_markdown_links(text)
        result_image = extract_markdown_images(text)
        self.assertEqual(result_link, [("to boot dev", "https://boot.dev")])
        self.assertEqual(result_image, [("boots the bear", "boots.jpg")])

    def test_extract_link_empty(self):
        text = "This is a text with an a link [](https://boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "https://boot.dev")])

    def test_split_nodes_image(self):
        old_nodes = [TextNode(
            "This is some text with an image ![logo](http://example.com/logo.png) right here.",
            TextType.TEXT
        )]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
        TextNode("This is some text with an image ", TextType.TEXT),
        TextNode("logo", TextType.IMAGE, "http://example.com/logo.png"),
        TextNode(" right here.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_images(self):
        old_nodes = [TextNode(
            "This is some text with an image ![logo](http://example.com/logo.png) right here and one ![logo](http://example.com/logo.jpg) right here.",
            TextType.TEXT
        )]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
        TextNode("This is some text with an image ", TextType.TEXT),
        TextNode("logo", TextType.IMAGE, "http://example.com/logo.png"),
        TextNode(" right here and one ", TextType.TEXT),
        TextNode("logo", TextType.IMAGE, "http://example.com/logo.jpg"),
        TextNode(" right here.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link(self):
        old_nodes = [TextNode(
            "This is a link [to boot dev](https://boot.dev) a good website.",
            TextType.TEXT
        )]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
        TextNode("This is a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://boot.dev"),
        TextNode(" a good website.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_links(self):
        old_nodes = [TextNode(
            "This is a link [to boot dev](https://boot.dev) a good website and a link [to google](https://google.com) an ok website.",
            TextType.TEXT
        )]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
        TextNode("This is a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://boot.dev"),
        TextNode(" a good website and a link ", TextType.TEXT),
        TextNode("to google", TextType.LINK, "https://google.com"),
        TextNode(" an ok website.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_to_nodes(self):
        old_nodes = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(old_nodes)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()
