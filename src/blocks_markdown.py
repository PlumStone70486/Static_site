from htmlnode import *
from textnode import *
from inline_markdown import *

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_code(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_code(block):
    block_type = block_to_block_type(block)
    if block_type == block_heading:
        return block_to_html_node_heading(block)
    if block_type == block_quote:
        return block_to_html_node_quote(block)
    if block_type == block_code:
        return block_to_html_node_code(block)
    if block_type == block_unordered_list:
        return block_to_html_node_unordered_list(block)
    if block_type == block_ordered_list:
        return block_to_html_node_ordered_list(block)
    if block_type == block_paragraph:
        return block_to_html_node_paragraph(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_to_html_node_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
     
def block_to_html_node_unordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)
    
def block_to_html_node_ordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
     
def block_to_html_node_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])
     
def block_to_html_node_heading(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)
     
def block_to_html_node_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[2:].strip()
    raise ValueError("Not valid title")
