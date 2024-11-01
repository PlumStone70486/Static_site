def markdown_to_blocks(markdown):
    block = markdown.split("\n\n")
    new_block = []
    new_string = ""
    for i in block:
        new_string = i.strip()
        if new_string != "":
            new_block.append(new_string)
    return new_block

def test_markdown_to_blocks():
    # Test basic block separation
    assert markdown_to_blocks("# Heading\n\nParagraph") == ["# Heading", "Paragraph"]
    
    # Test extra whitespace
    assert markdown_to_blocks("  # Heading  \n\n  Paragraph  ") == ["# Heading", "Paragraph"]
    
    # Test multiple newlines
    assert markdown_to_blocks("# Heading\n\n\n\nParagraph") == ["# Heading", "Paragraph"]
    
    # Test empty document
    assert markdown_to_blocks("") == []
    
    # Test single block
    assert markdown_to_blocks("Just one block") == ["Just one block"]

    print("All tests passed!")

# Run the tests
test_markdown_to_blocks()