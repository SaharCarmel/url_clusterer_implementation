from .node import Node
from .logger import Logger

class Tree:
    def __init__(self):
        self._initialize_logger()
        self.root = Node("", threshold=10000)

    def _initialize_logger(self):
        if not Logger._log_file:
            Logger.initialize()

    def print_tree(self):
        logger = Logger.get_instance()
        logger.log("\nCurrent Tree Structure:")
        logger.log(self.root.to_string())

    def walk_url(self, url):
        components = self._extract_url_components(url)
        return self.root.compare("", components)

    def _extract_url_components(self, url):
        url = url.split("://")[1]  # remove http or https
        return [component for component in url.split("/") if component]

    def print_current_output(self, output):
        Logger.get_instance().log(f"\nCurrent Output: {output}")
