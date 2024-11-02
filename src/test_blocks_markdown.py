import unittest

from blocks_markdown import *
from textnode import *
from htmlnode import *

class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        assert markdown_to_blocks("# Heading\n\nParagraph") == ["# Heading", "Paragraph"]

        assert markdown_to_blocks("  # Heading  \n\n  Paragraph  ") == ["# Heading", "Paragraph"]
            
        assert markdown_to_blocks("# Heading\n\n\n\nParagraph") == ["# Heading", "Paragraph"]
            
        assert markdown_to_blocks("") == []

        assert markdown_to_blocks("Just one block") == ["Just one block"]

    def test_block_to_block(self):
        quote = """> This is one
> This is two
> This is Three
> This is four"""
        ordered_list = """1. This is one
2. This is two
3. This is Three
4. This is four"""
        unordered_list = """* This is one
* This is two
- This is Three
* This is four"""

        code = "```Here are some code, good code etc..```"

        assert block_to_block_type("Paragraph") == block_paragraph

        assert block_to_block_type("#### Heading") == block_heading

        assert block_to_block_type(code) == block_code

        assert block_to_block_type("") == block_paragraph

        assert block_to_block_type(ordered_list) == block_ordered_list

        assert block_to_block_type(quote) == block_quote

        assert block_to_block_type(unordered_list) == block_unordered_list

    def test_markdown_to_html_node_heading(self):
        markdown_heading = "# Heading"
        expected_html_heading = ParentNode("div", [LeafNode("h1", "Heading")])
        result_heading = markdown_to_html_node(markdown_heading)
        self.assertEqual(result_heading, expected_html_heading)

    def test_markdown_to_html_node_paragraph(self):
        markdown_paragraph = "This is a paragraph."
        expected_html_paragraph = ParentNode("div", [LeafNode("p", "This is a paragraph.")])
        result_paragraph = markdown_to_html_node(markdown_paragraph)
        self.assertEqual(result_paragraph, expected_html_paragraph)

    def test_markdown_to_html_node_unordered_list(self):
        markdown_list = "- Item 1\n- Item 2"
        expected_html_list = ParentNode("div", [
            ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")])
        ])
        result_list = markdown_to_html_node(markdown_list)
        self.assertEqual(result_list, expected_html_list)

    def test_markdown_to_html_node_ordered_list(self):
        markdown_list = "1. Item 1\n2. Item 2"
        expected_html_list = ParentNode("div", [
            ParentNode("ol", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")])
        ])
        result_list = markdown_to_html_node(markdown_list)
        self.assertEqual(result_list, expected_html_list)

if __name__ == "__main__":
    unittest.main()