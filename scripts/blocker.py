import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    filename="logs/blocked_ip.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

blocked_ips = set()

def block_ip(ip):
    if ip in blocked_ips:
        return False  # IP is already blocked
    
    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True,
            capture_output=True
        )
        blocked_ips.add(ip)
        logging.info(f"Blocked IP: {ip}")
        print(f"[BLOCKER] {datetime.now().strftime('%H:%M:%S')} - IP bloquée : {ip}")
        return True
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur blocage {ip} : {e}")
        print(f"[BLOCKER] Erreur : imposssible de bloquer {ip}")
        return False
    

def unblock_ip(ip):
    if ip not in blocked_ips:
        return False  
    
    try:
        subprocess.run(
            ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
            check=True,
            capture_output=True
        )
        blocked_ips.discard(ip)
        logging.info(f"Unblocked IP: {ip}")
        print(f"[BLOCKER] {datetime.now().strftime('%H:%M:%S')} - IP débloquée : {ip}")
        return True
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur déblocage {ip} : {e}")
        return False

def get_blocked_ips():
    return list(blocked_ips)