from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        raise Exception("No nodes to parse")

    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception(f"Invalid markdown: missing closing '{delimiter}'")
            for i in range(len(split_nodes)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    if not old_nodes:
        raise Exception("No nodes to process")

    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images:
            alt_text = images[0][0]
            url = images[0][1]
            sections = node.text.split(f"![{alt_text}]({url})")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            if sections[1]:
                new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    if not old_nodes:
        raise Exception("No nodes to process")

    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links:
            text = links[0][0]
            url = links[0][1]
            sections = node.text.split(f"[{text}]({url})")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            if sections[1]:
                new_nodes.extend(split_nodes_link([TextNode(sections[1], TextType.TEXT)]))
        else:
            new_nodes.append(node)
    return new_nodes
