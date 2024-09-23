import socket
import sys
import requests
import os
import curses

def get_http_status(url):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)

        host = url.replace("http://", "").replace("https://", "").split("/")[0]
        client_socket.connect((host, 80))

        request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = client_socket.recv(1024).decode()
        status_code = response.split(' ')[1]

        client_socket.close()
        return status_code
    except socket.timeout:
        return "Timeout"
    except Exception as e:
        return f"Error: {e}"

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "Error getting geolocation"
    except Exception as e:
        return f"Error: {e}"

def process_file(stdscr, file_path):
    stdscr.clear()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                http_status = get_http_status(url)
                stdscr.addstr(f"URL: {url}, HTTP Status: {http_status}\n")

                ip = socket.gethostbyname(url.replace("http://", "").replace("https://", "").split("/")[0])
                geolocation = get_geolocation(ip)
                stdscr.addstr(f"Geolocation of {ip}: {geolocation}\n\n")
        stdscr.addstr("Press any key to return to the main menu...")
        stdscr.refresh()
        stdscr.getch()
    except FileNotFoundError:
        stdscr.addstr("File not found.\n")
        stdscr.refresh()
        stdscr.getch()

def list_txt_files():
    return [f for f in os.listdir('.') if f.endswith('.txt')]

def file_selection_menu(stdscr):

    curses.curs_set(0)
    txt_files = list_txt_files()
    txt_files.append("Return to main menu")
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select a .txt file:")
        for idx, file in enumerate(txt_files):
            if idx == current_row:
                stdscr.addstr(idx + 1, 0, f"> {file}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, file)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(txt_files) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if txt_files[current_row] == "Return to main menu":
                break
            else:
                process_file(stdscr, txt_files[current_row])
                stdscr.clear()
                stdscr.refresh()
                break

def main_menu(stdscr):
    curses.curs_set(0)
    current_row = 0
    menu = ["Get URL data", "Exit"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Main Menu:")
        for idx, item in enumerate(menu):
            if idx == current_row:
                stdscr.addstr(idx + 1, 0, f"> {item}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, item)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row] == "Get URL data":
                file_selection_menu(stdscr)
            elif menu[current_row] == "Exit":
                break

if __name__ == "__main__":
    curses.wrapper(main_menu)
