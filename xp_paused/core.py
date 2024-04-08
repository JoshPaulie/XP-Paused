import datetime as dt
import os
import subprocess
import sys
import time
import webbrowser

import requests
from bs4 import BeautifulSoup

from .console import console
from .macos_notification import macos_notification

if os.name == "nt":
    # Dependency is only installed on Windows
    # trying to install on other OS will cause import error
    from windows_toasts import Toast, WindowsToaster

if os.name == "posix" and sys.platform != "darwin":
    import notify_send_installed_check

status_page_url = "https://secure.runescape.com/m=news/game-status-information-centre?oldschool=1"


def status_page_changed():
    console.print(
        "Uh oh! It seems Jagex changed their status page, and server status couldn't be determined."
    )
    user_request_open_in_browser = input("Open status page in your default browser [y/n]: ")
    if user_request_open_in_browser.lower() in ["y", "yes"]:
        webbrowser.open_new(status_page_url)
    sys.exit(1)


# TODO: Create function that gets approx. downtime
# TODO: Create function that displays the approx uptime ETA in user local timezone
def get_soup() -> BeautifulSoup:
    """Returns the parsed source code of the status page"""
    status_page_source = requests.get(status_page_url).text
    return BeautifulSoup(status_page_source, "html.parser")


def get_status(soup: BeautifulSoup) -> str:
    # Why they used a "font" tag here will always baffle me
    server_status = soup.find_all("font")

    # For whatever reason, .find_next() won't find the font tag, likely because it's nested in a center tag
    # Until I am smarter than I am now, we'll instead .find_all() and exit if the list is empty
    if not server_status:
        status_page_changed()

    return server_status[0].get_text()


def is_offline(soup: BeautifulSoup) -> bool:
    status = get_status(soup)

    if not status.endswith(("ONLINE", "OFFLINE")):
        status_page_changed()

    if get_status(soup).endswith("OFFLINE"):
        return True
    return False


def send_servers_online_notification(elapsed_time_message: str):
    servers_online_message = "OldSchool Servers are online!"
    go_earn_xp_message = "Go earn some xp!"

    # Windows Notification
    if os.name == "nt":
        toaster = WindowsToaster("python")
        servers_online_toast = Toast()
        servers_online_toast.text_fields = [servers_online_message, go_earn_xp_message]
        servers_online_toast.text_fields.append(elapsed_time_message)
        toaster.show_toast(servers_online_toast)
        return

    # MacOS notification
    if sys.platform == "darwin":
        macos_notification(elapsed_time_message, title=servers_online_message, subtitle=go_earn_xp_message)
        return

    if os.name == "posix":
        try:
            subprocess.run(
                ["notify-send", "-t", "2500", servers_online_message, go_earn_xp_message],
                check=True,
            )
        except FileNotFoundError:
            pass
        except Exception as ex:
            console.print(f"An unknown error occurred sending a linux notification: [red]{ex}[/]")
            console.print(
                "Please consider filing an [link=https://github.com/JoshPaulie/XP-Paused/issues]issue[/link]."
            )
            console.print(elapsed_time_message)


def stalk_servers():
    first_check = True
    start_time = dt.datetime.now()

    # Determine server status every X seconds
    while True:
        soup = get_soup()

        # Server back online check
        if not is_offline(soup):
            break

        first_check = False
        console.print(f"Servers are [red]offline[/].. ")
        time.sleep(90)

    if first_check:
        console.print("The servers are already [green]online[/]!")
        sys.exit()

    # Determine script elapsed time
    servers_online_time = dt.datetime.now()
    xp_paused_elapsed_time = servers_online_time - start_time
    elapsed_time_message = f"Script runtime: {xp_paused_elapsed_time.seconds // 60} minutes"

    # Send notification
    console.print(f"Servers are back [green]online[/]!\a")
    send_servers_online_notification(elapsed_time_message)
