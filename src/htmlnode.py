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
    def __init__(self, value, tag=None,  props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        if props is None:
            props = {}
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            result = ""
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return f"<{self.tag}{result}>{self.value}</{self.tag}>"
        