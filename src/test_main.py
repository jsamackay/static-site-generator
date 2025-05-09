import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = "# This is a title"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title")

    def test_title_with_extra_spaces(self):
        markdown = "#    This is a title with spaces    "
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title with spaces")

    def test_title_without_hash(self):
        markdown = "This is a title without hash"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title without hash")

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown content is empty")

    def test_markdown_with_multiple_lines(self):
        markdown = "# This is the title\nThis is the body of the markdown."
        result = extract_title(markdown)
        self.assertEqual(result, "This is the title")

    def test_markdown_with_no_title(self):
        markdown = "\n\nThis is the body of the markdown."
        result = extract_title(markdown)
        self.assertEqual(result, "")

    def test_markdown_with_only_hash(self):
        markdown = "#"
        result = extract_title(markdown)
        self.assertEqual(result, "")

    def test_markdown_with_multiple_hashes(self):
        markdown = "### This is a title with multiple hashes"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title with multiple hashes")


if __name__ == "__main__":
    unittest.main()