# A doubly-linked circular linked list, with an additional 'owned_by' for node ownership

class node:
    def __init__(self):
        self.data = None
        self.prev = None
        self.next = None
        self.owned_by = None

class circular_list:
    def __init__(self, input_string: str):
        self.first_node = None
        self.last_node = None
        self.length = len(input_string)

        for char in input_string:
            self._add_at_end(char == '1')

        self._make_circular()

    def _add_at_end(self, data):
        new_node = node()
        new_node.data = data
        if not self.first_node:
            self.first_node = new_node
            self.last_node = new_node
        else:
            self.last_node.next = new_node
            new_node.prev = self.last_node
            self.last_node = new_node

    def get_node_at(self, pos: int):
        temp = self.first_node
        for i in range(0, pos):
            temp = temp.next
        return temp

    def _make_circular(self):
        self.last_node.next = self.first_node
        self.first_node.prev = self.last_node

    def __len__(self):
        return self.length

    def __str__(self):
        node = self.first_node
        ret = ''
        for i in range(0, len(self)):
            ret += str(int(node.data is True))
            node = node.next
        return ret
