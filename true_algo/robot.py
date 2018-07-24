import sys
import logging

from bitarray import bitarray

from circular_list import node
from command import command, local_rearrange_command, swap_command, move_command, reach_pattern_command, update_state_command

# Best to think of the robots as state machines

class robot:
    def __init__(self, ID: int, pattern: bitarray, current_node: node, k: int):

        self.ID = ID
        self.pattern = pattern
        self.current_node = current_node
        self.k = k  # total slices in the configuration

        self.consecutive_valid_windows_seen = 0
        self.state = 0  # 0 == unsatisfied, 1 == satisfied, 2 == done
        self.slice_size = len(pattern)

        self.window = []   # array of pointers to nodes
        self.sandbox = []  # array of pointers to nodes

        self.update_window_and_sandbox()

        self.commands = []
        self.has_computed = False

    def has_valid_window(self):
        return [w.data for w in self.window].count(False) == self.pattern.count(0)

    def has_valid_sandbox(self):
        return [s.data for s in self.sandbox].count(False) == self.pattern.count(0)

    def has_patterned_window(self):
        return ''.join(map(str,map(int,[w.data for w in self.window]))) == self.pattern.to01()

    def has_patterned_sandbox(self):
        return ''.join(map(str,map(int,[s.data for s in self.sandbox]))) == self.pattern.to01()

    def update_window_and_sandbox(self):
        self.window = []
        self.sandbox = []
        temp = self.current_node
        for i in range(0, self.slice_size):
            self.window.append(temp)
            temp = temp.next
        for i in range(0, self.slice_size):
            self.sandbox.append(temp)
            temp = temp.next

    def update_state(self):  # instantaneous operation
        # checks if window and sandbox is valid, adds to consecutive slices, sets states.
        if self.has_valid_window() and self.has_valid_sandbox():
            self.consecutive_valid_windows_seen += 1
        else:
            logging.debug('window: ' + str(self.has_valid_window()) + ', sandbox: ' + str(self.has_valid_sandbox()))
            self.consecutive_valid_windows_seen = 0

        if self.consecutive_valid_windows_seen >= self.k:
            self.state += 1
            self.consecutive_valid_windows_seen = 0

    def can_rearrange(self):
        window_zero_count = [w.data for w in self.window].count(False)
        sandbox_zero_count = [s.data for s in self.sandbox].count(False)
        pattern_zero_count = self.pattern.count(0)
        if window_zero_count > pattern_zero_count and sandbox_zero_count < self.slice_size:
            return True
        if window_zero_count < pattern_zero_count and sandbox_zero_count > 1:
            return True
        return False

    def __str__(self):
        window_data = [w.data for w in self.window]
        sandbox_data = [s.data for s in self.sandbox]
        return 'R'+str(self.ID) + ',\t' + ''.join(map(str,map(int,window_data))) + ':' \
                + ''.join(map(str,map(int, sandbox_data))) +',\tstate: ' + str(self.state) \
                + ' , consecutive_valid_windows_seen: ' + str(self.consecutive_valid_windows_seen) \
                + ',\tk: ' + str(self.k) + ', ' \
                + str(len(self.commands)) + ' commands in queue, next is ' \
                + str(next(iter(self.commands), None))

    def swap(self):
        for i in range(0, self.slice_size):
            self.commands.append(swap_command(self, i))

    def algo_iter(self):
        if self.state > 1:  # done
            return

        if self.state == 0:
            if not self.has_valid_window() and not self.has_valid_sandbox():
                if self.can_rearrange():  # keep rearranging until you can't
                    self.commands.append(local_rearrange_command(self))
                    return

            if [w.data for w in self.window].count(False)> self.pattern.count(0):
                logging.debug('R' + str(self.ID) + 'swapping')
                if [w.data for w in self.window].count(False) != [s.data for s in self.sandbox].count(False):
                    self.swap()

        if self.state == 1:
            if not self.has_patterned_window():
                logging.debug('no window')
                self.commands.append(reach_pattern_command(self, True))
                return
            if not self.has_patterned_sandbox():
                logging.debug('no sand')
                self.commands.append(reach_pattern_command(self, False))
                return

        # move
        for i in range(0, self.slice_size):
            self.commands.append(move_command(self, True))
        self.commands.append(update_state_command(self))
