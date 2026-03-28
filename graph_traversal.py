"""
Graph traversal algorithms: BFS and DFS implementations.
Includes testing and benchmarking utilities for social network analysis.
"""

import json
import time
import random
import sys
from pathlib import Path
from collections import deque

# ============================================================================
# PART 1: BREADTH-FIRST SEARCH (BFS)
# ============================================================================

def bfs(graph, start, target):
    """
    Find shortest path between two users using breadth-first search.
    """
    if start not in graph or target not in graph:
        return []
    if start == target:
        return [start]
    
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                
                if neighbor == target:
                    path = []
                    while neighbor is not None:
                        path.append(neighbor)
                        neighbor = parent.get(neighbor)
                    return path[::-1]
    
    return []


# ============================================================================
# PART 2: DEPTH-FIRST SEARCH (DFS)
# ============================================================================

def dfs(graph, start):
    """
    Find all users reachable from a starting user using depth-first search.
    """
    if start not in graph:
        return set()
    
    visited = set()
    
    def dfs_recursive(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_recursive(neighbor)
    
    dfs_recursive(start)
    return visited


# ============================================================================
# TESTING AND BENCHMARKING UTILITIES (unchanged from template)
# ============================================================================

def load_network(size):
    """Load social network dataset of given size."""
    filename = f'data/network_{size}.json'
    if not Path(filename).exists():
        print(f"Error: {filename} not found. Run network_generator.py first.")
        sys.exit(1)
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    graph = {int(k): v for k, v in data['graph'].items()}
    return graph, data['num_users']

def test_bfs():
    print("\n" + "="*70)
    print("TESTING: Breadth-First Search (BFS)")
    print("="*70)
    graph, num_users = load_network(100)
    test_cases = 5
    print(f"\nTesting {test_cases} random paths in 100-user network...\n")
    for i in range(test_cases):
        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)
        path = bfs(graph, start, target)
        if path:
            print(f"Test {i+1}: Path from User {start} to User {target}")
            print(f"  Length: {len(path) - 1} connections")
            print(f"  Path: {' → '.join(map(str, path[:5]))}{'...' if len(path) > 5 else ''}")
            valid = True
            for j in range(len(path) - 1):
                if path[j+1] not in graph[path[j]]:
                    valid = False
                    break
            status = "✓ Valid" if valid else "✗ Invalid"
            print(f"  Status: {status}\n")
        else:
            print(f"Test {i+1}: No path from User {start} to User {target}\n")

def test_dfs():
    print("\n" + "="*70)
    print("TESTING: Depth-First Search (DFS)")
    print("="*70)
    graph, num_users = load_network(100)
    test_cases = 5
    print(f"\nTesting {test_cases} explorations in 100-user network...\n")
    for i in range(test_cases):
        start = random.randint(0, num_users - 1)
        reachable = dfs(graph, start)
        print(f"Test {i+1}: Exploration from User {start}")
        print(f"  Reachable users: {len(reachable)}")
        print(f"  Percentage of network: {(len(reachable)/num_users)*100:.1f}%")
        status = "✓ Valid" if start in reachable else "✗ Invalid"
        print(f"  Status: {status}\n")

def benchmark_bfs(graph, num_users, num_trials=10):
    total_time = 0
    for _ in range(num_trials):
        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)
        start_time = time.time()
        bfs(graph, start, target)
        total_time += time.time() - start_time
    return total_time / num_trials

def benchmark_dfs(graph, num_users, num_trials=10):
    total_time = 0
    for _ in range(num_trials):
        start = random.randint(0, num_users - 1)
        start_time = time.time()
        dfs(graph, start)
        total_time += time.time() - start_time
    return total_time / num_trials

def run_benchmarks():
    print("\n" + "="*70)
    print("BENCHMARKING: BFS vs DFS Performance")
    print("="*70)
    sizes = [100, 500, 1000]
    print(f"\n{'Size':<8} {'Algorithm':<12} {'Avg Time (ms)':<15}")
    print("-" * 70)
    for size in sizes:
        graph, num_users = load_network(size)
        bfs_time = benchmark_bfs(graph, num_users)
        dfs_time = benchmark_dfs(graph, num_users)
        print(f"{size:<8} {'BFS':<12} {bfs_time*1000:<15.3f}")
        print(f"{size:<8} {'DFS':<12} {dfs_time*1000:<15.3f}\n")
    print("="*70)

def print_usage():
    print("\nUsage: python graph_traversal.py [option]")
    print("Options: --test-bfs, --test-dfs, --benchmark, --help")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    option = sys.argv[1]
    if not Path('data/network_100.json').exists():
        print("\nError: Data files not found! Run: python network_generator.py")
        sys.exit(1)
    if option == '--test-bfs':
        test_bfs()
    elif option == '--test-dfs':
        test_dfs()
    elif option == '--benchmark':
        run_benchmarks()
    elif option == '--help':
        print_usage()
    else:
        print(f"Unknown option '{option}'")
        print_usage()

if __name__ == '__main__':
    main()
