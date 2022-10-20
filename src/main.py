import os
import subprocess
import sys
from datetime import datetime, date
from termcolor import colored
import platform
# You will get an error if you're on Windows when importing apt (advanced package tool)
import apt

device_os = platform.platform().lower()


def check_tools():
    """
    This function is very important as it checks if all the necessary tools are
    installed on the machine.
    """
    print(colored("\n[..] Checking os support and tools installation..", "red"))
    if device_os == "linux":
        cache = apt.Cache()
        cache.open()
        status_nmap = cache["nmap"].is_installed
        status_gobuster = cache["gobuster"].is_installed
        status_nikto = cache["nikto"].is_installed

        if not status_nmap:
            print(colored("[🚫] Nmap not installed", "red"))
            print(colored("[..] Installing Nmap", "yellow"))
            subprocess.check_output("sudo apt install nmap -y", shell=True, stderr=subprocess.STDOUT)
            print(colored("[✅] Nmap installed\n", "green"))

        if not status_gobuster:
            print(colored("[🚫] Gobuster not installed", "red"))
            print(colored("[..] Installing Gobuster", "yellow"))
            subprocess.check_output("sudo apt install gobuster -y", shell=True, stderr=subprocess.STDOUT)
            print(colored("[✅] Gobuster installed\n", "green"))

        if not status_nikto:
            print(colored("[🚫] Nikto not installed", "red"))
            print(colored("[..] Installing Nikto", "yellow"))
            subprocess.check_output("sudo apt install nikto -y", shell=True, stderr=subprocess.STDOUT)
            print(colored("[✅] Nikto installed\n", "green"))
            print(colored("[✅] Success! Every requirement is installed!\n", "green"))

    elif device_os == "windows":
        print(colored("[🚫] Windows is not yet supported! Please use a machine with a Linux Kernel.", "red"))
        exit(0)

    else:
        print(colored("[🚫] Your operating system is not supported! Please use a machine with a Linux Kernel.", "red"))
        exit(0)


def log_output(data, tool, text):
    """
    This function will log the output of the ran tools
    """
    # Get the current working directory and output directory
    root_dir = os.getcwd()
    if root_dir.endswith("src"):
        root_dir = root_dir.replace("/src", "")
    out_dir = root_dir + "/out"

    # Check if the output directory exists
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    datetime_now = str(datetime.now()).strip().replace(" ", "_").replace(":", "-").replace("-", "_")
    
    # Get the output file
    out_file = f"{out_dir}/{tool}_{datetime_now}.log"

    # Open the output file
    with open(out_file, "w") as f:
        f.write(f"Date: {date.today()}\n\nTool: {tool}\n\n{text}:\n{data}")

    return out_file


def get_open_ports(target):
    """
    This function will scan the open ports of a target host
    """
    # This is the command that will be executed
    command = "sudo nmap -sCVT " + target

    # Execute the command
    output = subprocess.check_output(command, shell=True)

    open_ports = []

    # Get the open ports
    for line in output.decode("utf-8").splitlines():
        if "open" in line:
            open_ports.append(int(line.split("/")[0]))

    return open_ports


def scan_directories(target):
    """
    This function will scan the directories of a target host
    """
    # This is the command that will be executed
    command = f"sudo gobuster -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"

    # Execute the command and get the output
    output = subprocess.check_output(command, shell=True)

    # Get the directories
    directories = []
    for line in output.decode("utf-8").splitlines():
        if line.startswith("/"):
            directories.append(line.split(" ")[0])

    return directories


def nikto_scan(target):
    command = f"nikto -h {target}"
    output = subprocess.check_output(command, shell=True).decode()
    return output


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'
    print(box)


def print_logo():
    root_dir = os.getcwd()
    if root_dir.endswith("src"):
        root_dir = root_dir.replace("src", "")
    logo_txt = open(f"{root_dir}/assets/logo.txt", "r").read()
    print(colored(logo_txt + "\n", "green"))
    print_msg_box("\n  Author: Sami Hindi\n  Version: 1.0.0\n  GitHub: https://github.com/FujiwaraChoki\n  License: MIT\n")


def main():
    # Print the logo
    print_logo()

    # Check for the tools (if they're all installed) => nmap, gobuster and nikto
    check_tools()

    # Get the target host
    target = str(sys.argv).split("--host")[1].replace(" ", "").replace(",", "").replace("]", "").replace("[", "").replace("'", "")

    # Scan the open ports
    print(colored("\n[*] Scanning the open ports of the target host..", "green"))
    open_ports = get_open_ports(target)
    log_output(open_ports, "nmap", "Open ports")
    print(colored(f"[+] Open ports: {open_ports}\n", "green"))

    # Scan the directories
    print(colored("[*] Scanning the directories of the target host..", "green"))
    directories = scan_directories(target)
    log_output(directories, "gobuster", "Existing directories")
    print(colored(f"[+] Existing directories: {directories}\n", "green"))

    # Scanning with Nikto
    print(colored("[*] Scanning the target host with Nikto..", "green"))
    nikto = nikto_scan(target)
    file_name = log_output(nikto, "nikto", "Nikto output")
    print(colored(f"[+] Nikto log: {file_name}", "green"))

    print(colored("\nMade possible by the anonymous donors 😎", "yellow"))


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print(colored("[⭕] Please specify the target host with --host", "red"))
    except KeyboardInterrupt:
        print(colored("\n[⭕] Exiting..", "red"))
    except Exception as error:
        print(colored(f"[⭕] Error: {error}", "red"))
