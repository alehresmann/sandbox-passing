import sys
import logging
from bitarray import bitarray

from circular_list import node
from command import switch_command, move_command

class robot:
    def __init__(self, ID: int, pattern: bitarray, current_node: node, k: int):

        self.ID = ID
        self.pattern = pattern
        self.current_node = current_node
        self.k = k  # total slices in the configuration

        self.consecutive_pattern_windows_seen = 0
        self.state = True  # True -> keep going, False -> End
        self.slice_size = len(pattern)

        self.window = []   # array of pointers to nodes
        self.sandbox = []  # array of pointers to nodes

        self.window_projection = []  # lets you take decisions based on what the window will be
        self.sandbox_projection = [] # lets you take decisions based on what the sandbox will be

        self.commands = [] # array of commands

        self.update_window_and_sandbox()

        # for statistics. All of these except total_rounds is only touched in commands
        self.total_switches_done = 0
        self.total_moves_done = 0
        self.total_time_waited = 0
        self.total_rounds = 0

    def __str__(self):  # for debugging
        window_data = [w.data for w in self.window]
        sandbox_data = [s.data for s in self.sandbox]
        return 'R'+str(self.ID) + ',\t' + ''.join(map(str,map(int,window_data))) + ':' \
                + ''.join(map(str,map(int, sandbox_data))) +',\tstate: ' + str(self.state) \
                + ' , consecutive_pattern_windows_seen: ' + str(self.consecutive_pattern_windows_seen) \
                + ',\tk: ' + str(self.k) + ', ' \
                + str(len(self.commands)) + ' commands in queue, next is ' \
                + str(next(iter(self.commands), None))

    def update_window_and_sandbox(self):  # used once at initialisation
        self.window = []
        self.sandbox = []
        temp = self.current_node
        for i in range(0, self.slice_size):
            self.window.append(temp)
            temp = temp.next
        for i in range(0, self.slice_size):
            self.sandbox.append(temp)
            temp = temp.next
        self.window_projection = [n.data for n in self.window]
        self.sandbox_projection = [n.data for n in self.sandbox]

    def final_state(self):  # for printing after algorithm completion
        return 'R' + str(self.ID) + '\t, total switches: ' + str(self.total_switches_done) \
                + '\ttotal moves: ' + str(self.total_moves_done) + '\ttotal rounds: ' \
                + str(self.total_rounds) + '\ttime waited: ' \
                + str(self.total_time_waited) + '\tconsecutive pattern windows seen: ' \
                + str(self.consecutive_pattern_windows_seen) + '\t state: ' + str(self.state)

    def has_valid_window(self):
        return [w.data for w in self.window].count(False) == self.pattern.count(0)

    def has_valid_sandbox(self):
        return [s.data for s in self.sandbox].count(False) == self.pattern.count(0)

    def should_I_swap(self):
        wz = self.window_projection.count(False)
        sz = self.sandbox_projection.count(False)
        pz = self.pattern.count(1)

        if wz > pz and wz > sz:
            return True
        return False

    def local_rearrange(self):
        wz = [w.data for w in self.window].count(False)
        sz = [s.data for s in self.sandbox].count(False)
        pz = self.pattern.count(0)
        i = 0
        j = 0
        while (wz > pz and sz < self.slice_size) or (wz < pz and sz > 0):
            want = bool(wz > pz)
            while self.window[i].data == want:
                i += 1
            while self.sandbox[j].data != want:
                j += 1
            self.commands.append(switch_command(self, i, j, True, False))
            self.window_projection[i], self.sandbox_projection[j] = self.sandbox_projection[j], self.window_projection[i]
            if want:
                wz -= 1
                sz += 1
            else:
                wz += 1
                sz -= 1
            i += 1
            j += 1
            if i == self.slice_size or j == self.slice_size:
                break

        logging.debug('R' + str(self.ID) + ' local rearrange: ' + str(self.commands))

    def swap(self):
        logging.debug('R' + str(self.ID) + '  swapping w and s')
        for i in range(0, self.slice_size):
            self.commands.append(switch_command(self, i, i, True, False))
            self.window_projection[i], self.sandbox_projection[i] = self.sandbox_projection[i], self.window_projection[i]

    def reach_pattern(self):
        logging.debug('R' + str(self.ID) + ' reaching pattern in w')
        if self.window_projection.count(False) != self.pattern.count(0):
            raise AssertionError('tried to reach pattern on an invalid slice!')
        i = 0
        taken = []
        for i in range(0, self.slice_size):
            if self.window_projection[i] != self.pattern[i] and i not in taken:
                for j in range(i + 1, self.slice_size):
                    if self.window_projection[j] != self.pattern[j] \
                            and self.window_projection[j] != self.window_projection[i] \
                            and j not in taken:
                        self.commands.append(switch_command(self, i, j, True, True))
                        self.window_projection[i], self.window_projection[i] = self.window_projection[j], self.window_projection[i]
                        taken.append(j)
                        break

    def algo_round(self):
        self.total_rounds += 1
        # compute
        if not self.has_valid_window() and not self.has_valid_sandbox():
            self.local_rearrange()

        wz = self.window_projection.count(False)
        pz = self.pattern.count(0)
        if wz > pz and wz > self.sandbox_projection.count(False):
            self.swap()

        if self.window_projection.count(False) == self.pattern.count(0):
            self.reach_pattern()
            self.consecutive_pattern_windows_seen += 1
        else:
            self.consecutive_pattern_windows_seen = 0

        if self.consecutive_pattern_windows_seen == self.k:
            self.state = False

        # move
        # NOTE: Should probably implement the checking for robots blocking me in here
        # and not in move command, for the unsynced version
        for i in range(0, self.slice_size):
            self.commands.append(move_command(self, True))

