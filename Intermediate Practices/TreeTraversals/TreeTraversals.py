class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None
        self.nodes = {}  # store all nodes here

    def add_node(self, parent_value, left_value, right_value):
        # create parent if it doesn't exist yet
        if parent_value not in self.nodes:
            self.nodes[parent_value] = Node(parent_value)

        parent_node = self.nodes[parent_value]

        # first node becomes root
        if self.root is None:
            self.root = parent_node

        # add left child
        if left_value != "null" and left_value is not None:
            if left_value not in self.nodes:
                self.nodes[left_value] = Node(left_value)
            parent_node.left = self.nodes[left_value]

        # add right child
        if right_value != "null" and right_value is not None:
            if right_value not in self.nodes:
                self.nodes[right_value] = Node(right_value)
            parent_node.right = self.nodes[right_value]

    def preorder_traversal(self, node, result=None):
        # root, left, right
        if result is None:
            result = []

        if node is not None:
            result.append(node.value)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

        return result

    def inorder_traversal(self, node, result=None):
        # left, root, right
        if result is None:
            result = []

        if node is not None:
            self.inorder_traversal(node.left, result)
            result.append(node.value)
            self.inorder_traversal(node.right, result)

        return result

    def postorder_traversal(self, node, result=None):
        # left, right, root
        if result is None:
            result = []

        if node is not None:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.value)

        return result

    def display_tree_structure(self):
        print(f"{'Node':<10} {'L-Subtree':<15} {'R-Subtree':<15}")
        print("-" * 40)

        for node_value in self.nodes:
            node = self.nodes[node_value]
            left = node.left.value if node.left else "null"
            right = node.right.value if node.right else "null"
            print(f"{node_value:<10} {left:<15} {right:<15}")

    def display_traversals(self):
        print(f"\nRoot of the Tree: {self.root.value}\n")

        preorder = self.preorder_traversal(self.root)
        inorder = self.inorder_traversal(self.root)
        postorder = self.postorder_traversal(self.root)

        print(f"Preorder Traversal: {' '.join(preorder)}")
        print(f"Inorder Traversal: {' '.join(inorder)}")
        print(f"Postorder Traversal: {' '.join(postorder)}")


def parse_input(input_str):
    # parse something like "(A,B,E)" into parts
    input_str = input_str.strip()
    if input_str.startswith('(') and input_str.endswith(')'):
        input_str = input_str[1:-1]

    parts = [part.strip() for part in input_str.split(',')]

    # handle null values
    for i in range(len(parts)):
        if parts[i].lower() == 'null' or parts[i] == '':
            parts[i] = 'null'

    return parts[0], parts[1], parts[2]


def main():
    print("=" * 50)
    print("BINARY TREE TRAVERSALS PROGRAM")
    print("=" * 50)
    print("\nEnter nodes in format: (Parent, Left, Right)")
    print("Use 'null' for empty children")
    print("Type 'done' when finished\n")

    tree = BinaryTree()
    input_order = []  # remember the order for output

    while True:
        user_input = input("Enter node: ").strip()

        if user_input.lower() == 'done':
            break

        if not user_input:
            continue

        try:
            parent, left, right = parse_input(user_input)
            tree.add_node(parent, left, right)
            input_order.append((parent, left, right))
        except Exception as e:
            print(f"Invalid input format. Please use: (Parent, Left, Right)")
            continue

    if tree.root is None:
        print("\nNo tree created!")
        return

    print("\n" + "=" * 50)
    print("OUTPUT")
    print("=" * 50 + "\n")

    # show nodes in the order they were entered
    print(f"{'Node':<10} {'L-Subtree':<15} {'R-Subtree':<15}")
    print("-" * 40)
    for parent, left, right in input_order:
        print(f"{parent:<10} {left:<15} {right:<15}")

    # show all traversals
    tree.display_traversals()
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
