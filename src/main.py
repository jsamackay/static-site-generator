from textnode import TextNode 
from textnode import TextType
from leafnode import LeafNode
import re

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Use regex to split text into parts (images and surrounding text)
        pattern = r"!\[(.*?)\]\((.*?)\)"
        last_end = 0
        for match in re.finditer(pattern, old_node.text):
            start, end = match.span()
            # Add the text before the link as a TextNode
            if start > last_end:
                new_nodes.append(TextNode(old_node.text[last_end:start], TextType.TEXT))
            # Add the link as a TextNode with TextType.LINK
            link_text, url = match.groups()
            new_nodes.append(TextNode(link_text, TextType.IMAGE, url))
            last_end = end
        # Add the remaining text after the last link
        if last_end < len(old_node.text):
            new_nodes.append(TextNode(old_node.text[last_end:], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Use regex to find links and their surrounding text
        pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
        last_end = 0
        for match in re.finditer(pattern, old_node.text):
            start, end = match.span()
            # Add the text before the link as a TextNode
            if start > last_end:
                new_nodes.append(TextNode(old_node.text[last_end:start], TextType.TEXT))
            # Add the link as a TextNode with TextType.LINK
            link_text, url = match.groups()
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_end = end
        # Add the remaining text after the last link
        if last_end < len(old_node.text):
            new_nodes.append(TextNode(old_node.text[last_end:], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(text)), "`", TextType.CODE), "_", TextType.ITALIC), "**", TextType.BOLD)

main()
