import unittest
from main import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "Here is an image: ![Alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("Alt text", "https://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = (
            "Here is the first image: ![Image1](https://example.com/image1.png) "
            "and here is the second: ![Image2](https://example.com/image2.png)"
        )
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("Image1", "https://example.com/image1.png"),
                ("Image2", "https://example.com/image2.png"),
            ],
        )

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_single(self):
        text = "Here is a link: [Example](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Example", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = (
            "Here is the first link: [Google](https://google.com) "
            "and here is the second: [GitHub](https://github.com)"
        )
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [
                ("Google", "https://google.com"),
                ("GitHub", "https://github.com"),
            ],
        )

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_and_links(self):
        text = (
            "Here is a link: [Example](https://example.com) "
            "and an image: ![Alt text](https://example.com/image.png)"
        )
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertEqual(image_result, [("Alt text", "https://example.com/image.png")])
        self.assertEqual(link_result, [("Example", "https://example.com")])

    def test_extract_multiple_images(self):
        text = (
            "Here is the first image: ![Image1](https://example.com/image1.png) "
            "and here is the second image: ![Image2](https://example.com/image2.png) "
            "and a third image: ![Image3](https://example.com/image3.png)"
        )
        
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("Image1", "https://example.com/image1.png"),
                ("Image2", "https://example.com/image2.png"),
                ("Image3", "https://example.com/image3.png"),
            ],
        )

    def test_extract_multiple_links(self):
        text = (
            "Here is the first link: [Google](https://google.com) "
            "and here is the second link: [GitHub](https://github.com) "
            "and a third link: [StackOverflow](https://stackoverflow.com)"
        )
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [
                ("Google", "https://google.com"),
                ("GitHub", "https://github.com"),
                ("StackOverflow", "https://stackoverflow.com"),
            ],
        )

    def test_extract_mixed_images_and_links(self):
        text = (
            "Here is a link: [Example](https://example.com) "
            "and an image: ![Alt text](https://example.com/image.png) "
            "another link: [GitHub](https://github.com) "
            "and another image: ![Image2](https://example.com/image2.png)"
        )
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertEqual(
            image_result,
            [
                ("Alt text", "https://example.com/image.png"),
                ("Image2", "https://example.com/image2.png"),
            ],
        )
        self.assertEqual(
            link_result,
            [
                ("Example", "https://example.com"),
                ("GitHub", "https://github.com"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image_single(self):
        old_nodes = [TextNode("Here is an image: ![Alt text](https://example.com/image.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Here is an image: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.png")

    def test_split_nodes_image_multiple(self):
        old_nodes = [
            TextNode(
                "Here is the first image: ![Image1](https://example.com/image1.png) "
                "and here is the second image: ![Image2](https://example.com/image2.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Here is the first image: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Image1")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image1.png")
        self.assertEqual(new_nodes[2].text, " and here is the second image: ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "Image2")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://example.com/image2.png")

    def test_split_nodes_link_single(self):
        old_nodes = [TextNode("Here is a link: [Example](https://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Here is a link: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Example")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")

    def test_split_nodes_link_multiple(self):
        old_nodes = [
            TextNode(
                "Here is the first link: [Google](https://google.com) "
                "and here is the second link: [GitHub](https://github.com)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Here is the first link: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Google")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://google.com")
        self.assertEqual(new_nodes[2].text, " and here is the second link: ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "GitHub")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://github.com")

    def test_split_nodes_image_and_text(self):
        old_nodes = [
            TextNode(
                "Text before image ![Alt text](https://example.com/image.png) text after image.",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text before image ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
        self.assertEqual(new_nodes[2].text, " text after image.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_link_and_text(self):
        old_nodes = [
            TextNode(
                "Text before link [Example](https://example.com) text after link.",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text before link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "Example")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " text after link.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text.")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text.")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_italic_text(self):
        text = "This is _italic_ text."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text.")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_code_text(self):
        text = "This is `code` text."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text.")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_links(self):
        text = "This is a [link](https://example.com)."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, ".")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_images(self):
        text = "This is an image: ![Alt text](https://example.com/image.png)."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is an image: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image.png")
        self.assertEqual(result[2].text, ".")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_combined_formatting(self):
        text = "This is **bold**, _italic_, `code`, [link](https://example.com), and ![image](https://example.com/image.png)."
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, ", ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, ", ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, ", ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "link")
        self.assertEqual(result[7].text_type, TextType.LINK)
        self.assertEqual(result[7].url, "https://example.com")
        self.assertEqual(result[8].text, ", and ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "image")
        self.assertEqual(result[9].text_type, TextType.IMAGE)
        self.assertEqual(result[9].url, "https://example.com/image.png")
        self.assertEqual(result[10].text, ".")
        self.assertEqual(result[10].text_type, TextType.TEXT)

    def test_complex_text_with_all_formats(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        result = text_to_textnodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(result), 10)

        # Assertions for each part of the text
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[1].text_type, TextType.BOLD)

        self.assertEqual(result[2].text, " with an ")
        self.assertEqual(result[2].text_type, TextType.TEXT)

        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

        self.assertEqual(result[4].text, " word and a ")
        self.assertEqual(result[4].text_type, TextType.TEXT)

        self.assertEqual(result[5].text, "code block")
        self.assertEqual(result[5].text_type, TextType.CODE)

        self.assertEqual(result[6].text, " and an ")
        self.assertEqual(result[6].text_type, TextType.TEXT)

        self.assertEqual(result[7].text, "obi wan image")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")

        self.assertEqual(result[8].text, " and a ")
        self.assertEqual(result[8].text_type, TextType.TEXT)

        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "https://boot.dev")


if __name__ == "__main__":
    unittest.main()
