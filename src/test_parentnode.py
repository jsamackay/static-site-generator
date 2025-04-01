import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()
        self.assertEqual(str(context.exception), "The 'children' parameter is required.")

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node]).to_html()
        self.assertEqual(str(context.exception), "The 'tag' parameter is required.")

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested_structure(self):
        grandchild1 = LeafNode("i", "italic")
        grandchild2 = LeafNode("b", "bold")
        child = ParentNode("p", [grandchild1, grandchild2])
        parent_node = ParentNode("div", [child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><i>italic</i><b>bold</b></p></div>",
        )


if __name__ == "__main__":
    unittest.main()