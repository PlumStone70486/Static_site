import unittest

from blocks_markdown import *

class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        assert markdown_to_blocks("# Heading\n\nParagraph") == ["# Heading", "Paragraph"]

        assert markdown_to_blocks("  # Heading  \n\n  Paragraph  ") == ["# Heading", "Paragraph"]
            
        assert markdown_to_blocks("# Heading\n\n\n\nParagraph") == ["# Heading", "Paragraph"]
            
        assert markdown_to_blocks("") == []

        assert markdown_to_blocks("Just one block") == ["Just one block"]

if __name__ == "__main__":
    unittest.main()