from bitarray import bitarray
import random

# r = num of robots. w = size of window.

class robot:
    def __init__(self, window: bitarray, sandbox: bitarray, ID=-1, pattern=None):
        self.ID = ID
        self.replace_window(window)
        self.replace_sandbox(sandbox)

        if pattern is not None:
            self.pattern = pattern.copy()  # the window he wants to reach

        self.sandbox_is_locked = False

    def __str__(self):
        return self.window.to01() + '|' + self.sandbox.to01()

    def replace(self, arr: bitarray, in_window: bool):
        if in_window:
            self.window = arr.copy()
        else:
            self.sandbox = arr.copy()

    def replace_window(self, arr: bitarray):
        self.replace(arr, 1)

    def replace_sandbox(self, arr: bitarray):
        self.replace(arr, 0)

    def has_valid_window(self):
        return self.window == self.pattern

    def swap(self):   # O(3w)
        if self.has_randomised:
            self.has_randomised = False
            return
        temp = self.window.copy()
        self.window = self.sandbox.copy()
        self.sandbox = temp.copy()

    #def randomise(self):
    #    temp = list(self.window.to01() + self.sandbox.to01())
    #    random.shuffle(temp)
    #    self.window = bitarray("".join(temp[:len(self.pattern)]))
    #    self.sandbox = bitarray("".join(temp[len(self.pattern):]))

    def rearrange_window(self):  # O(w^2)
        for i in range(0, len(self.window)):
            if self.window[i] != self.pattern[i]:
                need = self.pattern[i]
                for j in range(i + 1, len(self.window)):
                    if self.window[j] == need:
                        self.window[j] = not need
                        self.window[i] = need
                        break

    def rearrange_from_sandbox(self):   # O(wlog(w) + O(w))  --> O(wlogw)
        #if self.sandbox == self.pattern:  # don't touch sandbox if it's the pattern
        #    if not self.has_valid_window():
        #        self.randomise()
        #        self.has_randomised = True
        #    return

        self.sandbox.sort()

        for i in range(0, len(self.window)):
            if self.window[i] != self.pattern[i]:
                if self.pattern[i] and self.sandbox[-1]:
                    self.sandbox.pop()
                    self.sandbox.insert(0, False)  # replace a 0 at the beginning
                    self.window[i] = True
                elif not self.pattern[i] and not self.sandbox[0]:
                    self.sandbox.pop(0)
                    self.sandbox.append(True)  # replace a 1 at the end
                    self.window[i] = False
                else:
                    break

    def swap_sandboxes_with(self, other):   # other is a robot,  O(w)
        temp = self.sandbox.copy()
        self.sandbox = other.sandbox
        other.sandbox = temp
