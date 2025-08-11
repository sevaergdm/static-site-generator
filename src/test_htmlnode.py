import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a",
                        "google",
                        None,
                        {
                            "href": "https://www.google.com",
                            "target": "some_target"
                        }
                        )
        self.assertEqual(node.props_to_html(),
                         ' href="https://www.google.com" target="some_target"')

    def test_props_to_html_exception(self):
        node = HTMLNode()
        with self.assertRaises(Exception) as context:
            node.props_to_html()
        self.assertEqual(str(context.exception), "No props provided")

    def test_props_to_html_empty_strings(self):
        node = HTMLNode("", "", "", "")
        with self.assertRaises(Exception) as context:
            node.props_to_html()
        self.assertEqual(str(context.exception), "No props provided")

    def test_props_to_html_not_dict(self):
        node = HTMLNode(None, None, None, "string")
        with self.assertRaises(Exception) as context:
            node.props_to_html()
        self.assertEqual(str(context.exception), "No props provided")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_href(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_leaf_to_html_val_error(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A value must be provided")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Google")
        self.assertEqual(node.to_html(), "Google")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_parent_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception),
                         "A list of child nodes must be provided")

    def test_to_html_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "A tag must be provided")

    def test_to_html_parent_with_props(self):
        child_node = LeafNode("p", "This is some text")
        child_node2 = LeafNode("b", "This is some more text")
        parent_node = ParentNode("a", [child_node, child_node2], {
                                 "href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(),
                         '<a href="https://www.google.com"><p>This is some '
                         'text</p><b>This is some more text</b></a>')


if __name__ == "__main__":
    unittest.main()
