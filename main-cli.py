"""Wingspan - a command line tool for bulk Pterodactyl server management
Copyright (C) 2026 Brahmtej Singh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>."""






# This is wingspan, Il be writing my targets and scopes for this project first.

# I realized that pterodactyl doesnt have purge options, or bulk server actions and all. I am making that.

# I will use ptero api, to connect with user's panel and task/schedule actions.

# Il make 2 versions, one for linux and one for windows. Only windows one would have GUI. I need to find a way to keep both in sync.

# Features planned:
# Bulk Suspend/Unsuspend (A Checkbox to select multiple servers and suspend them all at once)
# Bulk Delete (A Checkbox to select multiple servers and delete them all at once)
# Selective Purge (Deletes the servers which match scopes provided, + Dry run feature)
# Backup download (Download backups of selected servers)
# Bulk resource change, or Copy 1 server's resources and paste to multiple servers.
# Bulk Reinstall
# Bulk Transfer (Transfer multiple servers to another node, but does it one by one due to bandwidth limitations)
# Settings page for storing api keys and more.
# Email notifications to notify users for bulk actions if scheduled.
# Make a management tab in which all node's real specs (not just assigned specs, real specs) are shown, and heavy overloading or other parameter of servers are shown.
# Il take suggestions from UI of Proxmox and Proxmox Datacenter manager as thats a really good UI with a lot of pterodactyl usable features.
# User management features like Bulk Email, Bulk user delete, Specific User Purge (Like delete those without any server), User Clear (Clear all servers of a user)
# The complete flagship feature of panel speed booster, which does all required purges and makes panel faster
# Update monitor, so users can safely and reliably update their wingspan installation and get prompted whenever a new release is put.

# Features for future:
# Wings install: Add a panel's api key + ssh credentials of a fresh vps, and it installs and sets up wings and sets up node.
# DB Setup: Same as wings install, add the cred and it makes mysql db through ssh and sets it up on panel automatically.
# Server side Wingspan (A version that runs on your pterodactyl panel which connects with your windows/linux sessions to execute scheduled actions in future)
# Essentially add Ai capabilities in future to automate pterodactyl actions even more.


# Basic Settings / Imports


#----------Auto Dependencies Check and Install------------
import os
import sys
import subprocess
import hashlib

IS_WINDOWS = sys.platform.startswith("win")
IS_LINUX = sys.platform.startswith("linux")

