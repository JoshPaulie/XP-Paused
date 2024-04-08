"""
Module calls Osascript from Python to issue notifications on MacOS

Unsigned binaries of Python (self compiled) can't send notifications, detailed below
https://github.com/Jorricks/macos-notifications/issues/8
"""

import os


def macos_notification(text: str, *, title: str, subtitle: str):
    """Utilize osascript to send MacOS notifications. Dependency free!"""
    args = [
        f'display notification "{text}"',
        f'with title "{title}"',
        f'subtitle "{subtitle}"',
        'sound name "frog"',
    ]
    args_concat = " ".join(args)
    command = f"osascript -e '{args_concat}'"
    result = os.system(command)
    return result
