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
