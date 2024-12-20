class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value,  props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        if props is None:
            props = {}
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if children == [] or children is None:
            raise ValueError("No HTML child")

    def to_html(self):
        if self.tag is None:
            raise ValueError("No HTML tag")
        else:
            result = ""
            for child in self.children:
                result += child.to_html()
            return f"<{self.tag}>{result}</{self.tag}>"
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
        
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
        