from htmlnode import *

block_heading = "heading"
block_code = "code"
block_quote = "quote"
block_unordered_list = "unordered list"
block_ordered_list = "ordered list"
block_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    block = markdown.split("\n\n")
    new_block = []
    new_string = ""
    for i in block:
        new_string = i.strip()
        if new_string != "":
            new_block.append(new_string)
    return new_block

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_heading
    
    in_code_block = False
    lines = block.split("\n")
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
    if in_code_block:
        return block_code
  
    if all(line.startswith("> ") for line in lines):
            return block_quote
        
    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
            return block_unordered_list
        
    number = 1
    for line in lines:
        if not line.startswith(f"{number}. "):
            break
        number += 1
    else:
        return block_ordered_list
        
    return block_paragraph

def block_to_html_node_quote(block):
    return LeafNode("blockquote", block[2:])
     
def block_to_html_node_unordered_list(block):
    list_items = [LeafNode("li", line[2:].strip())for line in block.splitlines()]
    return ParentNode("ul", list_items)
    
def block_to_html_node_ordered_list(block):
    list_items = [LeafNode("li", line.split(" ", 1)[1].strip())for line in block.splitlines()]
    return ParentNode("ol", list_items)
     
def block_to_html_node_code(block):
    code_content = "\n".join(line.strip() for line in block.splitlines())
    code_node = LeafNode("code", code_content)
    return LeafNode("pre", code_node)
     
def block_to_html_node_heading(block):
    if block.startswith("# "):
        return LeafNode("h1", block[2:].strip())
    if block.startswith("## "):
        return LeafNode("h2", block[3:].strip())
    if block.startswith("### "):
        return LeafNode("h3", block[4:].strip())
    if block.startswith("#### "):
        return LeafNode("h4", block[5:].strip())
    if block.startswith("##### "):
        return LeafNode("h5", block[6:].strip())
    if block.startswith("###### "):
        return LeafNode("h6", block[7:].strip())
    else:
        raise ValueError("Block does not match any known heading format.")
     
def block_to_html_node_paragraph(block):
    new_block = block.strip()
    return LeafNode("p", new_block)
     
def markdown_to_html_node(markdown):
    new_list = []
    new_block = markdown_to_blocks(markdown)
    for block in new_block:
        block_type = block_to_block_type(block)
        if block_type == block_heading:
            html_node = block_to_html_node_heading(block)
        elif block_type == block_quote:
            html_node = block_to_html_node_quote(block)
        elif block_type == block_code:
            html_node = block_to_html_node_code(block)
        elif block_type == block_unordered_list:
            html_node = block_to_html_node_unordered_list(block)
        elif block_type == block_ordered_list:
            html_node = block_to_html_node_ordered_list(block)
        elif block_type == block_paragraph:
            html_node = block_to_html_node_paragraph(block)
        new_list.append(html_node)
    return ParentNode("div", new_list)
