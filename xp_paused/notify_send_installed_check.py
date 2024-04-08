# When imported, this module informs the user if they don't have notify-send installed
import subprocess

from .console import console

try:
    subprocess.check_output("notify_send")
except FileNotFoundError:
    console.print(
        "[yellow]Info[/]: [blue]notify-send[/] isn't installed. Linux desktop notifications depend on this package."
    )
