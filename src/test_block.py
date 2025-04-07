import unittest
from block import block_to_block_type, BlockType, markdown_to_blocks


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        code_block = "```\nCode block\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_quote_block(self):
        quote_block = "> This is a quote\n> Another line of the quote"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_unordered_list(self):
        unordered_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(unordered_list), BlockType.ULIST)

    def test_ordered_list(self):
        ordered_list = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(ordered_list), BlockType.OLIST)

    def test_paragraph(self):
        paragraph = "This is a normal paragraph with no special formatting."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        mixed_content = "# Heading\n- Item 1\n1. First item"
        self.assertEqual(block_to_block_type(mixed_content), BlockType.HEADING)

    def test_invalid_ordered_list(self):
        invalid_ordered_list = "1. First item\n3. Second item\n2. Third item"
        self.assertEqual(block_to_block_type(invalid_ordered_list), BlockType.PARAGRAPH)

    def test_empty_block(self):
        empty_block = ""
        self.assertEqual(block_to_block_type(empty_block), BlockType.PARAGRAPH)

    
    def test_single_block(self):
        markdown = "This is a single block of text."
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "This is a single block of text.")

    def test_multiple_blocks(self):
        markdown = (
            "This is the first block.\n\n"
            "This is the second block.\n\n"
            "This is the third block."
        )
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "This is the first block.")
        self.assertEqual(result[1], "This is the second block.")
        self.assertEqual(result[2], "This is the third block.")

    def test_empty_lines(self):
        markdown = (
            "This is the first block.\n\n"
            "\n\n"
            "This is the second block.\n\n"
            "\n\n"
            "This is the third block."
        )
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "This is the first block.")
        self.assertEqual(result[1], "This is the second block.")
        self.assertEqual(result[2], "This is the third block.")

    def test_no_blocks(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 0)

    def test_blocks_with_whitespace(self):
        markdown = (
            "   This is the first block.   \n\n"
            "   This is the second block.   \n\n"
            "   This is the third block.   "
        )
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "This is the first block.")
        self.assertEqual(result[1], "This is the second block.")
        self.assertEqual(result[2], "This is the third block.")

    def test_complex_markdown(self):
        markdown = (
            "This is **bold** text.\n\n"
            "This is _italic_ text.\n\n"
            "This is a [link](https://example.com).\n\n"
            "This is an ![image](https://example.com/image.png)."
        )
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "This is **bold** text.")
        self.assertEqual(result[1], "This is _italic_ text.")
        self.assertEqual(result[2], "This is a [link](https://example.com).")
        self.assertEqual(result[3], "This is an ![image](https://example.com/image.png).")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()