def _bootstrap():
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(project_root, ".venv")
    requirements_path = os.path.join(project_root, "requirements.txt")
    hash_marker_path = os.path.join(venv_dir, ".requirements.hash")

    venv_python = os.path.join(
        venv_dir,
        "Scripts" if IS_WINDOWS else "bin",
        "python.exe" if IS_WINDOWS else "python",
    )

    current_python = os.path.normcase(os.path.abspath(sys.executable))
    target_python = os.path.normcase(os.path.abspath(venv_python))
    if current_python == target_python:
        return

    first_time = not os.path.exists(venv_python)
    if first_time:
        print("[Wingspan] First run detected, creating virtual environment... Please wait, it may take time...")
        import venv as venv_module
        venv_module.EnvBuilder(with_pip=True, upgrade_deps=True).create(venv_dir)
        print("[Wingspan] Virtual environment created.")

    pip_check = subprocess.run(
        [venv_python, "-m", "pip", "--version"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if pip_check.returncode != 0:
        print("[Wingspan] pip missing inside venv, trying to fix it...")
        fix = subprocess.run(
            [venv_python, "-m", "ensurepip", "--upgrade"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if fix.returncode != 0:
            print(
                "[Wingspan] Could not install pip automatically.\n"
                "On Debian/Ubuntu this usually means python3-venv is missing. Run:\n\n"
                "    sudo apt update && sudo apt install python3-venv python3-pip\n\n"
                "Then delete the broken .venv folder and run this script again:\n\n"
                f"    rm -rf {venv_dir}\n"
                f"    python3 {os.path.abspath(__file__)}\n"
            )
            sys.exit(1)
        print("[Wingspan] pip fixed.")

    if os.path.exists(requirements_path):
        with open(requirements_path, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()

        previous_hash = None
        if os.path.exists(hash_marker_path):
            with open(hash_marker_path, "r") as f:
                previous_hash = f.read().strip()

        if first_time or current_hash != previous_hash:
            print("[Wingspan] Installing dependencies...")
            result = subprocess.run(
                [venv_python, "-m", "pip", "install", "-q", "-r", requirements_path]
            )
            if result.returncode != 0:
                print("[Wingspan] Dependency install failed. Check requirements.txt or your connection.")
                sys.exit(1)
            with open(hash_marker_path, "w") as f:
                f.write(current_hash)
            print("[Wingspan] Dependencies installed.")
    else:
        print(f"[Wingspan] Warning: no requirements.txt found at {requirements_path}, skipping installs.")

    if IS_WINDOWS:
        curses=subprocess.run([venv_python, "-m", "pip", "install", "-q", "windows-curses"])
        result = subprocess.run([venv_python, os.path.abspath(__file__)] + sys.argv[1:])
        
        sys.exit(result.returncode)
    else:
        os.execv(venv_python, [venv_python, os.path.abspath(__file__)] + sys.argv[1:])


def _enable_ansi_on_windows():
    if not IS_WINDOWS:
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    except Exception:
        pass


_bootstrap()
_enable_ansi_on_windows()


#--------------------------Imports--------------------------

import logging
import time, json, requests, threading, datetime,random,argparse,venv,curses,re,fnmatch,csv
from dotenv import load_dotenv
from pytterns import Pytterns
from colorama import Fore,Style, Back
pt = Pytterns()
if IS_WINDOWS:
    import tkinter

load_dotenv()

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")
LOG_PATH = os.path.join(PROJECT_ROOT, "wingspan.log")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

HEADERS = {
    'Authorization': f'Bearer {os.getenv("api_key")}',
    'Accept': 'Application/vnd.pterodactyl.v1+json'
}

def power_on_self_test():
    """
    Check if all configs are valid, API works, Logs work, Storage works etc. Continue if everything is fine, else exit with a message."""
    
    init_logger()
    logging.info("Starting Wingspan Power-On Self Test...")
    
    #---ENV---
    if os.path.exists(ENV_PATH):
        logging.info("Environment file found.")
    else:
        logging.critical(f"Environment file not found. Taking you to the setup wizard.")
        print(f"Environment file not found. Taking you to the setup wizard.")
        time.sleep(5)
        setup_wizard()
    #----Configs----
#    if os.path.exists(CONFIG_PATH):
#        logging.info("Config file found.")
#    else:
#        logging.critical(f"Config file not found. Please run 'setup' to create a config file.")
#        print(f"Error: Config file not found. Please run 'setup' to create a config file.")
#        exit(1)
    #----Storage----
    if os.path.exists(LOG_PATH):
        logging.info("Log file found.")
    else:
        logging.info("Created Logfile")
    
    logging.info("Wingspan Power-On Self Test completed successfully.")
  

def load_config():

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config


def save_config(config):
    """
    Overwrite the config.json file with the provided config dict. Save as Json
    """
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    logging.info("Config file saved successfully.")


#--------------------------------------------------------------------------------------------


def banner(animation=False, stars=False, clear=True):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    try:
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

            RESET   = "\033[0m"
            DIM     = "\033[2m"
            RIGGING = "\033[38;5;251m"
            STAR    = "\033[93m"
            STAR_DIM= "\033[38;5;58m"
            HULL    = "\033[38;5;180m"
            WATER   = "\033[36m"
            WAVE    = "\033[38;5;24m"
            GRAD = ["\033[38;5;51m", "\033[38;5;45m", "\033[38;5;39m",
                    "\033[38;5;33m", "\033[38;5;27m"]

            raw_lines = [
                "                          )       \\   /      (",
                "                         /|\\      )\\_/(     /|\\ ",   # <- fixed: trailing space
                "*                       / | \\    (/\\|/\\)   / | \\                      *",
                "|`.____________________/__|__o____\\`|'/___o__|__\\____________________.'|",
                "|                           '^`    \\|/   '^`                           |",
                "|                                   V                                  |",
                "|                                                                      |",
                "|     /|   _       _______   _____________ ____  ___    _   __  |\\     |",
                "|    //|  | |     / /  _/ | / / ____/ ___// __ \\/   |  / | / /  |\\\\    |",
                "|   ///|  | | /| / // //  |/ / / __ \\__ \\/ /_/ / /| | /  |/ /   |\\\\\\   |",
                "|  ////|  | |/ |/ // // /|  / /_/ /___/ / ____/ ___ |/ /|  /    |\\\\\\\\  |",
                "| /////|  |__/|__/___/_/ |_/\\____//____/_/   /_/  |_/_/ |_/     |\\\\\\\\\\ |",
                "| .__________________________________________________________________. |",
                "|'               l    /\\ /     \\\\            \\ /\\   l                 `|",
                "*                l  /   V       ))            V   \\ l                  *",
                "                 l/            //                  \\I",
                "                               V",
                
            ]

            colored_lines = [
                RIGGING + raw_lines[0] + RESET,
                RIGGING + raw_lines[1] + RESET,
                STAR + "*" + RIGGING + raw_lines[2][1:-1] + STAR + "*" + RESET,
                HULL + raw_lines[3] + RESET,
                HULL + raw_lines[4] + RESET,
                WATER + raw_lines[5] + RESET,
                raw_lines[6],
                GRAD[0] + raw_lines[7] + RESET,
                GRAD[1] + raw_lines[8] + RESET,
                GRAD[2] + raw_lines[9] + RESET,
                GRAD[3] + raw_lines[10] + RESET,
                GRAD[4] + raw_lines[11] + RESET,
                HULL + raw_lines[12] + RESET,
                WAVE + raw_lines[13] + RESET,
                STAR + "*" + WAVE + raw_lines[14][1:-1] + STAR + "*" + RESET,
                WAVE + raw_lines[15] + RESET,
                WAVE + raw_lines[16] + RESET,
            ]

            plain_width = max(len(l) for l in raw_lines)
            columns = os.get_terminal_size().columns
            padding = max((columns - plain_width) // 2, 0)
            pad_str = " " * padding

            if stars:
                star_field = [" " * plain_width for _ in range(2)]  # blank rows above ship
                for _ in range(24):
                    frame = ""
                    for _ in range(8):
                        chars = [" "] * plain_width
                        for _ in range(random.randint(1, 3)):
                            pos = random.randint(0, plain_width - 1)
                            chars[pos] = random.choice([STAR, STAR_DIM]) + "." + RESET
                        frame += pad_str + "".join(chars) + "\n"
                    sys.stdout.write(frame)
                    sys.stdout.flush()
                    time.sleep(0.08)
                    sys.stdout.write(f"\033[{8}A\033[J")  # move up & clear for next frame


            for line in colored_lines:
                sys.stdout.write(pad_str + line + "\n")
                sys.stdout.flush()
                if animation:
                    time.sleep(0.05)
            print()            
            # ASCII ART CREDITS TO Alan Greep
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def setup_wizard():
    """
    Interactive prompt (input()) asking for panel URL + API key,
    then calls save_config(). Used by `wingspan --setup`.
    TODO: implement
    """
    banner(animation=True, stars=True, clear=True)
    time.sleep(1)
    #--------------------------------------------------------------------------------------
    pt.panel(size=90,center=False,title="Wingspan Setup Wizard (1/3)", content=["Enter your Panel URL","(e.g. https://panel.example.com)"],border_bold=True,color="cyan")
    panel_url = input("--::>").strip()
    while not panel_url.startswith(("http://","https://")):
        print("Invalid URL. Please enter a valid URL starting with http:// or https://, and do not put a / at the end.")
        panel_url = input("--::>").strip()
        
    if panel_url.endswith("/"):
        panel_url = panel_url[:-1]
    
    
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    banner(False)
    pt.panel(size=90,center=False,title="Wingspan Setup Wizard (2/3)", content=["Enter your Admin User API Key", f"Make this at {panel_url}/account/api"],border_bold=True,color="cyan")
    admin_api_key=""
    times_wrong=0
    while not admin_api_key.startswith("ptlc_"):
        admin_api_key = input("--::>").strip()
        if admin_api_key.startswith("ptla_"):

            if times_wrong>=2:
                print(f"You have entered an Application API Key (Enter this in the next step).\nYou have entered a wrong key multiple times, I would guide you to setup.\nPlease visit {panel_url}/account/api and create a key and enter it here.")
                continue
            print("You have entered an Application API Key (Enter this in the next step). Please enter your Admin User API Key, starting with ptlc_.")
            times_wrong+=1
        elif not admin_api_key.startswith("ptlc_"):
            
            if times_wrong>=2:
                print(f"You have entered a wrong key multiple times, I would guide you to setup.\nPlease visit {panel_url}/account/api and create a key and enter it here.")
                continue
            print("Invalid API Key. Please enter a valid Admin User API Key starting with ptlc_.")
            times_wrong+=1
        

    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    banner(False)
    pt.panel(size=90,center=False,title="Wingspan Setup Wizard (3/3)", content=["Enter your Pterodactyl Application API Key", f"Make this at {panel_url}/admin/api"],border_bold=True,color="cyan")
    
    
    times_wrong=0
    api_key=""
    while not api_key.startswith("ptla_"):
        api_key = input("--::>").strip()
        if api_key.startswith("ptlc_"):

            if times_wrong>=2:
                print(f"You have entered an Admin User API Key.\nYou have entered a wrong key multiple times, I would guide you to setup.\nPlease visit {panel_url}/admin/api and create a key and enter it here.")
                continue
            print("You have entered an Admin User API Key. Please enter your Application API Key, starting with ptla_.")
            times_wrong+=1
        elif not api_key.startswith("ptla_"):
            
            if times_wrong>=2:
                print(f"You have entered a wrong key multiple times, I would guide you to setup.\nPlease visit {panel_url}/admin/api and create a key and enter it here.")
                continue
            print("Invalid API Key. Please enter a valid Application API Key starting with ptla_.")
            times_wrong+=1
        

    # Save the configuration
    env = {
        "api_key": api_key,
        "admin_api_key": admin_api_key,
        "panel_url": panel_url
    }
    with open(ENV_PATH, "w") as env_file:
        for key, value in env.items():
            env_file.write(f"{key}={value}\n")
            
    
    logging.info("Config file saved successfully.")
    
    save_config(env)
    banner()
    pt.panel(size=50,center=True,title="Setup Complete", content=["Setup is complete!","You can now run Wingspan and use its features.","Close this window and run script again"],border_bold=True,color="green")

    
# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def init_logger():
    
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger=logging.getLogger(__name__)

def log_action(level, action, server_id, server_name, before=None, after=None):
    logtext=f"Action: {action} was performed for server {server_name} ({server_id})."
    if before:
        logtext+=f" Before: {before}."
    if after:
        logtext+=f" After: {after}."
        
    level(logtext)



# ---------------------------------------------------------------------------
# API LAYER
# ---------------------------------------------------------------------------
if os.getenv("shipwrightmode")!="True":
    def api_request(method, endpoint, data=None):
        """
        Generic wrapper around urllib for talking to the Pterodactyl API.
        - method: "GET", "PATCH", "POST", "DELETE"
        - endpoint: e.g. "/api/application/servers"
        - config: dict from load_config()
        - data: dict to send as JSON body (for PATCH/POST)

        Should set headers:
            Authorization: Bearer <api_key>
            Content-Type: application/json
            Accept: Application/vnd.pterodactyl.v1+json

        Return parsed JSON response (dict), or None on failure.
        Handle urllib.error.HTTPError / URLError and print a useful message.
        TODO: implement
        """
        logging.info(f"API Request: {method} {endpoint} with data: {data}")
        req=requests.request(method=method, url=os.getenv("panel_url")+endpoint,headers=HEADERS, params=data if data else {})
        tries=0
        while req.status_code==429 and tries<10:
            tries+=1
            print(f"Rate Limited.. Trying after {5*tries} Seconds..")
            logging.warning(f"Rate Limited.. Trying after {5*tries} Seconds..")
            time.sleep(5*tries)
            req=requests.request(method=method, url=os.getenv("panel_url")+endpoint,headers=HEADERS, params=data if data else {})

        if str(req.status_code).startswith("2"):
            return req.json(),req.status_code
        elif str(req.status_code).startswith("4") or str(req.status_code).startswith("5"):
            return None,req.status_code
#else:
    #def api_request(method, endpoint, data=None):
        

def get_servers(limit=None):
    
    if limit==None:
        
        page=1
        data={'per_page': 200,'page':page}
        req,status=api_request("GET","/api/application/servers",data=data)
        
        
        if req and status==200:
            server_list=req
            total_pages=server_list["meta"]["pagination"]["total_pages"]
            if total_pages==1:
                return server_list

            else:
                data={'per_page': 200*total_pages,'page':page}
                req,status=api_request("GET","/api/application/servers",data=data)
                if req and status==200:
                    return req.json()
        else:
            print(f"Error while getting servers list at get_servers() : {status}")  
        
    else:
        data={'per_page': limit}
        api_request("GET", "/api/application/servers", data=data)

def get_server_details(config, server_id):
    """
    Fetch full detail for a single server by ID.
    Useful before showing a "before" value in dry-run mode.
    TODO: implement
    """
    pass


# ---------------------------------------------------------------------------
# FILTERING
# ---------------------------------------------------------------------------

def filter_servers(servers, node=None, status=None, name_pattern=None,
                    min_ram=None, max_ram=None, owner=None):
    """
    Take the full server list and narrow it down based on whichever
    filters are not None. Support wildcard matching for name_pattern
    (use fnmatch from stdlib, e.g. "mc-*").
    Return the filtered list.
    TODO: implement
    """
    pass

def flatten_dict(d):
    flat = {}
    for key, value in d.items():
        if isinstance(value, dict):
            flat.update(flatten_dict(value))
        else:
            flat[key] = value
    return flat

# ---------------------------------------------------------------------------
# OUTPUT / DISPLAY
# ---------------------------------------------------------------------------






def server_selector(stdscr, server_list, headers, all_selected=False):
    ANSI_RE = re.compile(r'\x1b\[([0-9;]*)m')
    ANSI_TO_CURSES = {
        30: curses.COLOR_BLACK, 31: curses.COLOR_RED, 32: curses.COLOR_GREEN,
        33: curses.COLOR_YELLOW, 34: curses.COLOR_BLUE, 35: curses.COLOR_MAGENTA,
        36: curses.COLOR_CYAN, 37: curses.COLOR_WHITE,
    }
    pair_cache = {}
    next_pair_id = [1]

    def get_pair(fg):
        if fg not in pair_cache:
            pid = next_pair_id[0]
            next_pair_id[0] += 1
            curses.init_pair(pid, fg, -1)
            pair_cache[fg] = curses.color_pair(pid)
        return pair_cache[fg]

    def visible_len(text):
        return len(ANSI_RE.sub('', text))

    def addstr_ansi(win, y, x, text, base_attr=0, max_width=None):
        cur_attr = base_attr
        cursor_x = x
        pos = 0

        for match in ANSI_RE.finditer(text):
            chunk = text[pos:match.start()]
            if chunk:
                if max_width is not None:
                    remaining = max_width - (cursor_x - x)
                    if remaining <= 0:
                        return
                    chunk = chunk[:remaining]
                try:
                    win.addstr(y, cursor_x, chunk, cur_attr)
                except curses.error:
                    pass
                cursor_x += len(chunk)

            codes = match.group(1)
            if codes in ("", "0"):
                cur_attr = base_attr
            else:
                for code_str in codes.split(";"):
                    if not code_str:
                        continue
                    code = int(code_str)
                    if code == 0:
                        cur_attr = base_attr
                    elif code in ANSI_TO_CURSES:
                        cur_attr = base_attr | get_pair(ANSI_TO_CURSES[code])
                    elif code == 1:
                        cur_attr |= curses.A_BOLD

            pos = match.end()

        chunk = text[pos:]
        if chunk:
            if max_width is not None:
                remaining = max_width - (cursor_x - x)
                chunk = chunk[:remaining] if remaining > 0 else ""
            if chunk:
                try:
                    win.addstr(y, cursor_x, chunk, cur_attr)
                except curses.error:
                    pass

    # --- setup ---
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()

    current = 0
    top = 0

    if all_selected:
        checked = set(range(len(server_list)))
    else:
        checked = set()

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        num_cols = len(headers)

        widths = [len(h) for h in headers]
        for server in server_list:
            for i in range(num_cols):
                text_len = visible_len(str(server[i]))
                if text_len > widths[i]:
                    widths[i] = text_len

        row_format = " | ".join("{:<" + str(w) + "}" for w in widths)

        addstr_ansi(stdscr, 0, 0, f"{Fore.BLUE}{Style.BRIGHT}Selector Menu (SPACE to check, ENTER to confirm, Q to quit)", max_width=width - 1)

        header_line = "    " + row_format.format(*headers)
        addstr_ansi(stdscr,2, 0, header_line[:width - 1], curses.A_BOLD)

        top_offset = 3
        rows_that_fit = height - top_offset

        if rows_that_fit <= 0:
            stdscr.refresh()
            stdscr.getch()
            continue

        visible = server_list[top:top + rows_that_fit]

        for i, server in enumerate(visible):
            real_index = top + i
            line = top_offset + i

            box = "[x] " if real_index in checked else "[ ] "
            values = [str(v) for v in server[:num_cols]]
            text = box + row_format.format(*values)

            style = curses.A_REVERSE if real_index == current else curses.A_NORMAL
            addstr_ansi(stdscr, line, 0, text, base_attr=style, max_width=width - 1)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current > 0:
            current -= 1
            if current < top:
                top = current

        elif key == curses.KEY_DOWN and current < len(server_list) - 1:
            current += 1
            if current >= top + rows_that_fit:
                top = current - rows_that_fit + 1

        elif key == ord(" "):
            if current in checked:
                checked.remove(current)
            else:
                checked.add(current)

        elif key in (10, 13, curses.KEY_ENTER):
            def strip_row(row):
                return [ANSI_RE.sub('', str(v)) for v in row]
            return [strip_row(server_list[i]) for i in sorted(checked)]
        elif key in (ord("q"), ord("Q")):
            return None
        
        
        
def export_csv(servers, filepath):
    """
    Write the server list out to a CSV file using the csv module.
    Useful for --output servers.csv
    TODO: implement
    """
    pass


def confirm_action(count, action_description):
    """
    Show the user exactly what's about to happen and how many servers
    are affected. Require them to type something explicit to proceed
    (e.g. type the number of servers, or type "yes").
    Return True if confirmed, False otherwise.
    TODO: implement
    """
    pass


# ---------------------------------------------------------------------------
# BULK ACTIONS
# ---------------------------------------------------------------------------

def bulk_resize(config, servers, ram=None, cpu=None, disk=None, swap=None,
                 dry_run=True):
    """
    Update resource limits on every server in `servers`.
    - Show a preview (old -> new) for each server first.
    - If dry_run is True, stop after the preview.
    - If not dry_run, call confirm_action(), then PATCH each server
      and log_action() the result.
    TODO: implement
    """
    pass


def bulk_power_action(config, servers, action, dry_run=True):
    """
    action is one of: "start", "stop", "restart", "kill"
    Send the power signal to every server in the filtered list.
    Same dry_run / confirm / log pattern as bulk_resize.
    TODO: implement
    """
    pass


def bulk_suspend(config, servers, suspend=True, dry_run=True):
    """
    Suspend (True) or unsuspend (False) every server in the list.
    Same dry_run / confirm / log pattern.
    TODO: implement
    """
    pass

def bulk_power(config, servers, action, dry_run=True):
    """
    Perform power actions (start, stop, restart, kill) on every server in the list.
    Same dry_run / confirm / log pattern.
    TODO: implement
    """
    pass

def bulk_purge(config, servers, dry_run=True, export_manifest_path=None):
    """
    THE DANGEROUS ONE.
    - Always show the full list of servers that will be deleted first.
    - If export_manifest_path is set, write server configs (name, egg,
      resources, owner) to that file BEFORE deleting anything.
    - If dry_run is True, stop after the preview - do not delete.
    - Require an extra-strict confirm_action() (e.g. typing the exact
      number of servers to delete, not just "yes").
    - DELETE each server via api_request(), log_action() each one.
    TODO: implement
    """
    pass


def bulk_reinstall(config, servers, dry_run=True):
    """
    Trigger a reinstall on every server in the list.
    Same dry_run / confirm / log pattern.
    TODO: implement
    """
    pass

# ---------------------------------------------------------------------------
# Terminal UI
# ---------------------------------------------------------------------------

def home_page():
    """
    Display a simple terminal UI with options to:
    - List servers
    - Bulk resize
    - Bulk power actions
    - Bulk suspend/unsuspend
    - Bulk purge
    - Bulk reinstall
    - Exit
    Use input() to get user choice and call the appropriate function."""
    time.sleep(1)
    
    banner(animation=True)
    pt.panel(size=60,center=False,title="HomePage [/]", content=["1. Search and Info","2. Purge","3. Power Actions","4. Suspension Manager", "5. Bulk Resource Change","6. Bulk Reinstall","S. Run Setup Again","Ctrl+C. Exit"],border_bold=True,color="cyan", center_content=False)

    home_inp = input("--::> ")
    

    while True:
        
        if home_inp=="1":
            banner()
            pt.panel(size=60,center=False,title="HomePage [/search-and-info/]", content=["1. Search Server [Search from Parameters]","2. Server Info [Get info from IDs]","H. Go Home","Ctrl+C. Exit"],border_bold=True,color="cyan", center_content=False)
            inp=input("--::> ").strip()
            if inp=="1":
                search_server()
                #break
            elif inp=="2":
                server_info()
                #break
            elif inp.lower()=="h":
                home_page()
                break
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                time.sleep(5)
                continue
        
        if home_inp=="2":
            banner()
            pt.panel(size=60,center=False,title="HomePage [/purge/]", content=["1. Purge Servers [Permanently Delete Servers]","2. Purge Users [Permanently Delete Users]","H. Go Home","Ctrl+C. Exit"],border_bold=True,color="cyan", center_content=False)
            inp=input("--::> ").strip()
            if inp=="1":
                purge_srv()
                #break
            if inp=="2":
                purge_users()
                #break
            elif inp.lower()=="h":
                home_page()
                break
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                time.sleep(5)
                continue
            
        elif home_inp in ["3","4","5","6"]:
            banner()
            pt.panel(size=60,center=False,title="HomePage [/coming-soon/]", content=["This feature is coming soon!","Please check back later."],border_bold=True,color="cyan", center_content=False)
            time.sleep(5)
            
        home_page()
        
def search_server():
    server_list=get_servers()
    try:
        parameters_list=list(server_list["data"][0]["attributes"].keys())
    except IndexError:
        print(f"{Fore.RED}{Style.BRIGHT}You dont have any servers on the Panel, or wingspan had an error fetching them. Sending you back to the homepage.")
        time.sleep(5)
        home_page()
        return
    converted=1
    while converted!=0:
        converted=0
        for i in parameters_list:
            try:
                new_parameters=list(server_list["data"][0]["attributes"][i].keys())
                parameters_list.remove(i)
                converted+=1
                for j in new_parameters:
                    parameters_list.append(j)
            except:
                pass

    params=[]
    for i in parameters_list:
        params.append([f"{Fore.YELLOW}{Back.LIGHTWHITE_EX}{i}"])
        
    selected_params = curses.wrapper(
    server_selector,
    server_list=params,
    headers=[f"{Fore.BLUE}Select all filters to filter from."])
    
    if selected_params is None:
        return

    parameters_filter=[]
    for i in selected_params:
        for j in i:
            parameters_filter.append(j)
    
    #servers_parametered=server_filter(server_list,parameters_filter)
    servers_filtering_list=server_list["data"]
    total_servers=len(servers_filtering_list)
    # -------------------Asking Answers to filters----------------------
    type_of_filter={'id':"int",
                    'external_id':"str",
                    'uuid':"str",
                    'identifier':"str",
                    'name':"str",
                    'description':"str",
                    'status':"str",
                    'suspended':"bool",
                    'user':"int",
                    'node':"int",
                    'allocation':"int",
                    'nest':"int",
                    'egg':"int",
                    'updated_at':"date",
                    'created_at':"date",
                    'memory':"int",
                    'swap':"int",
                    'disk':"int",
                    'io':"int",
                    'cpu':"int",
                    'threads':"str",
                    'oom_disabled':"bool",
                    'startup_command':"str",
                    'image':"str",
                    'installed':"bool",
                    'environment':"str",
                    'databases':"int",
                    'allocations':"int",
                    'backups':"int"}
    
    
    for current_parameter in parameters_filter:
        try:
            type_of_parameter=type_of_filter[current_parameter]
        except:
            type_of_parameter="custom"
            
        if type_of_parameter=="int":
            while True:
                banner()
                pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}[{len(servers_filtering_list)} / {total_servers} servers remaining]",f"Enter Value of {Fore.GREEN}{current_parameter}{Fore.RESET} Parameter",f"You can {Fore.GREEN}add a range{Fore.RESET} like this: {Fore.GREEN}30-100","",f"You can also {Fore.GREEN}combine selections{Fore.RESET} with a {Fore.GREEN}comma","",f"Like this: {Fore.GREEN}5,8,50-60,12","",f"{Fore.RED}Refer to docs for advanced search info",f"{Fore.YELLOW}{Style.DIM}Enter empty to bypass this filter"],border_bold=True,color="cyan")
                inp=input("--::> ")
                value=""
                # Spaces remove
                for i in inp:
                    if i != " ":
                        value+=i 
                
            # -------------------------------------------------
                if value=="":
                    # Bypass this filter
                    break
            
                if "," in value and "-" not in value:
                    # Uh, this means that the items are only single elements, so we can split directly.
                    a=value.split(",")
                    filters=[]
                    error=0
                    for i in a:
                        try:
                            i=int(i)
                            if i <0:
                                raise 0
                            filters.append(i)
                        except:
                            error=1
                    if error==1:
                        print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                        time.sleep(5)
                        continue
                    int_filters=filters
            # --------------------------------------------------------

                elif "," not in value and "-" in value:
                    # Means that the input is just a single range
                    try:
                        a=value.split("-")
                        ranges=[]
                        if len(a)!=2:
                            raise 0
                        
                        for i in a:
                            if int(i)<0:
                                raise 0
                            ranges.append(int(i))
                            
                        if ranges[0]>ranges[1]:
                            raise 0
                                            
                        
                        int_filters=range(ranges[0],ranges[1]+1)
                            
                            
                    except:
                        print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                        time.sleep(5)
                        continue


                elif "," in value and "-" in value:
                    # This is the last elif, means its the most complicated one, with both elements and ranges
                    
                    try:
                        
                        a=value.split(",")
                        
                        l1=[] #has all single elements
                        l2=[] #has all range elements
                        
                        for i in a:
                            if "-" in i:
                                l2.append(i)
                            else:
                                l1.append(i)
                                
                    #-----------------Simple Elements---------------------

                        l1_filters=[]
                        for i in l1:
                            i=int(i)
                            if i <0:
                                raise 0
                            l1_filters.append(i)
                            
                    #---------------------Range Elements---------------------
                        l2_filters=[]
                        for value in l2:
                            a=value.split("-")
                            ranges=[]
                            if len(a)!=2:
                                raise 0
                            
                            for i in a:
                                if int(i)<0:
                                    raise 0
                                ranges.append(int(i))
                                
                            if ranges[0]>ranges[1]:
                                raise 0
                            
                            l2_filters+=list(range(ranges[0],ranges[1]+1))


                                
                    #------------------------------------------------------------
                        combined_filters=l1_filters+l2_filters
                        final_filter=[]
                        for i in combined_filters:
                            if i not in final_filter:
                                final_filter.append(i)
                        int_filters=final_filter
                    # Final list ready with id_filters for all index numbers to be searched.            
                    except:
                        print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                        time.sleep(5)
                        continue
                
                else:
                    # Single element, no comma no dash
                    try:
                        n=int(value)
                        if n<0:
                            raise 0
                        int_filters=[n]
                    except:
                        print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                        time.sleep(5)
                        continue

                #--------------FILTER---------------
                servers_filtering_list = [
                    srv for srv in servers_filtering_list
                    if flatten_dict(srv["attributes"]).get(current_parameter) in int_filters
                ]
                print(f"{Fore.CYAN}[{current_parameter}] -> {len(servers_filtering_list)} / {total_servers} servers remaining.")
                time.sleep(1)
                break
                                    
        # --------------------------------------------------------------------------                        
        elif type_of_parameter=="bool":
            while True:
                banner()
                pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}[{len(servers_filtering_list)} / {total_servers} servers remaining]",f"Enter Value of {Fore.GREEN}{current_parameter}{Fore.RESET} Parameter",f"Enter {Fore.GREEN}yes{Fore.RESET} or {Fore.GREEN}no",f"{Fore.YELLOW}{Style.DIM}Enter empty to bypass this filter"],border_bold=True,color="cyan")
                inp=input("--::> ")
                value=""
                for i in inp:
                    if i != " ":
                        value+=i
                value=value.lower()
                
                if value=="":
                    break
                
                if value in ("yes","y","true","1"):
                    want=True
                elif value in ("no","n","false","0"):
                    want=False
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                    time.sleep(5)
                    continue
                
                servers_filtering_list = [
                    srv for srv in servers_filtering_list
                    if flatten_dict(srv["attributes"]).get(current_parameter) == want
                ]
                print(f"{Fore.CYAN}[{current_parameter}] -> {len(servers_filtering_list)} / {total_servers} servers remaining.")
                time.sleep(1)
                break
        
        # --------------------------------------------------------------------------
        elif type_of_parameter=="date":
            while True:
                banner()
                pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}[{len(servers_filtering_list)} / {total_servers} servers remaining]",f"Enter Date Range for {Fore.GREEN}{current_parameter}{Fore.RESET} Parameter",f"Format: {Fore.GREEN}YYYY-MM-DD,YYYY-MM-DD","",f"Like this: {Fore.GREEN}2024-01-01,2025-01-01","",f"{Fore.YELLOW}{Style.DIM}Enter empty to bypass this filter"],border_bold=True,color="cyan")
                inp=input("--::> ")
                value=""
                for i in inp:
                    if i != " ":
                        value+=i
                
                if value=="":
                    break
                
                try:
                    a=value.split(",")
                    if len(a)!=2:
                        raise 0
                    start_raw=a[0]
                    end_raw=a[1]
                    if start_raw.endswith("Z"):
                        start_raw=start_raw[:-1]+"+00:00"
                    if end_raw.endswith("Z"):
                        end_raw=end_raw[:-1]+"+00:00"
                    start=datetime.datetime.fromisoformat(start_raw)
                    if start.tzinfo is None:
                        start=start.replace(tzinfo=datetime.timezone.utc)
                    end=datetime.datetime.fromisoformat(end_raw)
                    if end.tzinfo is None:
                        end=end.replace(tzinfo=datetime.timezone.utc)
                    if start>end:
                        raise 0
                except:
                    print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                    time.sleep(5)
                    continue
                
                matched=[]
                for srv in servers_filtering_list:
                    raw=flatten_dict(srv["attributes"]).get(current_parameter)
                    if not raw:
                        continue
                    try:
                        check=raw
                        if check.endswith("Z"):
                            check=check[:-1]+"+00:00"
                        check_date=datetime.datetime.fromisoformat(check)
                        if check_date.tzinfo is None:
                            check_date=check_date.replace(tzinfo=datetime.timezone.utc)
                        if start<=check_date<=end:
                            matched.append(srv)
                    except:
                        pass
                servers_filtering_list=matched
                print(f"{Fore.CYAN}[{current_parameter}] -> {len(servers_filtering_list)} / {total_servers} servers remaining.")
                time.sleep(1)
                break

        # --------------------------------------------------------------------------
        else:
            
            while True:
                banner()
                pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}[{len(servers_filtering_list)} / {total_servers} servers remaining]",f"Enter Value of {Fore.GREEN}{current_parameter}{Fore.RESET} Parameter",f"You can {Fore.GREEN}combine selections{Fore.RESET} with a {Fore.GREEN}comma{Fore.RESET} (matches ANY of them)","",f"Use {Fore.GREEN}*{Fore.RESET} or {Fore.GREEN}%{Fore.RESET} as a wildcard, like {Fore.GREEN}node*{Fore.RESET} or {Fore.GREEN}*test*","",f"Wrap in {Fore.GREEN}/../{Fore.RESET} for raw regex, like {Fore.GREEN}/^py.*js$/","",f'Wrap in {Fore.GREEN}"..."{Fore.RESET} for a literal value, like {Fore.GREEN}"node*"{Fore.RESET} (ignores * and /)',"",f"Like this: {Fore.GREEN}suspended,py*","",f"{Fore.YELLOW}{Style.DIM}Enter empty to bypass this filter"],border_bold=True,color="cyan")
                inp=input("--::> ")
                
                if inp=="":
                    break
                
                a=inp.split(",")
                needles=[]
                for i in a:
                    i=i.strip()
                    if i!="":
                        needles.append(i)
                
                if not needles:
                    print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                    time.sleep(5)
                    continue
                
                patterns=[]
                error=0
                for n in needles:
                    try:
                        # AI GEN Code for wildcard checking and stuff:-
                        
                        if len(n)>=2 and n.startswith('"') and n.endswith('"'):
                            # Quoted, literal mode - ignores * % / entirely
                            literal=n[1:-1]
                            pattern=re.compile(re.escape(literal), re.IGNORECASE)
                            patterns.append((pattern,"search"))
                        elif n.startswith("/") and n.endswith("/") and len(n)>=2:
                            # Raw regex mode
                            pattern=re.compile(n[1:-1], re.IGNORECASE)
                            patterns.append((pattern,"search"))
                        elif "*" in n or "%" in n:
                            # Wildcard mode, * and % both act as wildcards
                            # fnmatch.translate anchors the END only (\Z), NOT the start,
                            # so it must be used with fullmatch, not search, or "p*" would
                            # match any string containing a "p" anywhere (like "Suspend").
                            wild=n.replace("%","*")
                            pattern=re.compile(fnmatch.translate(wild), re.IGNORECASE)
                            patterns.append((pattern,"fullmatch"))
                        else:
                            # Plain substring mode
                            pattern=re.compile(re.escape(n), re.IGNORECASE)
                            patterns.append((pattern,"search"))
                    except:
                        error=1
                
                if error==1:
                    print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                    time.sleep(5)
                    continue
                
                matched=[]
                for srv in servers_filtering_list:
                    val=flatten_dict(srv["attributes"]).get(current_parameter)
                    val_str=str(val)
                    hit=0
                    for p,mode in patterns:
                        if mode=="fullmatch":
                            if p.fullmatch(val_str):
                                hit=1
                        else:
                            if p.search(val_str):
                                hit=1
                    if hit==1:
                        matched.append(srv)
                servers_filtering_list=matched
                print(f"{Fore.CYAN}[{current_parameter}] -> {len(servers_filtering_list)} / {total_servers} servers remaining.")
                time.sleep(1)
                break

    banner()
    if not servers_filtering_list:
        print(f"{Fore.RED}No servers matched the given filters.")
    else:
        banner()
        print(f"{Fore.GREEN}Matched {len(servers_filtering_list)} / {total_servers} server(s).{Fore.RESET}\nPlease select the servers you want to export from the next menu.")
        input("Press Enter to continue...")
        
        selected_rows = curses.wrapper(
            server_selector,
            server_list=[[flatten_dict(srv["attributes"]).get("id"), flatten_dict(srv["attributes"]).get("name")] for srv in servers_filtering_list],
            headers=[f"{Fore.BLUE}ID", f"{Fore.BLUE}Name"],
            all_selected=True,
        )
        
        if selected_rows is None:
            print(f"{Fore.RED}No servers selected for export.")
            return
        
        servers_filtering_list=[]
        for srv in selected_rows:
            servers_filtering_list.append(srv)
        
        banner()
        pt.panel(size=70,center=False,title=f"/search-and-info/info/export", content=[f"Would you like to {Fore.GREEN}Export{Fore.RESET} the server list? ({len(servers_filtering_list)} Servers)","After exporting, you could use the list for other functions.","",f'Enter "{Fore.GREEN}y{Fore.RESET}" to export or "{Fore.GREEN}n{Fore.RESET}" to skip'],border_bold=True,color="cyan")
        while True:
            inp=input("--::>")
            if inp.lower() in ("y","yes"):
                pt.panel(size=70,center=False,title=f"/search-and-info/info/export", content=[f"Please enter a name for your export.",f"{Fore.GREEN}Enter this name to Re-Import this list in a function!{Fore.RESET}","You can access the export file in the exports folder","in this file's root dir, unless you enter a complete path."],border_bold=True,color="cyan")
                export_name=input("--::> ").strip()
                if "\\" in export_name or "/" in export_name:
                
                    pass
                else:
                    export_name="exports/"+export_name
                        
                    
                time.sleep(1)
                banner()
                
                export_list(['id','name'],servers_filtering_list,export_name+".csv")
                print(f"{Fore.GREEN}Exported {len(servers_filtering_list)} servers to {export_name}.csv successfully. Returning to Homepage.")
                time.sleep(5)
                return
            elif inp.lower() in ("n","no"):
                return
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Incorrect input entered or some error occurred, Please Re-Enter values correctly.")
                time.sleep(5)
                continue

def export_list(HEAD,servers,filepath):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(HEAD)
        for srv in servers:
            a = srv
            print(a)
            writer.writerow(a)
            
def server_info():
    # This function has a lot of AI use because it involves very complex GUI and formatting, which is not achievable by hand.
    banner()
    print(f"Enter the numerical {Fore.GREEN}Server ID{Fore.RESET} to get all related information.")

    APP_INCLUDE = "allocations,user,subusers,nest,egg,variables,location,node,databases"


    def app_get(endpoint, params=None):
        try:
            out = api_request("GET", endpoint, data=params)
        except Exception as e:
            logging.error(f"server_info app_get {endpoint}: {e}")
            return None, str(e)
        if not isinstance(out, tuple) or len(out) != 2:
            return None, "unexpected api_request return"
        payload, st = out
        if st == 200 and payload is not None:
            return payload, None
        return None, f"HTTP {st}"

    def client_get(path):
        key = os.getenv("admin_api_key")
        base = os.getenv("panel_url")
        if not key:
            return None, "admin_api_key not set in .env"
        if not key.startswith("ptlc_"):
            return None, "admin_api_key is not a ptlc_ client key"
        if not base:
            return None, "panel_url not set in .env"
        try:
            
            r = requests.get(
                base + path,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Accept": "application/json",
                },
                timeout=8,
            )
        except Exception as e:
            logging.error(f"server_info client_get {path}: {e}")
            return None, str(e)
        if r.status_code == 200:
            try:
                return r.json(), None
            except Exception as e:
                return None, f"bad json ({e})"
        reasons = {
            401: "HTTP 401 - key rejected",
            403: "HTTP 403 - key has no access to this server",
            404: "HTTP 404 - server not visible to this key",
            429: "HTTP 429 - rate limited",
        }
        return None, reasons.get(r.status_code, f"HTTP {r.status_code}")

    while True:
        raw_id = input("--::>").strip()
        if raw_id.lower() in ("q", "quit", "exit", "h", "back"):
            return
        try:
            server_id = int(raw_id)
        except Exception:
            print(f"{Fore.RED}{Style.BRIGHT}That is not a numeric server ID. Try again.")
            time.sleep(1.5)
            continue

        # =============================================================
        def dashboard(stdscr):
            COOLDOWN = 8
            LIVE_INTERVAL = 2.0
            HIST_MAX = 400
            HEAD_H = 3
            FOOT_H = 1

            curses.curs_set(0)
            curses.start_color()
            curses.use_default_colors()

            names = ["cyan", "green", "yellow", "red", "white", "magenta", "blue", "grey"]
            codes = [curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
                     curses.COLOR_RED, curses.COLOR_WHITE, curses.COLOR_MAGENTA,
                     curses.COLOR_BLUE, curses.COLOR_BLACK]
            C = {}
            for i, (n, code) in enumerate(zip(names, codes), start=1):
                try:
                    curses.init_pair(i, code, -1)
                    C[n] = curses.color_pair(i)
                except curses.error:
                    C[n] = 0

            LBL = C["cyan"]
            VAL = C["white"] | curses.A_BOLD
            DIM = C["grey"] | curses.A_BOLD
            OK = C["green"] | curses.A_BOLD
            WARN = C["yellow"] | curses.A_BOLD
            BAD = C["red"] | curses.A_BOLD
            ACC = C["magenta"] | curses.A_BOLD
            SUB = C["blue"] | curses.A_BOLD

            # probe whether this terminal can take block glyphs
            try:
                stdscr.addstr(0, 0, "\u2588\u2591")
                stdscr.erase()
                UNI = True
            except Exception:
                stdscr.erase()
                UNI = False

            if UNI:
                BAR_F, BAR_E = "\u2588", "\u2591"
                LEVELS = " \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
                DOT = "\u25cf"
                ARR_L, ARR_R = "\u2039", "\u203a"
                MORE_D, MORE_U = "\u25bc", "\u25b2"
            else:
                BAR_F, BAR_E = "#", "-"
                LEVELS = " ....::::"
                DOT = "*"
                ARR_L, ARR_R = "<", ">"
                MORE_D, MORE_U = "v", "^"

            S = {
                "app": None, "cli": None, "res": None,
                "backups": None, "schedules": None, "dbs": None,
                "subusers": {}, "errors": {},
                "fetched": 0.0, "last_try": 0.0,
                "flash": "", "flash_until": 0.0,
                "page": 0, "scroll": [0, 0, 0, 0, 0],
                "live": False, "last_poll": 0.0,
                "hist_cpu": [], "hist_mem": [], "hist_net": [],
                "prev_rx": None, "prev_tx": None, "prev_t": None,
                "rate_rx": 0.0, "rate_tx": 0.0,
            }

            PAGES = ["Overview", "Resources", "Access", "Configuration", "Infrastructure"]

            # ---------------- primitives ----------------
            def put(win, y, x, text, attr=0):
                if not text:
                    return
                try:
                    win.addstr(y, x, text, attr)
                except curses.error:
                    pass

            def fit(text, width):
                text = "-" if text is None or text == "" else str(text)
                text = text.replace("\r", " ").replace("\n", " ")
                if width <= 0:
                    return ""
                if len(text) <= width:
                    return text
                if width <= 3:
                    return text[:width]
                return text[: width - 3] + "..."

            def wrap(text, width):
                text = "-" if text is None or text == "" else str(text)
                text = text.replace("\r", " ").replace("\n", " ")
                if width <= 0:
                    return [text]
                out, cur = [], ""
                for word in text.split(" "):
                    if not word:
                        continue
                    if not cur:
                        cur = word
                    elif len(cur) + 1 + len(word) <= width:
                        cur += " " + word
                    else:
                        out.append(cur)
                        cur = word
                    while len(cur) > width:
                        out.append(cur[:width])
                        cur = cur[width:]
                if cur:
                    out.append(cur)
                return out or ["-"]

            def human_bytes(n):
                try:
                    n = float(n)
                except Exception:
                    return "-"
                for u in ("B", "KB", "MB", "GB", "TB"):
                    if abs(n) < 1024:
                        return f"{int(n)} {u}" if u == "B" else f"{n:.2f} {u}"
                    n /= 1024
                return f"{n:.2f} PB"

            def human_mb(n):
                try:
                    n = int(n)
                except Exception:
                    return "-"
                if n == 0:
                    return "Unlimited"
                if n >= 1024:
                    return f"{n} MB ({n/1024:.1f} GB)"
                return f"{n} MB"

            def human_uptime(ms):
                try:
                    s = int(ms) // 1000
                except Exception:
                    return "-"
                d, s = divmod(s, 86400)
                h, s = divmod(s, 3600)
                m, s = divmod(s, 60)
                if d:
                    return f"{d}d {h}h {m}m {s}s"
                if h:
                    return f"{h}h {m}m {s}s"
                if m:
                    return f"{m}m {s}s"
                return f"{s}s"

            def pdate(v):
                if not v:
                    return "-"
                try:
                    return datetime.datetime.fromisoformat(
                        str(v).replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    return str(v)

            def yn(v, good=True):
                if v is None:
                    return "-", DIM
                if v:
                    return "Yes", (OK if good else BAD)
                return "No", (BAD if good else OK)

            def bar(pct, width):
                try:
                    pct = max(0.0, min(float(pct), 100.0))
                except Exception:
                    pct = 0.0
                if width < 1:
                    return "", DIM, 0.0
                f = int(round(width * pct / 100.0))
                attr = OK if pct < 60 else (WARN if pct < 85 else BAD)
                return BAR_F * f + BAR_E * (width - f), attr, pct

            def draw_box(win, y, x, w, h, title, attr, subtitle=None):
                if w < 4 or h < 2:
                    return
                try:
                    win.hline(y, x + 1, curses.ACS_HLINE, w - 2, attr)
                    win.hline(y + h - 1, x + 1, curses.ACS_HLINE, w - 2, attr)
                    win.vline(y + 1, x, curses.ACS_VLINE, h - 2, attr)
                    win.vline(y + 1, x + w - 1, curses.ACS_VLINE, h - 2, attr)
                    win.addch(y, x, curses.ACS_ULCORNER, attr)
                    win.addch(y, x + w - 1, curses.ACS_URCORNER, attr)
                    win.addch(y + h - 1, x, curses.ACS_LLCORNER, attr)
                    try:
                        win.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER, attr)
                    except curses.error:
                        pass
                except curses.error:
                    pass
                if title:
                    put(win, y, x + 2, " " + fit(title, max(w - 6, 1)) + " ", attr | curses.A_BOLD)
                if subtitle:
                    t = " " + fit(subtitle, max(w - 8, 1)) + " "
                    put(win, y + h - 1, max(x + w - len(t) - 3, x + 2), t, DIM)

            def draw_graph(win, y, x, w, h, series, maxval, attr):
                if w < 2 or h < 1 or not series:
                    return
                data = series[-w:]
                if maxval is None or maxval <= 0:
                    maxval = max(max(data), 1.0)
                start = x + w - len(data)
                for i, v in enumerate(data):
                    try:
                        frac = max(0.0, min(float(v) / maxval, 1.0))
                    except Exception:
                        frac = 0.0
                    total = frac * h * 8
                    for row in range(h):
                        cell = total - row * 8
                        if cell <= 0:
                            continue
                        ch = LEVELS[8] if cell >= 8 else LEVELS[max(int(cell), 1)]
                        if ch == " ":
                            continue
                        put(win, y + h - 1 - row, start + i, ch, attr)

            # ---------------- loading screen ----------------
            STEPS = [
                "Server details (application API)",
                "Client details (client API)",
                "Live resource usage",
                "Databases / backups / schedules",
                "Subuser accounts",
            ]

            def loading(stdscr, done, note=""):
                stdscr.erase()
                rows, cols = stdscr.getmaxyx()
                bw = min(max(cols - 10, 30), 66)
                bh = len(STEPS) + 6
                by = max((rows - bh) // 2, 0)
                bx = max((cols - bw) // 2, 0)
                draw_box(stdscr, by, bx, bw, bh, "WINGSPAN", ACC)
                put(stdscr, by + 1, bx + 2, fit(f"Loading server {server_id}", bw - 4), VAL)
                for i, step in enumerate(STEPS):
                    yy = by + 3 + i
                    if i < done:
                        put(stdscr, yy, bx + 2, "[ok] ", OK)
                        put(stdscr, yy, bx + 7, fit(step, bw - 9), DIM)
                    elif i == done:
                        put(stdscr, yy, bx + 2, "[..] ", WARN)
                        put(stdscr, yy, bx + 7, fit(step, bw - 9), VAL)
                    else:
                        put(stdscr, yy, bx + 2, "[  ] ", DIM)
                        put(stdscr, yy, bx + 7, fit(step, bw - 9), DIM)
                pw = bw - 6
                filled = int(pw * done / max(len(STEPS), 1))
                put(stdscr, by + bh - 3, bx + 3, BAR_F * filled + BAR_E * (pw - filled), ACC)
                if note:
                    put(stdscr, by + bh - 2, bx + 3, fit(note, bw - 6), DIM)
                stdscr.refresh()

            # ---------------- data loading ----------------
            def sample_resources():
                ra = (S["res"] or {}).get("attributes", {}) or {}
                rr = ra.get("resources", {}) or {}
                lim = ((S["app"] or {}).get("attributes", {}) or {}).get("limits", {}) or {}
                cpu_lim = lim.get("cpu") or 0
                cpu_abs = rr.get("cpu_absolute") or 0
                cpu_pct = (cpu_abs / cpu_lim * 100.0) if cpu_lim else float(cpu_abs)
                mem_b = rr.get("memory_bytes") or 0
                mem_lim = (lim.get("memory") or 0) * 1024 * 1024
                mem_pct = (mem_b / mem_lim * 100.0) if mem_lim else 0.0

                now = time.time()
                rx = rr.get("network_rx_bytes") or 0
                tx = rr.get("network_tx_bytes") or 0
                if S["prev_t"] and now > S["prev_t"]:
                    dt = now - S["prev_t"]
                    S["rate_rx"] = max((rx - (S["prev_rx"] or 0)) / dt, 0.0)
                    S["rate_tx"] = max((tx - (S["prev_tx"] or 0)) / dt, 0.0)
                S["prev_rx"], S["prev_tx"], S["prev_t"] = rx, tx, now

                S["hist_cpu"].append(cpu_pct)
                S["hist_mem"].append(mem_pct)
                S["hist_net"].append(S["rate_rx"] + S["rate_tx"])
                for k in ("hist_cpu", "hist_mem", "hist_net"):
                    if len(S[k]) > HIST_MAX:
                        del S[k][:-HIST_MAX]

            def poll_resources():
                a = (S["app"] or {}).get("attributes", {}) or {}
                ident = a.get("identifier")
                if not ident:
                    return
                res, err = client_get(f"/api/client/servers/{ident}/resources")
                if res:
                    S["res"] = res
                    S["errors"].pop("live resources", None)
                    sample_resources()
                else:
                    S["errors"]["live resources"] = err

            def load_all(stdscr, initial=False):
                errs = {}
                loading(stdscr, 0)
                app, err = app_get(f"/api/application/servers/{server_id}", {"include": APP_INCLUDE})
                if app is None:
                    return err
                S["app"] = app
                ident = app.get("attributes", {}).get("identifier")

                loading(stdscr, 1)
                cli, e = client_get(f"/api/client/servers/{ident}")
                S["cli"] = cli
                if e:
                    errs["client details"] = e

                loading(stdscr, 2)
                res, e = client_get(f"/api/client/servers/{ident}/resources")
                S["res"] = res
                if e:
                    errs["live resources"] = e

                loading(stdscr, 3)
                bk, e = client_get(f"/api/client/servers/{ident}/backups")
                S["backups"] = bk
                if e:
                    errs["backups"] = e
                sc, e = client_get(f"/api/client/servers/{ident}/schedules")
                S["schedules"] = sc
                if e:
                    errs["schedules"] = e
                db, e = client_get(f"/api/client/servers/{ident}/databases")
                S["dbs"] = db
                if e:
                    errs["databases"] = e

                loading(stdscr, 4)
                S["subusers"] = {}
                try:
                    subs = app["attributes"]["relationships"]["subusers"]["data"]
                except Exception:
                    subs = []
                for su in subs:
                    uid = (su.get("attributes") or {}).get("user_id")
                    if uid is None:
                        continue
                    loading(stdscr, 4, f"user #{uid}")
                    u, e = app_get(f"/api/application/users/{uid}")
                    if u:
                        S["subusers"][uid] = u.get("attributes", {})
                    else:
                        errs[f"user {uid}"] = e

                loading(stdscr, 5)
                S["errors"] = errs
                S["fetched"] = time.time()
                if S["res"]:
                    sample_resources()
                return None

            # ---------------- panel content builders ----------------
            def A():
                return (S["app"] or {}).get("attributes", {}) or {}

            def REL(key, listy=False):
                try:
                    node = A()["relationships"][key]
                    return (node["data"] if listy else node["attributes"]) or ([] if listy else {})
                except Exception:
                    return [] if listy else {}

            def CLI():
                return (S["cli"] or {}).get("attributes", {}) or {}

            def CLI_META():
                return (S["cli"] or {}).get("meta", {}) or {}

            def RES():
                return ((S["res"] or {}).get("attributes", {}) or {}).get("resources", {}) or {}

            def RES_ATTR():
                return (S["res"] or {}).get("attributes", {}) or {}

            # a "row" is (kind, label, value, attr)
            #   kind "kv"   -> label: value, single line, truncated
            #   kind "wrap" -> label then wrapped value on following lines
            #   kind "text" -> raw single line
            #   kind "gap"  -> blank line
            def rows_to_lines(rows, inner):
                out = []
                for kind, label, value, attr in rows:
                    if kind == "gap":
                        out.append([(0, "", DIM)])
                    elif kind == "text":
                        out.append([(0, fit(value, inner), attr or VAL)])
                    elif kind == "wrap":
                        if label:
                            out.append([(0, f"{label}:", LBL)])
                            for ln in wrap(value, inner - 2):
                                out.append([(2, ln, attr or VAL)])
                        else:
                            for ln in wrap(value, inner):
                                out.append([(0, ln, attr or VAL)])
                    else:
                        prefix = f"{label}: " if label else ""
                        avail = inner - len(prefix)
                        if avail < 4:
                            out.append([(0, fit(f"{prefix}{value}", inner), attr or VAL)])
                        else:
                            out.append([(0, prefix, LBL),
                                        (len(prefix), fit(value, avail), attr or VAL)])
                return out

            def page_overview():
                a = A()
                user = REL("user")
                node = REL("node")
                egg = REL("egg")
                nest = REL("nest")
                loc = REL("location")
                allocs = REL("allocations", True)
                lim = a.get("limits", {}) or {}
                feat = a.get("feature_limits", {}) or {}
                cont = a.get("container", {}) or {}
                cli = CLI()

                P = []

                r = [("kv", "Name", a.get("name"), None),
                     ("kv", "Server ID", a.get("id"), None),
                     ("kv", "Identifier", a.get("identifier"), None)]
                if cli.get("internal_id") is not None:
                    r.append(("kv", "Internal ID", cli.get("internal_id"), None))
                if cli.get("server_identifier"):
                    r.append(("kv", "Long ID", cli.get("server_identifier"), DIM))
                r += [("kv", "UUID", a.get("uuid"), DIM),
                      ("kv", "External ID", a.get("external_id"), None),
                      ("wrap", "Description", a.get("description") or "(none)", None),
                      ("kv", "Created", pdate(a.get("created_at")), None),
                      ("kv", "Updated", pdate(a.get("updated_at")), None)]
                P.append(("Identity", r, C["cyan"]))

                v, at = yn(a.get("suspended"), good=False)
                r = [("kv", "Suspended", v, at)]
                v, at = yn(bool(cont.get("installed")))
                r.append(("kv", "Installed", v, at))
                if cli:
                    v, at = yn(cli.get("is_installing"), good=False)
                    r.append(("kv", "Installing", v, at))
                    v, at = yn(cli.get("is_transferring"), good=False)
                    r.append(("kv", "Transferring", v, at))
                    v, at = yn(cli.get("is_node_under_maintenance"), good=False)
                    r.append(("kv", "Node maintenance", v, at))
                state = RES_ATTR().get("current_state")
                if state:
                    r.append(("kv", "Power state", state.upper(),
                              OK if state == "running" else (WARN if state in ("starting", "stopping") else BAD)))
                r.append(("kv", "Panel status", a.get("status") or "normal", None))
                P.append(("State", r, C["cyan"]))

                r = []
                for al in allocs:
                    aa = al.get("attributes", {}) or {}
                    ip = aa.get("alias") or aa.get("ip")
                    primary = aa.get("id") == a.get("allocation")
                    r.append(("kv", "Primary" if primary else "Alt",
                              f"{ip}:{aa.get('port')}", OK if primary else VAL))
                if not r:
                    r.append(("text", "", "No allocations assigned", DIM))
                sftp = cli.get("sftp_details") or {}
                if sftp:
                    r.append(("kv", "SFTP", f"{sftp.get('ip')}:{sftp.get('port')}", None))
                r += [("kv", "Node", node.get("name"), None),
                      ("kv", "Node FQDN", node.get("fqdn"), None),
                      ("kv", "Location", f"{loc.get('short','?')} - {loc.get('long','?')}", None)]
                P.append(("Connection", r, C["cyan"]))

                r = [("kv", "Egg", egg.get("name"), None),
                     ("kv", "Nest", nest.get("name"), None),
                     ("kv", "Docker image", cont.get("image"), None),
                     ("kv", "Memory", human_mb(lim.get("memory")), None),
                     ("kv", "Disk", human_mb(lim.get("disk")), None),
                     ("kv", "CPU", f"{lim.get('cpu')}%" if lim.get("cpu") else "Unlimited", None),
                     ("kv", "Swap", "Unlimited" if (lim.get("swap") or 0) < 0 else human_mb(lim.get("swap")), None),
                     ("kv", "Slots", f"{feat.get('databases',0)} db / "
                                     f"{feat.get('allocations',0)} alloc / "
                                     f"{feat.get('backups',0)} backup", None)]
                P.append(("At a glance", r, C["cyan"]))

                r = [("kv", "Username", user.get("username"), None),
                     ("kv", "Email", user.get("email"), None),
                     ("kv", "Full name", f"{user.get('first_name','')} {user.get('last_name','')}".strip(), None),
                     ("kv", "User ID", user.get("id"), None)]
                v, at = yn(user.get("root_admin"), good=False)
                r.append(("kv", "Root admin", v, at))
                v, at = yn(user.get("2fa"))
                r.append(("kv", "2FA", v, at))
                r.append(("kv", "Registered", pdate(user.get("created_at")), None))
                P.append(("Owner", r, C["cyan"]))

                inv = cli.get("invocation") or cont.get("startup_command")
                r = [("wrap", "", inv, DIM)]
                P.append(("Startup command", r, C["cyan"]))

                return P

            def page_access():
                user = REL("user")
                subs = REL("subusers", True)
                meta = CLI_META()
                P = []

                r = [("kv", "Username", user.get("username"), None),
                     ("kv", "Email", user.get("email"), None),
                     ("kv", "First name", user.get("first_name"), None),
                     ("kv", "Last name", user.get("last_name"), None),
                     ("kv", "User ID", user.get("id"), None),
                     ("kv", "UUID", user.get("uuid"), DIM),
                     ("kv", "External ID", user.get("external_id"), None),
                     ("kv", "Language", user.get("language"), None)]
                v, at = yn(user.get("root_admin"), good=False)
                r.append(("kv", "Root admin", v, at))
                v, at = yn(user.get("2fa"))
                r.append(("kv", "2FA", v, at))
                r += [("kv", "Registered", pdate(user.get("created_at")), None),
                      ("kv", "Updated", pdate(user.get("updated_at")), None)]
                P.append(("Server owner", r, C["cyan"]))

                if subs:
                    for su in subs:
                        sa = su.get("attributes", {}) or {}
                        uid = sa.get("user_id")
                        info = S["subusers"].get(uid, {})
                        perms = sa.get("permissions", []) or []
                        r = [("kv", "Email", info.get("email"), None),
                             ("kv", "Full name",
                              f"{info.get('first_name','')} {info.get('last_name','')}".strip() or "-", None),
                             ("kv", "User ID", uid, None),
                             ("kv", "UUID", info.get("uuid"), DIM),
                             ("kv", "Subuser ID", sa.get("id"), None)]
                        v, at = yn(info.get("2fa"))
                        r.append(("kv", "2FA", v, at))
                        r += [("kv", "Language", info.get("language"), None),
                              ("kv", "Added", pdate(sa.get("created_at")), None),
                              ("kv", "Permissions", f"{len(perms)} granted", None)]
                        groups = {}
                        for p in perms:
                            g = p.split(".")[0]
                            groups[g] = groups.get(g, 0) + 1
                        if groups:
                            r.append(("wrap", "By group",
                                      "  ".join(f"{g}:{c}" for g, c in sorted(groups.items())), DIM))
                            r.append(("wrap", "Full list", ", ".join(perms), DIM))
                        title = info.get("username") or f"user #{uid}"
                        P.append((f"Subuser {DOT} {title}", r, C["blue"]))
                else:
                    P.append(("Subusers", [("text", "", "No subusers on this server", DIM)], C["blue"]))

                up = meta.get("user_permissions") or []
                if up:
                    P.append(("Your API key permissions",
                              [("wrap", "", ", ".join(up), DIM)], C["cyan"]))
                return P

            def page_config():
                a = A()
                egg = REL("egg")
                nest = REL("nest")
                vars_ = REL("variables", True)
                cont = a.get("container", {}) or {}
                env = cont.get("environment", {}) or {}
                cli = CLI()
                cfg = egg.get("config", {}) or {}
                script = egg.get("script", {}) or {}
                P = []

                r = [("kv", "Name", egg.get("name"), None),
                     ("kv", "Egg ID", egg.get("id"), None),
                     ("kv", "UUID", egg.get("uuid"), DIM),
                     ("kv", "Author", egg.get("author"), None),
                     ("wrap", "Description", egg.get("description"), None),
                     ("kv", "Default image", egg.get("docker_image"), None),
                     ("wrap", "Default startup", egg.get("startup"), DIM),
                     ("kv", "Created", pdate(egg.get("created_at")), None),
                     ("kv", "Updated", pdate(egg.get("updated_at")), None)]
                P.append(("Egg", r, C["cyan"]))

                imgs = egg.get("docker_images", {}) or {}
                r = []
                for k, v in imgs.items():
                    mark = " *" if v == cont.get("image") else ""
                    r.append(("kv", k, v + mark, OK if v == cont.get("image") else None))
                if not r:
                    r.append(("text", "", "No alternate images", DIM))
                P.append(("Available images", r, C["cyan"]))

                r = [("kv", "Stop command", cfg.get("stop"), None),
                     ("kv", "Startup done", (cfg.get("startup") or {}).get("done"), None),
                     ("kv", "Config extends", cfg.get("extends"), None)]
                files = (cfg.get("files") or {})
                for fname, fdata in files.items():
                    r.append(("kv", "File", f"{fname} ({(fdata or {}).get('parser')})", None))
                    for fk, fv in ((fdata or {}).get("find") or {}).items():
                        r.append(("kv", f"  {fk}", fv, DIM))
                denylist = cfg.get("file_denylist") or []
                r.append(("kv", "Denylist", ", ".join(denylist) if denylist else "(empty)", DIM))
                logs = cfg.get("logs")
                r.append(("kv", "Logs", json.dumps(logs) if logs else "(empty)", DIM))
                P.append(("Egg config", r, C["cyan"]))

                inst = script.get("install") or ""
                v, at = yn(script.get("privileged"), good=False)
                r = [("kv", "Entry", script.get("entry"), None),
                     ("kv", "Container", script.get("container"), None),
                     ("kv", "Privileged", v, at),
                     ("kv", "Extends", script.get("extends"), None),
                     ("kv", "Install script", f"{len(inst.splitlines())} lines, "
                                              f"{len(inst)} chars (press R for raw)", DIM)]
                P.append(("Install script", r, C["cyan"]))

                r = [("kv", "Name", nest.get("name"), None),
                     ("kv", "Nest ID", nest.get("id"), None),
                     ("kv", "UUID", nest.get("uuid"), DIM),
                     ("kv", "Author", nest.get("author"), None),
                     ("wrap", "Description", nest.get("description"), None),
                     ("kv", "Private", "Yes" if nest.get("private") else "No", None),
                     ("kv", "Created", pdate(nest.get("created_at")), None),
                     ("kv", "Updated", pdate(nest.get("updated_at")), None)]
                P.append(("Nest", r, C["cyan"]))

                if vars_:
                    for v_ in vars_:
                        va = v_.get("attributes", {}) or {}
                        val = va.get("server_value")
                        r = [("kv", "Value", val if val not in (None, "") else "(empty)",
                              VAL if val not in (None, "") else DIM),
                             ("kv", "Default", va.get("default_value") or "(empty)", DIM),
                             ("kv", "Env var", va.get("env_variable"), None),
                             ("kv", "Rules", va.get("rules"), DIM),
                             ("kv", "Viewable", "Yes" if va.get("user_viewable") else "No", None),
                             ("kv", "Editable", "Yes" if va.get("user_editable") else "No", None),
                             ("wrap", "Notes", va.get("description"), DIM)]
                        P.append((f"Var {DOT} {va.get('name', va.get('env_variable','?'))}", r, C["cyan"]))
                else:
                    P.append(("Variables", [("text", "", "No variables", DIM)], C["cyan"]))

                r = []
                for k, v_ in env.items():
                    r.append(("kv", k, v_ if v_ != "" else "(empty)", VAL if v_ != "" else DIM))
                if not r:
                    r.append(("text", "", "No environment", DIM))
                P.append(("Container environment", r, C["cyan"]))

                feats = cli.get("egg_features") or []
                if feats:
                    P.append(("Egg features",
                              [("wrap", "", ", ".join(feats), None)], C["cyan"]))
                return P

            def page_infra():
                a = A()
                node = REL("node")
                loc = REL("location")
                allocs = REL("allocations", True)
                dbs_app = REL("databases", True)
                feat = a.get("feature_limits", {}) or {}
                P = []

                r = [("kv", "Name", node.get("name"), None),
                     ("kv", "Node ID", node.get("id"), None),
                     ("kv", "UUID", node.get("uuid"), DIM),
                     ("wrap", "Description", node.get("description") or "(none)", None),
                     ("kv", "FQDN", node.get("fqdn"), None),
                     ("kv", "Scheme", node.get("scheme"), None)]
                v, at = yn(node.get("public"))
                r.append(("kv", "Public", v, at))
                v, at = yn(node.get("behind_proxy"))
                r.append(("kv", "Behind proxy", v, at))
                v, at = yn(node.get("maintenance_mode"), good=False)
                r.append(("kv", "Maintenance", v, at))
                v, at = yn(node.get("deployable"))
                r.append(("kv", "Deployable", v, at))
                r += [("kv", "Deploy fee", node.get("deploy_fee"), None),
                      ("kv", "Alert", node.get("alert") or "(none)", None),
                      ("kv", "Location ID", node.get("location_id"), None),
                      ("kv", "Created", pdate(node.get("created_at")), None),
                      ("kv", "Updated", pdate(node.get("updated_at")), None)]
                P.append(("Node", r, C["cyan"]))

                ar = node.get("allocated_resources", {}) or {}
                nm, nd = node.get("memory") or 0, node.get("disk") or 0
                am, ad = ar.get("memory") or 0, ar.get("disk") or 0
                r = [("kv", "Memory total", f"{nm} MB", None),
                     ("kv", "Memory allocated", f"{am} MB" + (f" ({am/nm*100:.2f}%)" if nm else ""),
                      OK if (nm and am / nm < 0.85) else WARN),
                     ("kv", "Memory overalloc", f"{node.get('memory_overallocate')}%", None),
                     ("kv", "Disk total", f"{nd} MB", None),
                     ("kv", "Disk allocated", f"{ad} MB" + (f" ({ad/nd*100:.2f}%)" if nd else ""),
                      OK if (nd and ad / nd < 0.85) else WARN),
                     ("kv", "Disk overalloc", f"{node.get('disk_overallocate')}%", None),
                     ("kv", "Upload limit", f"{node.get('upload_size')} MB", None)]
                P.append(("Node capacity", r, C["cyan"]))

                r = [("kv", "Daemon port", node.get("daemon_listen"), None),
                     ("kv", "SFTP port", node.get("daemon_sftp"), None),
                     ("kv", "Daemon base", node.get("daemon_base"), DIM),
                     ("kv", "Daemon text", node.get("daemon_text"), DIM),
                     ("kv", "Container text", node.get("container_text"), DIM)]
                P.append(("Daemon", r, C["cyan"]))

                r = [("kv", "Short", loc.get("short"), None),
                     ("kv", "Long", loc.get("long"), None),
                     ("kv", "Location ID", loc.get("id"), None),
                     ("kv", "Created", pdate(loc.get("created_at")), None),
                     ("kv", "Updated", pdate(loc.get("updated_at")), None)]
                P.append(("Location", r, C["cyan"]))

                r = []
                for al in allocs:
                    aa = al.get("attributes", {}) or {}
                    ip = aa.get("alias") or aa.get("ip")
                    primary = aa.get("id") == a.get("allocation")
                    r.append(("kv", f"#{aa.get('id')}",
                              f"{ip}:{aa.get('port')}" + (" [primary]" if primary else ""),
                              OK if primary else VAL))
                    if aa.get("ip") and aa.get("alias"):
                        r.append(("kv", "  raw ip", aa.get("ip"), DIM))
                    if aa.get("notes"):
                        r.append(("kv", "  notes", aa.get("notes"), DIM))
                    r.append(("kv", "  assigned", "Yes" if aa.get("assigned") else "No", DIM))
                if not r:
                    r.append(("text", "", "No allocations", DIM))
                P.append(("Allocations", r, C["cyan"]))

                r = []
                cdb = (S["dbs"] or {}).get("data") or []
                for d in cdb:
                    da = d.get("attributes", {}) or {}
                    r.append(("kv", da.get("name", "db"), f"{da.get('host',{}).get('address','?')}"
                                                          f":{da.get('host',{}).get('port','?')}", None))
                    r.append(("kv", "  username", da.get("username"), DIM))
                if not r and dbs_app:
                    for d in dbs_app:
                        da = d.get("attributes", {}) or {}
                        r.append(("kv", "database", da.get("database"), None))
                if not r:
                    note = S["errors"].get("databases")
                    r.append(("text", "", note if note else f"None (slots: {feat.get('databases',0)})", DIM))
                P.append(("Databases", r, C["cyan"]))

                r = []
                for b in ((S["backups"] or {}).get("data") or []):
                    ba = b.get("attributes", {}) or {}
                    r.append(("kv", ba.get("name", "backup"), human_bytes(ba.get("bytes")), None))
                    r.append(("kv", "  created", pdate(ba.get("created_at")), DIM))
                    r.append(("kv", "  completed", "Yes" if ba.get("is_successful") else "No", DIM))
                if not r:
                    note = S["errors"].get("backups")
                    r.append(("text", "", note if note else f"None (slots: {feat.get('backups',0)})", DIM))
                P.append(("Backups", r, C["cyan"]))

                r = []
                for s_ in ((S["schedules"] or {}).get("data") or []):
                    sa = s_.get("attributes", {}) or {}
                    cron = sa.get("cron", {}) or {}
                    r.append(("kv", sa.get("name", "schedule"),
                              "active" if sa.get("is_active") else "inactive",
                              OK if sa.get("is_active") else DIM))
                    r.append(("kv", "  cron", " ".join(str(cron.get(k, "*")) for k in
                              ("minute", "hour", "day_of_month", "month", "day_of_week")), DIM))
                    r.append(("kv", "  next run", pdate(sa.get("next_run_at")), DIM))
                if not r:
                    note = S["errors"].get("schedules")
                    r.append(("text", "", note if note else "No schedules", DIM))
                P.append(("Schedules", r, C["cyan"]))

                if S["errors"]:
                    r = [("wrap", k, v, WARN) for k, v in S["errors"].items()]
                    P.append(("Diagnostics", r, C["yellow"]))
                return P

            # ---------------- generic paged panel renderer ----------------
            def render_packed(pad, panels, cols, avail_w):
                ncols = max(1, min(3, avail_w // 46))
                cw = avail_w // ncols
                inner = cw - 4
                sized = []
                for title, rows, color in panels:
                    lines = rows_to_lines(rows, inner)
                    sized.append((title, lines, color, len(lines) + 2))
                heights = [0] * ncols
                buckets = [[] for _ in range(ncols)]
                for item in sized:
                    t = heights.index(min(heights))
                    buckets[t].append(item)
                    heights[t] += item[3]
                for ci, bucket in enumerate(buckets):
                    y = 0
                    x = ci * cw
                    w = cw - 1 if ci < ncols - 1 else avail_w - x
                    for title, lines, color, h in bucket:
                        draw_box(pad, y, x, w, h, title, color)
                        for li, segs in enumerate(lines):
                            for off, text, attr in segs:
                                if text:
                                    put(pad, y + 1 + li, x + 2 + off,
                                        fit(text, max(w - 4 - off, 0)), attr)
                        y += h
                return max(heights) if heights else 1

            # ---------------- resources page (custom layout) ----------------
            def render_resources(pad, cols, avail_w, body_h):
                a = A()
                lim = a.get("limits", {}) or {}
                rr = RES()
                ra = RES_ATTR()
                node = REL("node")

                y = 0
                if not rr:
                    h = 7
                    draw_box(pad, 0, 0, avail_w, h, "Live resource usage unavailable", C["yellow"])
                    why = S["errors"].get("live resources") or S["errors"].get("client details") or "no data"
                    put(pad, 1, 2, fit(f"Reason: {why}", avail_w - 4), WARN)
                    put(pad, 2, 2, fit("Endpoint: GET /api/client/servers/{identifier}/resources",
                                       avail_w - 4), DIM)
                    put(pad, 3, 2, fit("This needs a CLIENT key (ptlc_) in .env as admin_api_key,",
                                       avail_w - 4), DIM)
                    put(pad, 4, 2, fit("belonging to an account that owns or is a subuser on this server",
                                       avail_w - 4), DIM)
                    put(pad, 5, 2, fit("(root admin accounts can reach any server).", avail_w - 4), DIM)
                    return h

                # ---- gauges ----
                gh = 8
                draw_box(pad, y, 0, avail_w, gh, "Utilisation", C["cyan"],
                         "live" if S["live"] else "static")
                bw = max(min(avail_w - 46, 60), 10)
                cpu_lim = lim.get("cpu") or 0
                cpu_abs = rr.get("cpu_absolute") or 0
                cpu_pct = (cpu_abs / cpu_lim * 100.0) if cpu_lim else float(cpu_abs)
                mem_b = rr.get("memory_bytes") or 0
                mem_lim = (lim.get("memory") or 0) * 1024 * 1024
                mem_pct = (mem_b / mem_lim * 100.0) if mem_lim else 0.0
                dsk_b = rr.get("disk_bytes") or 0
                dsk_lim = (lim.get("disk") or 0) * 1024 * 1024
                dsk_pct = (dsk_b / dsk_lim * 100.0) if dsk_lim else 0.0

                gauges = [
                    ("CPU ", cpu_pct, f"{cpu_abs:.2f}% of {cpu_lim or '∞'}%" if UNI
                     else f"{cpu_abs:.2f}% of {cpu_lim or 'inf'}%"),
                    ("MEM ", mem_pct, f"{human_bytes(mem_b)} / {human_mb(lim.get('memory'))}"),
                    ("DISK", dsk_pct, f"{human_bytes(dsk_b)} / {human_mb(lim.get('disk'))}"),
                ]
                for i, (name, pct, detail) in enumerate(gauges):
                    g, at, pv = bar(pct, bw)
                    put(pad, y + 2 + i * 2, 2, name, LBL)
                    put(pad, y + 2 + i * 2, 7, g, at)
                    put(pad, y + 2 + i * 2, 8 + bw, f"{pv:6.2f}%", at)
                    put(pad, y + 2 + i * 2, 16 + bw, fit(detail, max(avail_w - 18 - bw, 0)), DIM)
                y += gh

                # ---- runtime + network side by side ----
                half = avail_w // 2
                rt = [("kv", "State", (ra.get("current_state") or "unknown").upper(), None),
                      ("kv", "Uptime", human_uptime(rr.get("uptime")), None),
                      ("kv", "Suspended", "Yes" if ra.get("is_suspended") else "No",
                       BAD if ra.get("is_suspended") else OK),
                      ("kv", "Samples held", f"{len(S['hist_cpu'])}", DIM),
                      ("kv", "Live polling", "ON (2s)" if S["live"] else "OFF - press L",
                       OK if S["live"] else DIM)]
                nl = [("kv", "Net RX total", human_bytes(rr.get("network_rx_bytes")), None),
                      ("kv", "Net TX total", human_bytes(rr.get("network_tx_bytes")), None),
                      ("kv", "RX rate", human_bytes(S["rate_rx"]) + "/s", None),
                      ("kv", "TX rate", human_bytes(S["rate_tx"]) + "/s", None),
                      ("kv", "Combined", human_bytes(S["rate_rx"] + S["rate_tx"]) + "/s", DIM)]
                rt_lines = rows_to_lines(rt, half - 5)
                nl_lines = rows_to_lines(nl, avail_w - half - 4)
                bh = max(len(rt_lines), len(nl_lines)) + 2
                draw_box(pad, y, 0, half - 1, bh, "Runtime", C["cyan"])
                for li, segs in enumerate(rt_lines):
                    for off, text, attr in segs:
                        put(pad, y + 1 + li, 2 + off, fit(text, max(half - 5 - off, 0)), attr)
                draw_box(pad, y, half, avail_w - half, bh, "Network", C["cyan"])
                for li, segs in enumerate(nl_lines):
                    for off, text, attr in segs:
                        put(pad, y + 1 + li, half + 2 + off,
                            fit(text, max(avail_w - half - 4 - off, 0)), attr)
                y += bh

                # ---- node capacity, placed before graphs so graphs can
                # ---- absorb every remaining row without overflowing
                ar = node.get("allocated_resources", {}) or {}
                nm, nd = node.get("memory") or 0, node.get("disk") or 0
                am, ad = ar.get("memory") or 0, ar.get("disk") or 0
                nrows = [("kv", "Node memory", f"{am} / {nm} MB" + (f"  ({am/nm*100:.2f}%)" if nm else ""), None),
                         ("kv", "Node disk", f"{ad} / {nd} MB" + (f"  ({ad/nd*100:.2f}%)" if nd else ""), None),
                         ("kv", "Overallocate", f"mem {node.get('memory_overallocate')}% / "
                                                f"disk {node.get('disk_overallocate')}%", DIM)]
                nlines = rows_to_lines(nrows, avail_w - 4)
                nh = len(nlines) + 2
                draw_box(pad, y, 0, avail_w, nh, f"Node capacity ({node.get('name','?')})", C["cyan"])
                for li, segs in enumerate(nlines):
                    for off, text, attr in segs:
                        put(pad, y + 1 + li, 2 + off, fit(text, max(avail_w - 4 - off, 0)), attr)
                y += nh

                # ---- history graphs, sized to whatever height is left ----
                left = body_h - y
                graphs = [("CPU %", S["hist_cpu"], 100.0, C["green"]),
                          ("Memory %", S["hist_mem"], 100.0, C["cyan"]),
                          ("Network B/s", S["hist_net"], None, C["magenta"])]
                per = max(left // 3, 4)
                for gname, series, gmax, gcolor in graphs:
                    gw = avail_w
                    gh2 = per
                    peak = max(series) if series else 0
                    if gmax is None:
                        sub = f"peak {human_bytes(peak)}/s"
                        scale = max(peak, 1.0)
                    else:
                        sub = f"peak {peak:.1f}%"
                        scale = gmax
                    draw_box(pad, y, 0, gw, gh2, gname, gcolor, sub)
                    if len(series) < 2:
                        put(pad, y + gh2 // 2, 4,
                            fit("collecting samples - press L for live polling, or U to refresh",
                                gw - 8), DIM)
                    else:
                        draw_graph(pad, y + 1, 2, gw - 4, gh2 - 2, series, scale,
                                   gcolor | curses.A_BOLD)
                    y += gh2

                return y

            # ---------------- chrome ----------------
            def paint_header(head, cols):
                head.erase()
                a = A()
                ra = RES_ATTR()
                state = ra.get("current_state")
                if a.get("suspended"):
                    st, sat = "SUSPENDED", BAD
                elif state == "running":
                    st, sat = "RUNNING", OK
                elif state in ("starting", "stopping"):
                    st, sat = state.upper(), WARN
                elif state == "offline":
                    st, sat = "OFFLINE", BAD
                else:
                    st, sat = "NO LIVE STATE", DIM

                draw_box(head, 0, 0, cols, HEAD_H, None, ACC)
                name = fit(a.get("name", "?"), max(cols - 40, 10))
                put(head, 0, 2, f" WINGSPAN {DOT} {name} ", ACC)
                tag = f" [{st}] "
                put(head, 0, max(cols - len(tag) - 3, 2), tag, sat)

                x = 2
                for i, pname in enumerate(PAGES):
                    label = f" {i+1} {pname} "
                    if x + len(label) + 4 > cols:
                        break
                    if i == S["page"]:
                        put(head, 1, x, label, curses.A_REVERSE | ACC)
                    else:
                        put(head, 1, x, label, DIM)
                    x += len(label) + 1
                put(head, 1, 1, ARR_L, DIM)
                put(head, 1, min(x, cols - 2), ARR_R, DIM)

                paint_status(head, cols)

            def paint_status(head, cols):
                ts = datetime.datetime.fromtimestamp(S["fetched"]).strftime("%H:%M:%S") if S["fetched"] else "--:--:--"
                age = int(time.time() - S["fetched"]) if S["fetched"] else 0
                left = f" updated {ts} ({age}s) "
                if S["live"]:
                    left += f"{DOT} LIVE "
                try:
                    head.hline(HEAD_H - 1, 2, curses.ACS_HLINE, max(cols - 4, 1), ACC)
                except curses.error:
                    pass
                put(head, HEAD_H - 1, 3, fit(left, max(cols - 8, 1)),
                    OK if S["live"] else DIM)
                if S["flash"] and time.time() < S["flash_until"]:
                    msg = f" {S['flash']} "
                    x = max(cols - len(msg) - 3, len(left) + 5)
                    put(head, HEAD_H - 1, x, fit(msg, max(cols - x - 2, 1)), WARN)

            def paint_footer(foot, cols, more_up, more_down):
                foot.erase()
                keys = (f"{ARR_L}{ARR_R}/1-5 page   Up/Dn scroll   U refresh   "
                        f"L live   R raw   Enter new   Q quit")
                put(foot, 0, 1, fit(keys, max(cols - 20, 1)), DIM)
                ind = ""
                if more_up:
                    ind += f"{MORE_U} "
                if more_down:
                    ind += f"{MORE_D} more"
                if ind:
                    put(foot, 0, max(cols - len(ind) - 2, 1), ind, WARN)

            # ---------------- frame assembly ----------------
            def build_page(rows, cols):
                body_h = max(rows - HEAD_H - FOOT_H, 3)
                avail_w = max(cols - 2, 20)
                pad = curses.newpad(max(body_h * 4, 200), max(cols, 20))
                pad.erase()
                p = S["page"]
                try:
                    if p == 0:
                        used = render_packed(pad, page_overview(), cols, avail_w)
                    elif p == 1:
                        used = render_resources(pad, cols, avail_w, body_h)
                    elif p == 2:
                        used = render_packed(pad, page_access(), cols, avail_w)
                    elif p == 3:
                        used = render_packed(pad, page_config(), cols, avail_w)
                    else:
                        used = render_packed(pad, page_infra(), cols, avail_w)
                except Exception as e:
                    logging.error(f"server_info render page {p}: {e}")
                    pad.erase()
                    put(pad, 1, 2, fit(f"Failed rendering this page: {e}", avail_w), BAD)
                    used = 3
                return pad, max(used, 1), body_h

            def repaint(stdscr, full=True):
                rows, cols = stdscr.getmaxyx()
                if rows < 14 or cols < 52:
                    stdscr.erase()
                    put(stdscr, 0, 0, "Terminal too small.", BAD)
                    put(stdscr, 1, 0, f"Need 52x14, have {cols}x{rows}.", DIM)
                    put(stdscr, 2, 0, "Resize, or press Q.", DIM)
                    stdscr.refresh()
                    return None, None, None, 0, 0
                head = curses.newwin(HEAD_H, cols, 0, 0)
                foot = curses.newwin(FOOT_H, cols, rows - FOOT_H, 0)
                pad, used, body_h = build_page(rows, cols)
                maxscroll = max(used - body_h, 0)
                S["scroll"][S["page"]] = min(S["scroll"][S["page"]], maxscroll)
                sc = S["scroll"][S["page"]]
                paint_header(head, cols)
                paint_footer(foot, cols, sc > 0, sc < maxscroll)
                stdscr.erase()
                stdscr.noutrefresh()
                head.noutrefresh()
                try:
                    pad.noutrefresh(sc, 0, HEAD_H, 1, HEAD_H + body_h - 1, cols - 2)
                except curses.error:
                    pass
                foot.noutrefresh()
                curses.doupdate()
                return head, foot, pad, used, body_h

            # ---------------- boot ----------------
            err = load_all(stdscr, initial=True)
            if err:
                return ("error", err)

            head, foot, pad, used, body_h = repaint(stdscr)
            stdscr.timeout(500)

            while True:
                try:
                    ch = stdscr.getch()
                    rows, cols = stdscr.getmaxyx()

                    if ch == -1:
                        did = False
                        if S["live"] and time.time() - S["last_poll"] >= LIVE_INTERVAL:
                            S["last_poll"] = time.time()
                            poll_resources()
                            S["fetched"] = time.time()
                            if S["page"] == 1:
                                head, foot, pad, used, body_h = repaint(stdscr)
                                did = True
                        if not did and head is not None:
                            paint_status(head, cols)
                            head.noutrefresh()
                            curses.doupdate()
                        continue

                    if ch in (ord("q"), ord("Q")):
                        return ("quit", None)
                    if ch in (10, 13, curses.KEY_ENTER):
                        return ("again", None)
                    if ch in (ord("r"), ord("R")):
                        return ("raw", {"application": S["app"], "client": S["cli"],
                                        "resources": S["res"], "backups": S["backups"],
                                        "schedules": S["schedules"], "databases": S["dbs"],
                                        "subusers": S["subusers"], "errors": S["errors"]})

                    if ch in (ord("u"), ord("U")):
                        now = time.time()
                        wait = COOLDOWN - (now - S["last_try"])
                        if wait > 0:
                            S["flash"] = f"cooldown {int(wait)+1}s"
                            S["flash_until"] = now + 2
                            if head is not None:
                                paint_status(head, cols)
                                head.noutrefresh()
                                curses.doupdate()
                            continue
                        S["last_try"] = now
                        e = load_all(stdscr)
                        if e:
                            S["flash"] = f"refresh failed: {e}"
                            S["flash_until"] = time.time() + 4
                        else:
                            S["flash"] = "refreshed"
                            S["flash_until"] = time.time() + 2
                        head, foot, pad, used, body_h = repaint(stdscr)
                        continue

                    if ch in (ord("l"), ord("L")):
                        S["live"] = not S["live"]
                        S["flash"] = "live polling ON (every 2s)" if S["live"] else "live polling OFF"
                        S["flash_until"] = time.time() + 2
                        S["last_poll"] = 0.0
                        head, foot, pad, used, body_h = repaint(stdscr)
                        continue

                    newpage = None
                    if ch == curses.KEY_RIGHT:
                        newpage = (S["page"] + 1) % len(PAGES)
                    elif ch == curses.KEY_LEFT:
                        newpage = (S["page"] - 1) % len(PAGES)
                    elif ch in (ord("]"),):
                        newpage = (S["page"] + 1) % len(PAGES)
                    elif ch in (ord("["),):
                        newpage = (S["page"] - 1) % len(PAGES)
                    elif ord("1") <= ch <= ord("5"):
                        newpage = ch - ord("1")

                    if newpage is not None:
                        S["page"] = newpage
                        head, foot, pad, used, body_h = repaint(stdscr)
                        continue

                    if ch == curses.KEY_RESIZE:
                        head, foot, pad, used, body_h = repaint(stdscr)
                        continue

                    if pad is None:
                        continue

                    maxscroll = max(used - body_h, 0)
                    cur = S["scroll"][S["page"]]
                    moved = False
                    if ch in (curses.KEY_DOWN, ord("j")):
                        cur = min(cur + 1, maxscroll); moved = True
                    elif ch in (curses.KEY_UP, ord("k")):
                        cur = max(cur - 1, 0); moved = True
                    elif ch == curses.KEY_NPAGE:
                        cur = min(cur + body_h, maxscroll); moved = True
                    elif ch == curses.KEY_PPAGE:
                        cur = max(cur - body_h, 0); moved = True
                    elif ch == curses.KEY_HOME or ch == ord("g"):
                        cur = 0; moved = True
                    elif ch == curses.KEY_END or ch == ord("G"):
                        cur = maxscroll; moved = True

                    if moved:
                        S["scroll"][S["page"]] = cur
                        paint_footer(foot, cols, cur > 0, cur < maxscroll)
                        try:
                            pad.noutrefresh(cur, 0, HEAD_H, 1, HEAD_H + body_h - 1, cols - 2)
                        except curses.error:
                            pass
                        foot.noutrefresh()
                        curses.doupdate()

                except Exception as e:
                    logging.error(f"server_info loop: {e}")
                    time.sleep(0.4)

        try:
            action, payload = curses.wrapper(dashboard)
        except Exception as e:
            logging.error(f"server_info curses: {e}")
            print(f"{Fore.RED}Dashboard crashed: {e}")
            time.sleep(2)
            continue

        if action == "quit":
            return
        elif payload == "HTTP 404":
            print(f"{Fore.RED}Server not found: {server_id}")
            time.sleep(2)
        elif action == "error":
            print(f"{Fore.RED}Could not load server {server_id}: {payload}")
            time.sleep(2)
        elif action == "raw":
            try:
                print(json.dumps(payload, indent=2, default=str))
            except Exception:
                print(payload)
            input("Press Enter to continue...")

        banner()
        print(f"Enter the numerical {Fore.GREEN}Server ID{Fore.RESET} to get all related information. Enter {Fore.GREEN}'h'{Fore.RESET} to return to homepage")

def purge_srv():
    pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}Thats a thing for the next ship/update!"],border_bold=True,color="cyan")
    time.sleep(5)
def purge_users():
    pt.panel(size=70,center=False,title=f"/search-and-info/inputs", content=[f"{Fore.MAGENTA}{Style.BRIGHT}Thats a thing for the next ship/update!"],border_bold=True,color="cyan")
    time.sleep(5)

def server_filter(server_list:dict,header):
    
    if not header:
        header=list(server_list["data"][0]["attributes"].keys())
    
    server_data=[]
    for i in range(server_list["meta"]["pagination"]["count"]):

        server_data.append(server_list["data"][i]["attributes"])


    server_final=[]
    for i in server_data:
        server_row=[]
        for h in header:
            server_row.append(i.get(h))
        server_final.append(server_row)

    return(server_final)



# ---------------------------------------------------------------------------
# ARGUMENT PARSING / CLI ENTRY
# ---------------------------------------------------------------------------

def build_parser():
    """Build the argparse structure with shared filters and subcommands.
    THIS FUNCTION IS AI BUILT"""
    
    # Top-level parser
    parser = argparse.ArgumentParser(prog="wingspan", description="Wingspan CLI management tool")
    subparsers = parser.add_subparsers(dest="command", required=False, help="Subcommands")

    # 1. Setup Subcommand (Stand-alone, no filters needed)
    setup_parser = subparsers.add_parser("setup", help="Run the configuration setup wizard")
    setup_parser.add_argument("--setup", action="store_true", required=False, help="Trigger setup sequence")

    # 2. Shared Parent Parser for Common Filter Flags
    filter_parent = argparse.ArgumentParser(add_help=False)
    filter_parent.add_argument("--node", help="Filter by node name")
    filter_parent.add_argument("--status", help="Filter by status (e.g., running, stopped)")
    filter_parent.add_argument("--name", help="Filter by server name (regex/substring)")
    filter_parent.add_argument("--min-ram", type=int, help="Minimum RAM in MB")
    filter_parent.add_argument("--max-ram", type=int, help="Maximum RAM in MB")
    filter_parent.add_argument("--owner", help="Filter by owner ID or username")

    # 3. Shared Parent Parser for Global Execution Modifiers
    execution_parent = argparse.ArgumentParser(add_help=False)
    execution_parent.add_argument("--dry-run", action="store_true", help="Simulate actions without applying changes")
    execution_parent.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompts")

    # 4. List Subcommand
    list_parser = subparsers.add_parser("list", parents=[filter_parent], help="List and filter servers")
    list_parser.add_argument("--output", choices=["table", "csv", "json"], default="table", help="Output format")

    # 5. Resize Subcommand
    resize_parser = subparsers.add_parser("resize", parents=[filter_parent, execution_parent], help="Bulk resize servers")
    resize_parser.add_argument("--ram", type=int, required=True, help="Target RAM in MB")
    resize_parser.add_argument("--cpu", type=int, required=True, help="Target CPU cores")
    resize_parser.add_argument("--disk", type=int, required=True, help="Target Disk space in GB")

    # 6. Power Subcommand
    power_parser = subparsers.add_parser("power", parents=[filter_parent, execution_parent], help="Bulk power management")
    power_parser.add_argument("--action", choices=["start", "stop", "restart", "kill"], required=True, help="Power action to execute")

    # 7. Suspend Subcommand
    suspend_parser = subparsers.add_parser("suspend", parents=[filter_parent, execution_parent], help="Bulk suspend servers")
    suspend_parser.add_argument("--undo", action="store_true", help="Unsuspend/resume the target servers")

    # 8. Purge Subcommand
    purge_parser = subparsers.add_parser("purge", parents=[filter_parent, execution_parent], help="Bulk purge/delete servers")
    purge_parser.add_argument("--manifest", help="Path to manifest FILE for validation tracking")

    # 9. Reinstall Subcommand
    subparsers.add_parser("reinstall", parents=[filter_parent, execution_parent], help="Bulk reinstall OS/environments")

    return parser




def main():
    """Main execution block mapping arguments to backend functionality."""
    
    parser = build_parser()
    args = parser.parse_args()
    
    
    if args.command is None:
        print("Booting in Interactive mode..")
        power_on_self_test()
#        load_config()
        init_logger()
        
        home_page()
        
    else:    
       # Route immediate commands bypassing infrastructure setup
        if args.command == "setup":
            setup_wizard()
            return
        power_on_self_test()
        # Initialize environment
#        load_config()
        init_logger()

        # Gather data context
        servers = get_servers()
        filtered_servers = filter_servers(servers, args)

        # Dispatch commands
        if args.command == "list":
#            if args.output == "csv":
            export_csv(filtered_servers, "export.csv")
#            else:


        elif args.command == "resize":
            bulk_resize(filtered_servers, args.ram, args.cpu, args.disk, args.dry_run, args.yes)

        elif args.command == "power":
            bulk_power(filtered_servers, args.action, args.dry_run, args.yes)

        elif args.command == "suspend":
            bulk_suspend(filtered_servers, args.undo, args.dry_run, args.yes)

        elif args.command == "purge":
            bulk_purge(filtered_servers, args.manifest, args.dry_run, args.yes)

        elif args.command == "reinstall":
            bulk_reinstall(filtered_servers, args.dry_run, args.yes)


if __name__ == "__main__":
    main()
    
while True:
    pass