# Trees Fundamentals

## Core structure
A tree is a hierarchical acyclic structure.
For binary trees, each node has up to two children.

## Core mental model
Every tree problem is usually:
- traversal problem (visit nodes in specific order), or
- divide-and-conquer recursion (answer from left and right subtrees).

## DFS vs BFS
- DFS: deeper first; natural with recursion/stack.
- BFS: level by level; natural with queue.

## Traversal meaning
- Preorder: process node before children (good for serialization/copying).
- Inorder: left, node, right (sorted order in BST).
- Postorder: children before node (good for delete/aggregate bottom-up).

## Recursion framework
For each node:
1. Define what recursive function returns.
2. Define base case for `None`.
3. Combine left/right results.

## BST fundamentals
BST rule: left < node < right.
- Search/insert/delete average `O(log n)` if balanced.
- Worst case skewed tree `O(n)`.

## Common pitfalls
- Missing base case leading to recursion errors.
- Using global state when return-values would be cleaner.
- Wrong bounds in BST validation.

## Templates

### DFS traversal skeleton
```python

def dfs(root):
    if not root:
        return

    # preorder position
    dfs(root.left)
    # inorder position
    dfs(root.right)
    # postorder position
```

### Height / max depth
```python

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Level-order traversal
```python
from collections import deque


def level_order(root):
    if not root:
        return []
    q = deque([root])
    ans = []

    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        ans.append(level)
    return ans
```

### Validate BST
```python

def is_valid_bst(root):
    def dfs(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return dfs(node.left, lo, node.val) and dfs(node.right, node.val, hi)

    return dfs(root, float("-inf"), float("inf"))
```
