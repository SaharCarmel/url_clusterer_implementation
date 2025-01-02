from .logger import Logger
from .tree import Tree

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
