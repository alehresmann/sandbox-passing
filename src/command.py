class command:
    def __init__(self, bot, count_as_op=True):
        self.bot = bot
        self.count_as_op = count_as_op

    def execute(self):
        pass

    # to be able to print commands in a list
    def __repr__(self):
        return self.__str__()


class switch_command(command):
    def __init__(
        self, bot, first_index, second_index, first_in_window, second_in_window
    ):
        command.__init__(self, bot)
        self.indices = [first_index, second_index]
        self.in_windows = [first_in_window, second_in_window]

    def __str__(self):
        return (
            "switch "
            + str(self.indices[0])
            + " in "
            + ("w" if self.in_windows[0] else "s")
            + " and "
            + str(self.indices[1])
            + " in "
            + ("w" if self.in_windows[1] else "s")
        )

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
        return "move"

    def execute(self):
        if self.forward:
            new_node_to_add = self.bot.sandbox[-1].next
            abandoned_node = self.bot.current_node
            new_current_node = self.bot.current_node.next
        else:
            new_node_to_add = self.bot.current_node.prev
            abandoned_node = self.bot.sandbox[-1]
            new_current_node = self.bot.current_node.prev

        if abandoned_node.owned_by == self.bot:
            abandoned_node.owned_by = None
        self.bot.current_node = new_current_node
        new_node_to_add.owned_by = self.bot

        self.bot.update_window_and_sandbox()
