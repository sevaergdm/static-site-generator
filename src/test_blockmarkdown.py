import textwrap
import unittest

from block_markdown import (BlockType, block_to_block_type, extract_title,
                            markdown_to_blocks)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` "
                "here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_heading(self):
        md = textwrap.dedent("""
        # This is a heading

        - Followed
        - by
        - a
        - list

        With some more **paragraph** _text_
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "# This is a heading",
                "- Followed\n- by\n- a\n- list",
                "With some more **paragraph** _text_",
            ],
            blocks
        )

    def test_block_to_block_type(self):
        md = "### This is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_bad_ordered_list(self):
        md = textwrap.dedent("""
        1. This is the first item
        3. This is the third item
        4. This is the fourth item
        """)
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md = textwrap.dedent("""
        > This is a quote
        > From someone
        > I don't know who
        """)
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = textwrap.dedent("""
        - This is
        - an unordered
        - list
        """)
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_extract_title(self):
        md = textwrap.dedent("""
        # This is a single line header
        """)
        title = extract_title(md)
        self.assertEqual(title, " This is a single line header")

    def test_extract_title_multiline(self):
        md = textwrap.dedent("""
        # This is my main title

        This is just some regular text

        ## This is an h2 header
        """)
        title = extract_title(md)
        self.assertEqual(title, " This is my main title")

    def test_extract_title_no_title(self):
        md = textwrap.dedent("""
        This is just some text

        That doesn't have a title
        """)
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception),
                         "No level 1 header present in the text")


if __name__ == "__main__":
    unittest.main()
