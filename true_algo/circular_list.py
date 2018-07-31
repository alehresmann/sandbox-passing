# A circular doubly-linked linked list, with minor modifications for printing.

from colorama import Fore

# no black because unreadable on dark terminal. white reserved for no robots.
colours = [ Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN ]

class node:
    def __init__(self):
        self.data = None
        self.prev = None
        self.next = None
        self.owned_by = None
        self.quantity = 0

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
            if node.owned_by is None:
                ret += Fore.WHITE
            else:
                ret += colours[node.owned_by.ID % len(colours)]
            ret += str(int(node.data is True))
            node = node.next
        ret += Fore.WHITE
        return ret
