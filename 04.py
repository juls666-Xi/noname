import psutil
import socket
import time
from collections import defaultdict
import threading
from scapy.all import sniff, IP, TCP, Raw

# ---------- PROCESS CONNECTION MONITOR ----------
def get_process_by_port(local_port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == local_port and conn.status == 'ESTABLISHED':
            try:
                return psutil.Process(conn.pid)
            except:
                return None
    return None

def list_active_connections():
    print("[*] Active TCP connections with process info:")
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED':
            try:
                proc = psutil.Process(conn.pid)
                name = proc.name()
                pid = conn.pid
            except:
                name = "unknown"
                pid = conn.pid if conn.pid else -1
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "local"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "remote"
            print(f"  PID {pid} [{name}] : {laddr} -> {raddr}")

# ---------- URL SNIFFER (HTTP requests) ----------
captured_urls = set()
sniffing = False
sniff_thread = None

def packet_handler(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        ip_layer = packet[IP]
        tcp_layer = packet[TCP]
        payload = bytes(packet[Raw].load)
        # Check for HTTP GET/POST requests
        try:
            # Decode as ASCII (HTTP headers)
            text = payload.decode('ascii', errors='ignore')
            lines = text.split('\r\n')
            if lines and ('GET' in lines[0] or 'POST' in lines[0] or 'Host:' in text):
                # Extract request line
                request_line = lines[0]
                host_line = None
                for line in lines:
                    if line.lower().startswith('host:'):
                        host_line = line.split(':', 1)[1].strip()
                        break
                if host_line:
                    url = f"http://{host_line}{request_line.split(' ')[1]}"
                else:
                    url = request_line.split(' ')[1] if ' ' in request_line else request_line
                if url not in captured_urls:
                    captured_urls.add(url)
                    print(f"[URL] {ip_layer.src}:{tcp_layer.sport} -> {url}")
        except:
            pass

def start_sniffing(interface=None):
    global sniffing, sniff_thread
    sniffing = True
    # Filter HTTP traffic (port 80)
    bpf_filter = "tcp port 80"
    sniff_thread = threading.Thread(target=lambda: sniff(iface=interface, filter=bpf_filter, prn=packet_handler, store=False))
    sniff_thread.daemon = True
    sniff_thread.start()
    print("[*] HTTP sniffer started")

def stop_sniffing():
    global sniffing
    sniffing = False
    # scapy sniff has no built-in stop; thread will be daemon, exit on main exit.

# ---------- MAIN ----------
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--sniff':
        # Requires admin/root privileges
        try:
            start_sniffing()
        except PermissionError:
            print("[!] Run as administrator/root for packet sniffing")
            sys.exit(1)
    # Monitor connections every 5 seconds
    try:
        while True:
            list_active_connections()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[*] Stopping")