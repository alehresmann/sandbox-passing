import sys
import logging
from bitarray import bitarray

from circular_list import node
from command import switch_command, move_command, update_state_command

class robot:
    def __init__(self, ID: int, pattern: bitarray, current_node: node, k: int, is_synchronised=False):

        self.is_synchronised = is_synchronised
        self.ID = ID
        self.pattern = pattern
        self.current_node = current_node
        self.k = k  # total slices in the configuration

        self.consecutive_valid_windows_seen = 0
        self.state = 0  # 0 == unsatisfied, 1 == satisfied, 2 == done
        self.slice_size = len(pattern)

        self.window = []   # array of pointers to nodes
        self.sandbox = []  # array of pointers to nodes
        self.commands = [] # array of commands

        self.update_window_and_sandbox()

        # for statistics. All of these except total_rounds is only touched in commands
        self.total_switches_done = 0
        self.total_moves_done = 0
        self.total_time_waited = 0
        self.total_rounds = 0
        self.reached_satisfied_at = -1
        self.reached_done_at = -1

    def __str__(self):  # for debugging
        window_data = [w.data for w in self.window]
        sandbox_data = [s.data for s in self.sandbox]
        return 'R'+str(self.ID) + ',\t' + ''.join(map(str,map(int,window_data))) + ':' \
                + ''.join(map(str,map(int, sandbox_data))) +',\tstate: ' + str(self.state) \
                + ' , consecutive_valid_windows_seen: ' + str(self.consecutive_valid_windows_seen) \
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

    def final_state(self):  # for printing after algorithm completion
        return 'R' + str(self.ID) + '\t, total switches: ' + str(self.total_switches_done) \
                + '\ttotal moves: ' + str(self.total_moves_done) + '\ttotal rounds: ' \
                + str(self.total_rounds) + '\ttime waited: ' \
                + str(self.total_time_waited) + '\tconsecutive slices seen: ' \
                + str(self.consecutive_valid_windows_seen) + '\t state: ' + str(self.state) \
                + ', reached satisfied at round: ' + str(self.reached_satisfied_at) \
                + ', reached done at round: ' + str(self.reached_done_at)

    def has_valid_window(self):
        return [w.data for w in self.window].count(False) == self.pattern.count(0)

    def has_valid_sandbox(self):
        return [s.data for s in self.sandbox].count(False) == self.pattern.count(0)

    def should_I_swap(self):
        zh = [w.data for w in self.window].count(False) + [s.data for s in self.sandbox].count(False)
        oh = [w.data for w in self.window].count(True) + [s.data for s in self.sandbox].count(True)
        zw = self.pattern.count(0)
        ow = self.pattern.count(1)

        # if window can be made valid, don't swap
        if zh >= zw and oh >= ow:
            if self.has_valid_sandbox():
                return True
            return False

        # if not enough ones, the sandbox will necessarily have more or equal zeroes as the window
        if oh < ow:
            return False

        # if not enough zeroes, push the zeroes to the right.
        if zh < zw:
            return True

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

    def reach_pattern(self):
        logging.debug('R' + str(self.ID) + ' reaching pattern in w')
        if not self.has_valid_window():
            raise AssertionError('tried to reach pattern on an invalid slice!')
        i = 0
        taken = []
        for i in range(0, self.slice_size):
            if self.window[i].data != self.pattern[i] and i not in taken:
                for j in range(i + 1, self.slice_size):
                    if self.window[j].data != self.pattern[j] \
                            and self.window[j].data != self.window[i].data \
                            and j not in taken:
                        self.commands.append(switch_command(self, i, j, True, True))
                        taken.append(j)
                        break

    def algo_round(self):
        self.total_rounds += 1

        #compute
        if self.state == 0:
            if not self.has_valid_window() and not self.has_valid_sandbox():
                self.local_rearrange()
            if self.should_I_swap():
                self.swap()

        if self.state == 1:
            self.reach_pattern()

        if self.state == 2 and self.consecutive_valid_windows_seen >= self.k - 2:
            return

        self.commands.append(update_state_command(self))

        # move
        # NOTE: Should probably implement the checking for robots blocking me in here
        # and not in move command, for the unsynced version
        for i in range(0, self.slice_size):
            self.commands.append(move_command(self, True))

