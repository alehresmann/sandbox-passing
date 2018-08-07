import sys
import logging

from circular_list import node


class command():
    def __init__(self, bot, count_as_op = True):
        self.bot = bot
        self.count_as_op = count_as_op

    def execute(self):
        pass


class switch_command(command):
    def __init__(self, bot, first_index, second_index, first_in_window, second_in_window):
        command.__init__(self, bot)
        self.indices = [first_index, second_index]
        self.in_windows = [first_in_window, second_in_window]

    def __str__(self):
        return 'switch ' + str(self.indices[0]) + ', ' + str(self.in_windows[0]) \
                + ' and '+ str(self.indices[1]) + ', ' + str(self.in_windows[1])

    def execute(self):
        switch = []
        for i in range(0, len(self.in_windows)):
            if self.in_windows[i]:
                switch.append(self.bot.window[self.indices[i]])
            else:
                switch.append(self.bot.sandbox[self.indices[i]])
        switch[0].data, switch[1].data = switch[1].data, switch[0].data
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

        if new_node_to_add.owned_by is not None and not self.bot.is_synchronised:
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


class update_state_command(command):  # as this should be done once every $p$ bits, I added it as an instantaneous command.
    def __init__(self, bot):
        command.__init__(self, bot, False)

    def __str__(self):
        return 'update_state'

    def execute(self):
        # checks if window and sandbox is valid, adds to consecutive slices, sets states.
        if self.bot.has_valid_window():
            self.bot.consecutive_valid_windows_seen += 1
        else:
            self.bot.consecutive_valid_windows_seen = 0

        if self.bot.consecutive_valid_windows_seen >= self.bot.k:
            self.bot.state += 1
            print('STATE', self.bot.state)
            if self.bot.state == 2:
                self.bot.reached_done_at = self.bot.total_rounds
            self.bot.consecutive_valid_windows_seen = 0
