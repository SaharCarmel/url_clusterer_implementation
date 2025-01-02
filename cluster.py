import os
from datetime import datetime

class Logger:
    _instance = None
    _log_file = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    @classmethod
    def initialize(cls, log_dir="logs"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cls._log_file = os.path.join(log_dir, f"tree_log_{timestamp}.txt")
        with open(cls._log_file, 'w') as f:
            f.write(f"Tree clustering started at {timestamp}\n")

    @classmethod
    def log(cls, message, level=0):
        if cls._log_file:
            indent = "  " * level
            with open(cls._log_file, 'a') as f:
                f.write(f"{indent}{message}\n")

class Node(object):
    def __init__(self, value, recursive_values=None, threshold=3):
        self.threshold = threshold
        self.value = value
        self.type = ""
        self.children = []
        self.observed_values = []
        
        if recursive_values and len(recursive_values) > 0:
            # Filter out empty values and create a single path
            valid_values = [v for v in recursive_values if v]
            if valid_values:
                current_value = valid_values[0]
                remaining_values = valid_values[1:]
                child = Node(value=current_value, recursive_values=remaining_values)
                self.add_node(child)
        
        Logger.get_instance().log(f"Created new node with value: {value}", level=0)

    def _log(self, message, level=0):
        Logger.get_instance().log(message, level)

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def is_terminal(self):
        return len(self.children) == 0

    def _handle_no_remaining_url(self) -> str:
        return self.value

    def _compare(self, current_value: str) -> bool:
        if self.type == "wildcard":
            return True
        elif self.value == current_value:
            return True
        return False

    def _append_result_to_current_value(self, current_value: str) -> str:
        return f"{self.value}/{current_value}"

    def _compare_children(self, remaining_url: list[str]) -> str:
        self._log(f"Comparing with children, remaining URL: {remaining_url}", level=2)
        for child in self.children:
            result = child.compare(remaining_url[0], remaining_url[1:])
            if result != "":
                return self._append_result_to_current_value(result)
        self._log("No matching child found, creating new node", level=3)
        self.add_node(Node(value=remaining_url[0], recursive_values=remaining_url[1:])) 
        return self.children[-1].compare(remaining_url[0], remaining_url[1:])

    def _add_recursive_node(self, remaining_url: list[str]) -> str:
        self._log(f"Adding recursive node with remaining URL: {remaining_url}", level=2)
        node = Node(value=remaining_url[0], recursive_values=remaining_url[1:])
        self.add_node(node)
        return node.compare(remaining_url[0], remaining_url[1:])

    def _handle_adding_recursive_node(self, remaining_url: list[str]) -> str:
        if len(remaining_url) == 0:
            return self.value

    def _handle_current_node(self, remaining_url: list[str]) -> str:
        # Filter out empty values from remaining URL
        remaining_url = [v for v in remaining_url if v]
        
        if not remaining_url:
            return self._handle_no_remaining_url()
        if self.is_terminal:
            return self._add_recursive_node(remaining_url)
        else:
            return self._compare_children(remaining_url)

    def compare(self, current_value: str, remaining_url: list[str]) -> str:
        self._log(f"Comparing current_value: {current_value} with node value: {self.value}", level=1)
        current_value_part_of_current_node = self._compare(current_value)
        if current_value_part_of_current_node:
            self._log("Match found, handling current node", level=2)
            current_node_output = self._handle_current_node(remaining_url)
            return current_node_output
        else:
            self._log("No match found", level=2)
            return ""

    def add_node(self, node):
        self._log(f"Adding new node with value: {node.value}", level=1)
        self.children.append(node)
        self.observed_values.append(node.value)
        if len(self.observed_values) >= self.threshold:
            self._log("Threshold reached, converting to wildcard", level=2)
            self.children = [self.children[0]]
            self.children[0].type = "wildcard"
            self.children[0].value = "*"

    def add_child(self, child):
        self.children.append(child)
        self.observed_values.append(child.value)

    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.value} ({self.type})\n"
        for child in self.children:
            result += child.to_string(level + 1)
        return result


class Tree(object):
    def __init__(self):
        if not Logger._log_file:
            Logger.initialize()
        self.root = Node("", threshold=10000)

    def print_tree(self):
        Logger.get_instance().log("\nCurrent Tree Structure:")
        Logger.get_instance().log(self.root.to_string())

    def walk_url(self, url):
        # remove http or https
        url = url.split("://")[1]
        # break url to components and filter out empty values
        components = [c for c in url.split("/") if c]
        results = self.root.compare(
            "",
            components
        )
        return results

    def print_current_output(self, output):
        Logger.get_instance().log(f"\nCurrent Output: {output}")

def cluster_urls(urls):
    """
    Given a list of URLs, cluster them based on their patterns.
    """
    outputs = []
    tree = Tree()
    for i, url in enumerate(urls):
        Logger.get_instance().log(f"\nProcessing URL {i + 1}: {url}")
        result = tree.walk_url(url)
        tree.print_tree()
        tree.print_current_output(result)
    # return ordered alphabetically set of outputs
    # do it again to get the final tree structure
    for i, url in enumerate(urls):
        result = tree.walk_url(url)
        outputs.append(result)
    return sorted(set(outputs))


