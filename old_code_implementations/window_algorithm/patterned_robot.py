from bitarray import bitarray
import random
import logging
# r = num of robots. w = size of window.

class robot:
    def __init__(self, pattern: bitarray, window=None, sandbox=None, ID=-1, expulse_lim = 5):
        self.ID = ID
        self.pattern = pattern.copy()
        window_size = len(pattern)
        self.window  = bitarray('0' * window_size)
        self.sandbox = bitarray('0' * window_size)
        self.expulse_lim = expulse_lim
        self.expulse_count = 0
        self.expulsing = False
        self.dont_swap = False

        if window is not None:
            self.replace_window(window)
            if sandbox is not None:
                self.replace_sandbox(sandbox)

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

    def has_valid_sandbox(self):
        return self.sandbox == self.pattern

    def swap(self):   # O(3w)
        temp = self.window.copy()
        self.window = self.sandbox.copy()
        self.sandbox = temp.copy()
        if self.sandbox != self.pattern:
            self.sandbox.sort()

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

    def trade_sandboxes_with(self, other, should_not_swap=False):   # other is a robot,  O(w)
        temp = self.sandbox.copy()
        self.sandbox = other.sandbox
        other.sandbox = temp
        if self.expulsing:
            other.dont_swap = True
            self.dont_swap = False
            self.expulsing = False
