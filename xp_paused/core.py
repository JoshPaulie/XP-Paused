import datetime as dt
import sys
import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from rich import print
from windows_toasts import Toast, WindowsToaster

status_page_url = "https://secure.runescape.com/m=news/game-status-information-centre?oldschool=1"

def status_page_changed():
    print("Uh oh! It seems Jagex changed their status page, and server status couldn't be determined.")
    user_request_open_in_browser = input("Open status page in your default browser [y/n]: ")
    if user_request_open_in_browser.lower() in ["y", "yes"]:
        webbrowser.open_new(status_page_url)
    sys.exit()
        
# TODO: Create function that fetches the page returns soup
# TODO: Create function that gets approx. downtime
# TODO: Create function that displays the finished downtime ETA in local timezone
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


def stalk_servers():
    first_check = True
    start_time = dt.datetime.now()

    # Windows Notification
    toaster = WindowsToaster("python")
    servers_online_toast = Toast()
    servers_online_toast.text_fields = ["OldSchool Servers are online!", "Go earn some xp!"]
    

    # Determine server status every X seconds
    while True:
        soup = get_soup()

        # Server back online check
        if not is_offline(soup):
            break 

        first_check = False
        print(f"[{dt.datetime.now().strftime("%I:%M %p")}] Servers are [red]offline[/].. ")
        time.sleep(90)

    if first_check:
        print("The servers are already [green]online[/]!")
        sys.exit()

    # Determine script elapsed time
    servers_online_time = dt.datetime.now()
    xp_paused_elapsed_time = servers_online_time - start_time
    runtime_message = f"Script runtime: {xp_paused_elapsed_time.seconds // 60} minutes"
    servers_online_toast.text_fields.append(runtime_message)

    # Send notification, final print statements
    print(f"[{dt.datetime.now().strftime("%I:%M %p")}] Servers are back [green]online[/]!\a")
    print(runtime_message)
    toaster.show_toast(servers_online_toast)


