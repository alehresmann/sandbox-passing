import sys
import logging
from bitarray import bitarray


class robot:
    def __init__(self, ID: int, pattern: bitarray, a: int, b: int, pconfig: bitarray):

        self.ID = ID
        self.pattern = pattern
        self.pconfig = pconfig  # configuration pointer
        self.pattern_zero_count = pattern.count(0)
        self.a = 0
        self.b = 0
        self.window_zero_count = 0
        self.sandbox_zero_count = 0
        self.total_window_count = len(pconfig)
        self.consecutive_valid_windows_seen = 0
        self.status = 0  # 1 means ready to set to pattern
        self.done = 0
        self.windows_from_original_position = 0  # after having set the pattern, go to original position and end.
        self.window_size = int((b - a) / 2)

        self.move(a, b)

    def check_local_validity(self):
        if self.has_valid_window() and self.has_valid_sandbox():
            self.consecutive_valid_windows_seen += 1
        else:
            self.consecutive_valid_windows_seen = 0

    def update_status(self):
        if not self.status and self.consecutive_valid_windows_seen >= self.total_window_count:
            self.status = 1
            self.consecutive_valid_windows_seen = 0

    def __str__(self):
        return 'R'+str(self.ID) + ', pos:' + str(self.a) + ':' + str(self.b) + ', ' \
                + str(self.window) + ':' + str(self.sandbox) + ',count: ' \
                + str(self.window_zero_count) + ':' + str(self.sandbox_zero_count)

    def set_window_in_pconfig(self, arr: bitarray):
        self.pconfig[self.a:self.a + self.window_size] = arr

    def set_sandbox_in_pconfig(self, arr: bitarray):
        if self.b == 0:
            self.pconfig[self.a + self.window_size:] = arr
        elif self.a > self.b:
            self.pconfig[0:self.window_size] = arr
        else:
            self.pconfig[self.a + self.window_size: self.b] = arr

    def move(self, a: int, b :int):
        self.a = (a) % (len(self.pconfig))
        self.b = (b) % (len(self.pconfig))

        self.window = self.pconfig[self.a: self.a + self.window_size]

        if self.b == 0:
            self.sandbox = self.pconfig[self.a + self.window_size:self.a + self.window_size + self.window_size]
        elif self.a > self.b:
            self.sandbox = self.pconfig[0:self.window_size]
        else:
            self.sandbox = self.pconfig[self.a + self.window_size: self.b]

        self.window_zero_count = self.window.count(0)
        self.sandbox_zero_count = self.sandbox.count(0)

    def move_by_window_size(self):
        self.windows_from_original_position += 1
        self.windows_from_original_position % self.total_window_count
        self.move(self.a + self.window_size, self.b + self.window_size)

    def has_valid_window(self):
        return self.window_zero_count == self.pattern_zero_count

    def has_valid_sandbox(self):
        return self.sandbox_zero_count == self.pattern_zero_count

    def rearrange_from_unsorted_sandbox(self):
        logging.debug('rearranging:\t' + str(self))
        need = self.window_zero_count - self.pattern_zero_count
        while need > 0 and self.sandbox_zero_count < self.window_size:
            for i, bit in enumerate(self.window):
                if not bit:
                    self.window[i] = 1
                    break
            for i, bit in enumerate(self.sandbox):
                if bit:
                    self.sandbox[i] = 0
                    break
            self.window_zero_count -= 1
            self.sandbox_zero_count += 1
            need -= 1
        while need < 0 and self.sandbox_zero_count > 0:
            for i, bit in enumerate(self.window):
                if bit:
                    self.window[i] = 0
                    break
            for i, bit in enumerate(self.sandbox):
                if not bit:
                    self.sandbox[i] = 1
                    break
            self.window_zero_count += 1
            self.sandbox_zero_count -= 1
            need += 1
        self.set_window_in_pconfig(self.window)
        self.set_sandbox_in_pconfig(self.sandbox)
        logging.debug('done:\t\t' + str(self))

    def rearrange_from_sorted_sandbox(self):
        logging.debug('rearranging:\t' + str(self))
        need = self.window_zero_count - self.pattern_zero_count
        while need > 0 and self.sandbox[-1]:
            self.window[-(len(self.window) - self.window_zero_count) - 1] = 1
            self.sandbox[self.sandbox_zero_count] = 0
            self.window_zero_count -= 1
            self.sandbox_zero_count += 1
            need -= 1
        while need < 0 and not self.sandbox[0]:
            self.window[self.window_zero_count] = 0
            self.sandbox[self.sandbox_zero_count - 1] = 1
            self.window_zero_count += 1
            self.sandbox_zero_count -= 1
            need += 1
        self.set_window_in_pconfig(self.window)
        self.set_sandbox_in_pconfig(self.sandbox)
        logging.debug('done:\t\t' + str(self))


    def swap(self):
        logging.debug('swapping R' + str(self.ID))
        self.window, self.sandbox = self.sandbox, self.window  # local copy
        self.window_zero_count, self.sandbox_zero_count = self.sandbox_zero_count, self.window_zero_count
        self.set_window_in_pconfig(self.window)  # actually modifying in pconfig
        self.set_sandbox_in_pconfig(self.sandbox)

    def _reach_pattern(self, arr: bitarray):
        for i in range(0,len(arr)):
            if arr[i] != self.pattern[i]:
                for j in range(i + 1,len(arr)):
                    if arr[j] != self.pattern[j] and arr[j] != arr[i]:
                        arr[i], arr[j] = arr[j], arr[i]
                        break
        if arr != self.pattern:
            logging.warning('ERROR REACHING PATTERN!')
            logging.warning('have ' + str(arr))
            logging.warning('want '+ str(self.pattern))
            logging.warning(self)
            sys.exit(0)
        return arr

    def reach_pattern(self):
        logging.debug( 'R' + str(self.ID) + ': swapping locally to reach pattern...')
        self.window = self._reach_pattern(self.window)
        self.sandbox = self._reach_pattern(self.sandbox)
        self.set_window_in_pconfig(self.window)
        self.set_sandbox_in_pconfig(self.sandbox)

    def algo_iter(self):
        self.check_local_validity()
        self.update_status()
        if self.done:
            return
        if self.status:
            if self.consecutive_valid_windows_seen < self.total_window_count:
                self.reach_pattern()
                return
            else:
                logging.debug('DONE!: R' + str(self.ID))
                self.done = 1
                return

        if not self.has_valid_sandbox() and not self.has_valid_window():
            self.rearrange_from_unsorted_sandbox()

        if self.window_zero_count > self.pattern_zero_count:
                # someone else is stuck with my 1s. I expulse my window
                # and hope they will catch it.
                self.swap()
