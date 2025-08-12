import unittest

from htmlnode import HTMLNode
from inline_markdown import (extract_markdown_images, extract_markdown_links,
                             split_nodes_delimiter, split_nodes_image,
                             split_nodes_link, text_to_textnodes)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        old_nodes = [TextNode("This is some **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_unmatched_delim(self):
        old_nodes = [TextNode("This is some _italic text", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(str(context.exception),
                         "Invalid markdown: missing closing '_'")

    def test_mixed_nodes(self):
        old_nodes = [HTMLNode("p", "some value"), TextNode(
            "This is some `code`", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                HTMLNode("p", "some value"),
                TextNode("This is some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("", TextType.TEXT)
            ],
            new_nodes
        )

    def test_bold_and_italic(self):
        old_nodes = [
            TextNode("This is some _italic_ and **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_extract_images_multiple(self):
        matches = extract_markdown_images(
            "Here is one: ![image](https://someimage.com/someplace) and "
            "here is another: ![image2](https://someimage.com/anotherplace)"
        )
        self.assertListEqual(
            [
                ("image", "https://someimage.com/someplace"),
                ("image2", "https://someimage.com/anotherplace"),
            ],
            matches
        )

    def test_extract_images_no_match(self):
        matches = extract_markdown_images(
            "Here is some text without any markdown formatting"
        )
        self.assertListEqual([], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is a link to [Google](https://www.google.com)"
        )
        self.assertListEqual(
            [
                ("Google", "https://www.google.com")
            ],
            matches
        )

    def test_extract_links_multiple(self):
        matches = extract_markdown_links(
            "[Here](https://www.google.com) is a link to Google. "
            "[This](https://www.yahoo.com) is a link to Yahoo"
        )
        self.assertListEqual(
            [
                ("Here", "https://www.google.com"),
                ("This", "https://www.yahoo.com"),
            ],
            matches
        )

    def test_extract_links_no_match(self):
        matches = extract_markdown_links(
            "Here is some text with no links"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text without an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_multiple_nodes_images(self):
        old_nodes = [
            TextNode(
                "This is text with an ![image](https://www.someimage.com)",
                TextType.TEXT),
            TextNode(
                "This is some other text with another "
                "![image](https://www.anotherimage.com)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.someimage.com"),
                TextNode("This is some other text with another ",
                         TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://www.anotherimage.com")
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and "
            "another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode("This is text without a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_multiple_nodes_links(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://www.someimage.com)",
                TextType.TEXT),
            TextNode(
                "This is some other text with another "
                "[link](https://www.anotherimage.com)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.someimage.com"),
                TextNode("This is some other text with another ",
                         TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.anotherimage.com")
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` " \
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and " \
            "a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_no_formats(self):
        text = "This is just some plain text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just some plain text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes_unclosed_delimiter(self):
        text = "This text is _missing a closing delimiter"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception),
                         "Invalid markdown: missing closing '_'")


if __name__ == "__main__":
    unittest.main()
