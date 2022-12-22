from random import randrange

items = [
    "R",
    "FBN",
    "COS",
    "TOT",
    "AFK",
    "HEM",
    "PEW",
    "MP",
    "SIG",
    "GUP",
    "POW",
    "HYF",
    "PRS",
    "RTB",
    "CTP",
    "TFE",
    "VT",
    "SA",
    "CA",
]
uncompared_items = []


class Node:
    root_node = None

    def __init__(self, value: str, middle_child: bool = False):
        self.left = None
        self.middle = None
        self.right = None
        self.value = value
        self.is_middle_child = middle_child

    def get_weight(self):
        children = [self.left, self.middle, self.right]
        weight = 1
        for ch in children:
            weight = weight + (0 if ch is None else ch.get_weight())
        return weight

    def get_leftmost_leaf(self):
        if self.left is not None:
            return self.left.get_leftmost_leaf()
        return self

    def get_rightmost_leaf(self):
        if self.right is not None:
            return self.right.get_rightmost_leaf()
        return self

    def get_parent(self, node):
        if node is None:
            return None
        if self.left is node or self.right is node or self.middle is node:
            return self
        parent = None
        if self.left is not None:
            parent = self.left.get_parent(node)
        if parent is None and self.right is not None:
            parent = self.right.get_parent(node)
        if parent is None and self.middle is not None:
            parent = self.middle.get_parent(node)
        return parent

    def get_topmost_equal_node(self):
        if not self.is_middle_child:
            return self
        parent = Node.root_node.get_parent(self)
        return parent.get_topmost_equal_node()

    def get_ordered_list(self):
        left_list = [] if self.left is None else self.left.get_ordered_list()
        middle_list = [self.value]
        mc = self.middle
        while mc is not None:
            middle_list.append(mc.value)
            mc = mc.middle
        right_list = [] if self.right is None else self.right.get_ordered_list()
        return left_list + [middle_list] + right_list

    @classmethod
    def rebalance(cls, root):
        left_weight = 0 if root.left is None else root.left.get_weight()
        right_weight = 0 if root.right is None else root.right.get_weight()
        if left_weight * 1.5 < right_weight:
            # right branch is bigger
            new_root = root.right
            root.right = None
            new_attachment_node = new_root.get_leftmost_leaf()
            new_attachment_node.left = root
            return new_root
        elif left_weight > right_weight * 1.5:
            # left branch is bigger
            new_root = root.left
            root.left = None
            new_attachment_node = new_root.get_rightmost_leaf()
            new_attachment_node.right = root
            return new_root
        return root


def setup():
    for i in items:
        uncompared_items.append(i)
    i = randrange(len(uncompared_items))
    Node.root_node = Node(uncompared_items[i])
    uncompared_items.pop(i)


def rank_item(item):
    insert_node = Node.root_node
    while insert_node is not None:
        prompt = f"Is {item} ranked above {insert_node.value}? y/n/c"
        choice = input(prompt)
        if choice == "y":
            # Is middle child?
            insert_node = insert_node.get_topmost_equal_node()
            if insert_node.right is None:
                insert_node.right = Node(item)
                insert_node = None
            else:
                insert_node = insert_node.right
        elif choice == "n":
            # Is middle child?
            insert_node = insert_node.get_topmost_equal_node()
            if insert_node.left is None:
                insert_node.left = Node(item)
                insert_node = None
            else:
                insert_node = insert_node.left
        elif choice == "c":
            if insert_node.middle is None:
                insert_node.middle = Node(item)
                insert_node = None
            else:
                insert_node = insert_node.middle
    ordered_list = Node.root_node.get_ordered_list()
    print(f"Added {item} to tree, ordered list is {ordered_list}")


def do_ranking():
    while len(uncompared_items) != 0:
        idx = randrange(len(uncompared_items))
        item = uncompared_items.pop(idx)
        rank_item(item)


setup()
do_ranking()
