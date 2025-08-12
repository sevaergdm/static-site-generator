from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if not self.props or not isinstance(self.props, dict):
            raise Exception("No props provided")

        for key in self.props:
            string += (f' {key}="{self.props[key]}"')
        return string

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLnode({self.tag}, {self.value}, \
        {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("A value must be provided")

        if self.tag is None:
            return self.value
        else:
            if self.props is not None:
                text_props = self.props_to_html()
            else:
                text_props = ""
            return f'<{self.tag}{text_props}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A tag must be provided")
        if self.children is None:
            raise ValueError("A list of child nodes must be provided")

        if self.props is not None:
            text_props = self.props_to_html()
        else:
            text_props = ""

        string = ""
        for child in self.children:
            string += child.to_html()

        return f"<{self.tag}{text_props}>{string}</{self.tag}>"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img",
                            "",
                            {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextType not recognized")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    count = len(block) - len(block.lstrip("#"))
    text = block.lstrip("#").lstrip()
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)


def code_to_html_node(block):
    text = block.strip("```").lstrip("\n")
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [html_node])])


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line.lstrip().split(" ", 1)[1]
        line_children = text_to_children(text)
        li_node = ParentNode("li", line_children)
        children.append(li_node)
    return ParentNode("ol", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line.lstrip().lstrip("*-+").lstrip()
        line_children = text_to_children(text)
        li_node = ParentNode("li", line_children)
        children.append(li_node)
    return ParentNode("ul", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        text = line.lstrip().split(">", 1)[1].lstrip()
        quote_lines.append(text)
    full_quote = " ".join(quote_lines)
    children = text_to_children(full_quote)
    return ParentNode("blockquote", children)
