import sys
import time
from src.cluster import cluster_urls, Tree

def main(input_file):
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f.readlines()]
    
    start_time = time.time()
    results = cluster_urls(urls)
    end_time = time.time()
    
    for result in results:
        print(result)
    
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    
    tree = Tree()
    for url in urls:
        tree.walk_url(url)
    print("\nFinal Tree Representation:")
    print(tree.root.to_string())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    main(input_file)
