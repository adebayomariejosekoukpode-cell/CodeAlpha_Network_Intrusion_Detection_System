import json
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blocker import block_ip
from alerter import send_alert

EVE_LOG= "/var/log/suricata/eve.json"

SEVERITY_THRESHOLD = 4

MY_IP= "192.168.1.84"

processed_alerts = set()

alerts_history  = []

def extract_alert(line):
    try:
        data = json.loads(line)

        if data.get("event_type") != "alert":
            return None
        
        alert = data.get("alert", {})
        severity= alert.get("severity", 4)

        if severity > SEVERITY_THRESHOLD:
            return None
        
        return {
            "timestamp": data.get("timestamp", ""),
            "src_ip": data.get("src_ip", "Unknown"),
            "dest_ip": data.get("dest_ip", "Unknown"),
            "protocol": data.get("proto", "Unknown"),
            "signature": alert.get("signature", "Unknown"),
            "severity": severity,
            "sid": alert.get("signature_id", 0),
        }
    except json.JSONDecodeError:
        return None

import signal
import subprocess

def cleanup(signum, frame):
    print("\n[PARSER] Nettoyage des règles iptables...")
    from blocker import blocked_ips
    for ip in list(blocked_ips):
        subprocess.run(
            ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
            capture_output=True
        )
    print("[PARSER] Toutes les IPs débloquées.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def follow_eve_log():
    print(f"[PARSER] Surveillance de {EVE_LOG} ...")

    if not os.path.exists(EVE_LOG):
        print(f"[PARSER] Erreur : {EVE_LOG} introuvable. Suricata est-il lancé ?")
        return
    
    with open(EVE_LOG, "r") as f:
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                time.sleep(0.1)
                continue

            line= line.strip()
            if not line:
                continue

            alert = extract_alert(line)
            if alert is None:
                continue

            alert_id = f"{alert['sid']}_{alert['src_ip']}_{alert['timestamp']}"
            if alert_id in processed_alerts:
                continue

            processed_alerts.add(alert_id)
            alerts_history.append(alert)

            print(f"[PARSER] ALERTE : {alert['signature']} depuis {alert['src_ip']}")

            if alert["src_ip"] != MY_IP:
                block_ip(alert["src_ip"])
            send_alert(alert)

def get_alerts_history():
    return alerts_history 

if __name__ == "__main__":
    try:
        follow_eve_log()
    except KeyboardInterrupt:
        print("\n[PARSER] Arrêt du parser.")
    