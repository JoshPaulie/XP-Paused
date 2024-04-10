"""
Simple subclassed version of the rich console, with a custom prefix.
`Console.log()` doesn't have any way to customize the prefix, afaik
"""

import datetime as dt

from rich.console import Console


class PrintPrefixConsole(Console):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def print(self, *objects, sep=" ", end="\n", **kwargs):
        timestamp = f"[bright_white][{dt.datetime.now().strftime('%I:%M %p')}][/] "
        objects = (timestamp + str(obj) for obj in objects)
        super().print(*objects, sep=sep, end=end, **kwargs)


console = PrintPrefixConsole()
