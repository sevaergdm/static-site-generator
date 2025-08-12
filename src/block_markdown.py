from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for text in split_markdown:
        stripped_text = text.strip()
        if stripped_text != "":
            blocks.append(stripped_text)
    return blocks


def block_to_block_type(block):
    pattern = r"#{1,6} "
    if re.match(pattern, block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.lstrip().startswith(">"):
        block_lines = block.split("\n")
        for line in block_lines:
            if line.strip() == "":
                continue
            if not line.lstrip().startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.lstrip().startswith("- "):
        block_lines = block.split("\n")
        for line in block_lines:
            if line.strip() == "":
                continue
            if not line.lstrip().startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        block_lines = block.split("\n")
        for i in range(len(block_lines)):
            if not block_lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("# "):
            return line.split("#", 1)[1]
    raise Exception("No level 1 header present in the text")
