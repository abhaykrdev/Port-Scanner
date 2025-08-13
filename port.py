import socket
import os
import sys
import argparse
from datetime import datetime
from colorama import init, Fore, Style
from threading import Thread, Lock

open_ports = []
lock = Lock()

def clear_screen():
  pass


def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def scan_port(remote_server_ip, port, verbose, banner):
    print(f"Checking port {port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((remote_server_ip, port))
        if result == 0:
            with lock:
                open_ports.append(port)
            msg = Fore.GREEN + f"Port {port}: Open"
            if banner:
                try:
                    sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
                    data = sock.recv(1024)
                    msg += Fore.YELLOW + f" | Banner: {data.decode(errors='ignore').strip()}"
                except Exception:
                    msg += Fore.YELLOW + " | Banner: N/A"
            print(msg + Style.RESET_ALL)
        elif verbose:
            print(Fore.RED + f"Port {port}: Closed" + Style.RESET_ALL)
        sock.close()
    except Exception:
        pass

def scan_ports(remote_server_ip, verbose, start_port, end_port, threads, banner):
    print('-' * 60)
    print(f"Starting the scan of the machine {remote_server_ip}")
    print(f"Scanning ports {start_port} to {end_port} using {threads} threads")
    print('-' * 60)

    start_time = datetime.now()
    thread_list = []

    for port in range(start_port, end_port + 1):
        t = Thread(target=scan_port, args=(remote_server_ip, port, verbose, banner))
        thread_list.append(t)
        t.start()
        if len(thread_list) >= threads:
            for thr in thread_list:
                thr.join()
            thread_list = []

    # Wait for remaining threads
    for thr in thread_list:
        thr.join()

    end_time = datetime.now()
    total_time = end_time - start_time

    print('-' * 60)
    print(f"Scan completed in: {total_time}")
    print(f"Open ports: {sorted(open_ports) if open_ports else 'None found'}")
    print('-' * 60)

def main():
    parser = argparse.ArgumentParser(description="An enhanced port scanner.")
    parser.add_argument("ip", nargs='?', help="The IP address of the server to scan.")
    parser.add_argument("-v", "--verbose", help="Show closed ports.", action="store_true")
    parser.add_argument("-sp", "--start-port", type=int, default=1, help="Start of port range (default: 1)")
    parser.add_argument("-ep", "--end-port", type=int, default=1024, help="End of port range (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-b", "--banner", help="Try to grab service banners.", action="store_true")
    args = parser.parse_args()

    clear_screen()

    if not args.ip:
        args.ip = input("Enter the IP address of the server to scan: ")

    if not is_valid_ip(args.ip):
        print("Invalid IP address.")
        sys.exit(1)

    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        print("Invalid port range.")
        sys.exit(1)

    init(autoreset=True)
    scan_ports(args.ip, args.verbose, args.start_port, args.end_port, args.threads, args.banner)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit()