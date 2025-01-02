from .logger import Logger

class Node:
    def __init__(self, value, recursive_values=None, threshold=3):
        self.threshold = threshold
        self.value = value
        self.type = ""
        self.children = []
        self.observed_values = []
        
        if recursive_values:
            self._initialize_recursive_values(recursive_values)
        
        self._log(f"Created new node with value: {value}")

    def _initialize_recursive_values(self, recursive_values):
        valid_values = [v for v in recursive_values if v]
        if valid_values:
            current_value = valid_values[0]
            remaining_values = valid_values[1:]
            child = Node(value=current_value, recursive_values=remaining_values)
            self.add_node(child)

    def _log(self, message, level=0):
        Logger.get_instance().log(message, level)

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def is_terminal(self):
        return len(self.children) == 0

    def compare(self, current_value: str, remaining_url: list[str]) -> str:
        self._log(f"Comparing current_value: {current_value} with node value: {self.value}", level=1)
        if self._compare(current_value):
            self._log("Match found, handling current node", level=2)
            return self._handle_current_node(remaining_url)
        else:
            self._log("No match found", level=2)
            return ""

    def _compare(self, current_value: str) -> bool:
        return self.type == "wildcard" or self.value == current_value

    def _handle_current_node(self, remaining_url: list[str]) -> str:
        remaining_url = [v for v in remaining_url if v]  # Filter out empty values
        if not remaining_url:
            return self.value
        if self.is_terminal:
            return self._add_recursive_node(remaining_url)
        else:
            return self._compare_children(remaining_url)

    def _add_recursive_node(self, remaining_url: list[str]) -> str:
        self._log(f"Adding recursive node with remaining URL: {remaining_url}", level=2)
        node = Node(value=remaining_url[0], recursive_values=remaining_url[1:])
        self.add_node(node)
        return node.compare(remaining_url[0], remaining_url[1:])

    def _compare_children(self, remaining_url: list[str]) -> str:
        self._log(f"Comparing with children, remaining URL: {remaining_url}", level=2)
        for child in self.children:
            result = child.compare(remaining_url[0], remaining_url[1:])
            if result:
                return self._append_result_to_current_value(result)
        self._log("No matching child found, creating new node", level=3)
        self.add_node(Node(value=remaining_url[0], recursive_values=remaining_url[1:])) 
        return self.children[-1].compare(remaining_url[0], remaining_url[1:])

    def _append_result_to_current_value(self, current_value: str) -> str:
        return f"{self.value}/{current_value}"

    def add_node(self, node):
        self._log(f"Adding new node with value: {node.value}", level=1)
        self.children.append(node)
        self.observed_values.append(node.value)
        if len(self.observed_values) >= self.threshold:
            self._convert_to_wildcard()

    def _convert_to_wildcard(self):
        self._log("Threshold reached, converting to wildcard", level=2)
        self.children = [self.children[0]]
        self.children[0].type = "wildcard"
        self.children[0].value = "*"

    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.value} ({self.type})\n"
        for child in self.children:
            result += child.to_string(level + 1)
        return result
