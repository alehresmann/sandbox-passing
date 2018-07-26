import sys
import logging

from circular_list import node

class command():
    def __init__(self, bot, count_as_op = True):
        self.bot = bot
        self.count_as_op = count_as_op

    def execute(self):
        pass

class local_rearrange_command(command):
    def __init__(self, bot):
        command.__init__(self, bot)

    def __str__(self):
        return 'local rearrange'

    def execute(self):
        logging.debug('R' + str(self.bot.ID) + ' rearranging...')
        window_zero_count = [w.data for w in self.bot.window].count(False)
        sandbox_zero_count = [s.data for s in self.bot.sandbox].count(False)
        pattern_zero_count = self.bot.pattern.count(0)

        if window_zero_count < pattern_zero_count and sandbox_zero_count > 0:
            want = True
        elif window_zero_count > pattern_zero_count and sandbox_zero_count < self.bot.slice_size:
            want = False
        for node in self.bot.window:
            if node.data == want:
                for node_s in self.bot.sandbox:
                    if not node_s.data == want:
                        node.data, node_s.data = node_s.data, node.data

                        self.bot.total_switches_done += 1
                        return
        logging.warning('tried to rearrange but couldn\'t! something went wrong here! R' + str(self.bot.ID))
        sys.exit(0)


class swap_command(command):
    def __init__(self, bot, index):
        command.__init__(self, bot)
        self.index = index

    def __str__(self):
        return 'swap data bits in window and sandbox at index ' + str(self.index)

    def execute(self):
        self.bot.window[self.index].data, self.bot.sandbox[self.index].data \
        = self.bot.sandbox[self.index].data, self.bot.window[self.index].data
        self.bot.total_switches_done += 1

class move_command(command):
    def __init__(self, bot, forward: bool):
        command.__init__(self, bot)
        self.forward = forward

    def __str__(self):
        return 'move'

    def execute(self):
        if self.forward:
            new_node_to_add = self.bot.sandbox[-1].next
            abandoned_node = self.bot.current_node
            new_current_node = self.bot.current_node.next
        else:
            new_node_to_add = self.bot.current_node.prev
            abandoned_node = self.bot.sandbox[-1]
            new_current_node = self.bot.current_node.prev

        if new_node_to_add.owned_by is not None:
                self.bot.total_time_waited += 1
            # if one wants to include the code below, it would need to be stacked, that is, if a
            # robot R1 is blocking a robot R2 that is blocking a robot R3, R3 should push both R2 and R1, or none at all.
            #if not len(new_node_to_add.owned_by.commands) > 0 \
            #or not type(new_node_to_add.owned_by.commands[0]) == move_command \
            #or not new_node_to_add.owned_by.commands[0].forward == self.forward:
                # in other words, if the next robot isn't about to move in the same direction we are
                logging.debug('R' + str(self.bot.ID) + ' PUSHING.')
                # WAIT 1 tick code below tries to push nodes off
                # push robot blocking the way
                #new_node_to_add.owned_by.commands = []
                #for i in range(0, self.bot.slice_size):
                #    new_node_to_add.owned_by.commands.append(move_command(new_node_to_add.owned_by, self.forward))

                # since this command failed to execute as another robot was in front,
                # insert a new move. Consider this a 'wait' op. maybe implement a check
                # to verify no one is behind me before doing a swap so that waiting is avoided?
                self.bot.commands.insert(0,move_command(self.bot, self.forward))
                return

        if abandoned_node.owned_by == self.bot:
            abandoned_node.owned_by = None
        self.bot.current_node = new_current_node
        new_node_to_add.owned_by = self.bot
        self.bot.update_window_and_sandbox()
        self.bot.total_moves_done += 1


class reach_pattern_command(command):
    def __init__(self, bot, in_window):
        command.__init__(self, bot)
        self.in_window = in_window

    def __str__(self):
        return 'reach pattern, in window? : ' + str(self.in_window)

    def execute(self):
        if self.in_window:
            local_slice = self.bot.window
        else:
            local_slice = self.bot.sandbox

        for i in range(0, self.bot.slice_size):
            if local_slice[i].data != self.bot.pattern[i]:
                for j in range(i, self.bot.slice_size):
                    if local_slice[j].data != self.bot.pattern[j] and local_slice[i].data != local_slice[j].data:
                        local_slice[i].data, local_slice[j].data = local_slice[j].data, local_slice[i].data

                        self.bot.total_switches_done += 1
                        return
        logging.debug('something went wrong whilst reaching pattern! R' + str(self.bot.ID))

        sys.exit(0)

class update_state_command(command):  # as this should be done once every $p$ bits, I added it as an instantaneous command.
    def __init__(self, bot):
        command.__init__(self, bot, False)

    def __str__(self):
        return 'update_state'

    def execute(self):
        logging.debug('R' + str(self.bot.ID) + ' UPDATING STATE')
        # checks if window and sandbox is valid, adds to consecutive slices, sets states.
        if self.bot.has_valid_window() and self.bot.has_valid_sandbox():
            self.bot.consecutive_valid_windows_seen += 1
        else:
            self.bot.consecutive_valid_windows_seen = 0

        if self.bot.consecutive_valid_windows_seen >= self.bot.k:
            self.bot.state += 1
            self.bot.consecutive_valid_windows_seen = 0
