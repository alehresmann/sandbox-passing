from bitarray import bitarray


class robot:
    def __init__(self, pattern: bitarray, window: bitarray, sandbox: bitarray, ID: int, num_of_other_bots: int):

        self.pattern = pattern.copy()
        self.window = window.copy()
        self.sandbox = sandbox.copy()
        self.ID = ID
        self.num_of_other_bots = num_of_other_bots

        self.pattern_zero_count = pattern.count(0)
        self.window_zero_count = window.count(0)
        self.sandbox_zero_count = sandbox.count(0)
        self.num_of_other_bots = num_of_other_bots
        self.satisfaction_array = bitarray('0' * num_of_other_bots)
        self.done = False

    def __str__(self):
        return self.window.to01() + '|' + self.sandbox.to01()

    def _sort(self, to_be_sorted: bitarray):
        j = 0
        for i in range(len(to_be_sorted)):
            if not to_be_sorted[i]:  # if to_be_sorted[i] is 0, swap with bit at j
                to_be_sorted[j], to_be_sorted[i] = to_be_sorted[i], to_be_sorted[j]
                j += 1
        return to_be_sorted

    def has_valid_window(self):
        return self.window_zero_count == self.pattern_zero_count

    def has_valid_sandbox(self):
        return self.sandbox_zero_count == self.pattern_zero_count

    def preliminary(self):
        self.window = self._sort(self.window)
        self.sandbox = self._sort(self.sandbox)

    def rearrange_from_sandbox(self):
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

    def swap(self):
        self.window, self.sandbox = self.sandbox, self.window
        self.window_zero_count, self.sandbox_zero_count = self.sandbox_zero_count, self.window_zero_count

    def trade_sandbox_with(self, other):  # other: robot
        self.sandbox, other.sandbox = other.sandbox, self.sandbox
        self.sandbox_zero_count, other.sandbox_zero_count = other.sandbox_zero_count, self.sandbox_zero_count

    def send_satisfaction_array(self, other):
        self.satisfaction_array[self.ID] = (self.has_valid_window()
                and self.has_valid_window())
        other.satisfaction_array = self.satisfaction_array.copy()

    def _reach_pattern(self, arr: bitarray):
        j = len(arr) - 1
        for i in range(0, int((len(arr) + 1) /2) ):
            if arr[i] != self.pattern[i]:
                while arr[j] == self.pattern[j]:
                    j -= 1
                    if j < i:
                        print('something went wrong while reaching pattern!')
                        sys.exit(0)
                arr[i], arr[j] = arr[j], arr[i]
        return arr

    def reach_pattern(self):
        self.window = self._reach_pattern(self.window)
        self.sandbox = self._reach_pattern(self.sandbox)
