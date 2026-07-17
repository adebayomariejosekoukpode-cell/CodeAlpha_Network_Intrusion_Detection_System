# CodeAlpha — Network Intrusion Detection System

> **Linux only** — This project requires Linux for iptables-based 
> IP blocking. Windows is not supported.

A network-based intrusion detection system (IDS) built with Suricata and Python, featuring real-time alert monitoring, automatic IP blocking via iptables, email notifications, and a web dashboard.

---

## Features

- Real-time network traffic monitoring with Suricata
- 5 custom detection rules (ICMP, Nmap, SSH, HTTP, DNS)
- Automatic IP blocking via iptables
- Email alerts via Gmail SMTP
- Live web dashboard (Flask)
- Manual Block / Unblock from the dashboard
- Clean shutdown with automatic IP unblocking

---

## Project Structure

```
CodeAlpha_Network_Intrusion_Detection_System/
├── suricata/
│   ├── suricata.yaml           # Suricata reference configuration
│   └── rules/
│       └── local.rules         # Custom detection rules
├── scripts/
│   ├── ids_parser.py           # eve.json parser + response logic
│   ├── blocker.py              # IP blocking via iptables
│   ├── alerter.py              # Email alerts via Gmail
│   └── email_config.example.py # Email configuration template
├── dashboard/
│   ├── app.py                  # Flask web server
│   ├── templates/
│   │   └── index.html          # Dashboard UI
│   └── static/
│       └── style.css           # Dashboard styles
├── logs/                       # Auto-generated log files
├── requirements.txt
└── README.md
```

---

## Detection Rules

| Rule ID | Threat               | Detection Logic               |
|---------|----------------------|-------------------------------|
| 1001    | ICMP Ping Sweep      | 5+ pings in 10 seconds        |
| 1002    | Nmap Port Scan       | 20+ SYN packets in 5 seconds  |
| 1003    | SSH Brute Force      | 5+ SSH attempts in 60 seconds |
| 1004    | HTTP Path Traversal  | `/etc/passwd` in HTTP URI     |
| 1005    | Suspicious DNS Query | DNS queries to `.tk` domains  |

---

## Requirements

- Linux (Kali / Ubuntu / Debian)
- Python 3.10+
- Suricata 7+
- Flask
- Root privileges (for packet capture and iptables)

---

## Installation & Usage

### 1. Install Suricata

```bash
sudo apt update
sudo apt install suricata -y
suricata --version
```

Expected output:
```
This is Suricata version 8.x.x RELEASE
```

---

### 2. Clone the repository

```bash
git clone https://github.com/your-username/CodeAlpha_Network_Intrusion_Detection_System.git
cd CodeAlpha_Network_Intrusion_Detection_System
```

---

### 3. Configure Suricata

#### 3.1 — Find your network interface
```bash
ip a
```

Look for an interface that is **UP** and has an IP address assigned. Common names:
- `wlan0` → WiFi interface
- `eth0` → Ethernet interface

#### 3.2 — Open Suricata configuration file
The main Suricata configuration file is located at `/etc/suricata/suricata.yaml`.

```bash
sudo nano /etc/suricata/suricata.yaml
```

> **Nano tip:** Use `Ctrl+W` to search for a specific section in the file.
> Type the keyword and press `Enter` to jump to it directly.
> Press `Ctrl+W` again to find the next occurrence.

#### 3.3 — Set your network interface
Still in `/etc/suricata/suricata.yaml`, search with `Ctrl+W`: type `af-packet` and press `Enter`.

Find:
```yaml
af-packet:
  - interface: eth0
```

Replace `eth0` with your interface (e.g. `wlan0`):
```yaml
af-packet:
  - interface: wlan0
```

#### 3.4 — Verify eve-log output
Still in `/etc/suricata/suricata.yaml`, search with `Ctrl+W`: type `eve-log` and press `Enter`.

Make sure this block is present and enabled:
```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
```

#### 3.5 — Copy custom rules
Exit nano first (`Ctrl+X`), then copy the rules file from the project to Suricata's rules directory:

```bash
sudo cp suricata/rules/local.rules /var/lib/suricata/rules/local.rules
```

#### 3.6 — Set rule files
Reopen `/etc/suricata/suricata.yaml`:

```bash
sudo nano /etc/suricata/suricata.yaml
```

Search with `Ctrl+W`: type `rule-files` and press `Enter`.

Replace the existing content with:
```yaml
rule-files:
  - /var/lib/suricata/rules/local.rules
```

#### 3.7 — Save and exit nano
```
Ctrl+X  →  Y  →  Enter
```

#### 3.8 — Verify Suricata configuration
```bash
sudo suricata -T -c /etc/suricata/suricata.yaml
```

Expected output:
```
This is Suricata version 8.x.x RELEASE running in SYSTEM mode
Configuration provided was successfully loaded. Exiting.
```

> If you see `No rule files match the pattern`, make sure step 3.5 and 3.6 were done correctly.

---

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure email alerts

#### 5.1 — Generate a Google App Password

A Google App Password is a 16-character password that allows external apps to connect to your Gmail account securely via SMTP. It is **different from your regular Gmail password**.

Follow these steps:

```
1. Go to: myaccount.google.com
2. Click on "Security" in the left menu
3. Under "How you sign in to Google", enable "2-Step Verification" if not already active
4. Go back to "Security" and scroll down to "App passwords" or search "App passwords" in research bar
5. In the "App name" field, type: NetworkIDS
6. Click "Create"
7. Copy the generated 16-character password (shown only once — save it!)
```

> The App Password is shown **only once**. Copy it before closing the window.

#### 5.2 — Create your configuration file

```bash
cp scripts/email_config.example.py scripts/email_config.py
nano scripts/email_config.py
```

Fill in your credentials:
```python
EMAIL_CONFIG = {
    "sender": "your_email@gmail.com",
    "password": "xxxxxxxxxxxxxxxx",  # 16-char App Password (no spaces)
    "receiver": "your_email@gmail.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
}
```

> You can use the same address for `sender` and `receiver` to send alerts to yourself.

---

### 6. Launch Suricata

Open a **Terminal 1** and run:

```bash
sudo suricata -c /etc/suricata/suricata.yaml -i wlan0
```

Expected output:
```
This is Suricata version 8.x.x RELEASE running in SYSTEM mode
...
(packet capture starts silently)
```

> Suricata is now monitoring all traffic on your interface.

---

### 7. Launch the dashboard

Open a **Terminal 2** and run:

```bash
sudo python3 dashboard/app.py
```

Expected output:
```
[PARSER] Surveillance de /var/log/suricata/eve.json ...
[PARSER] En attente de nouvelles lignes...
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```

Open your browser at:
```
http://localhost:5000
```

---

### 8. Test the detection rules

Open a **Terminal 3** and generate suspicious traffic:

```bash
# Test Rule 1001 — ICMP Ping Sweep
ping -c 10 <target_ip>

# Test Rule 1002 — Nmap Port Scan
sudo nmap -sS <target_ip>
```

Expected results:
- Dashboard updates automatically with new alerts
- Suspicious IP is automatically blocked via iptables
- Email alert received in your Gmail inbox

---

### 9. Stop the system

Press `Ctrl+C` in Terminal 2 to stop the dashboard.

Expected output:
```
[PARSER] Nettoyage des règles iptables...
[PARSER] Toutes les IPs débloquées.
```

> All blocked IPs are automatically unblocked on shutdown.
> iptables rules are also cleared automatically on system reboot.

---

## Dashboard

The web dashboard provides:

| Feature           | Description                                  |
|-------------------|----------------------------------------------|
| Total Alerts      | Number of intrusions detected                |
| Blocked IPs       | Number of automatically blocked IPs          |
| Last Alert        | Timestamp of the most recent alert           |
| Live Alerts Table | Real-time alert feed (auto-refresh every 5s) |
| Block button      | Manually block a suspicious IP               |
| Unblock button    | Remove an IP from the blocklist              |

---

## Email Alerts

When an intrusion is detected, an HTML email is automatically sent containing:
- Timestamp
- Signature (attack type)
- Source IP
- Destination IP
- Protocol
- Severity level

---

## 📱 Remote Access

The dashboard is accessible from any device connected to the same network.

On your phone or another computer, open a browser and go to:

http://<your-kali-ip>:5000

To find your Kali IP :
```bash
ip a | grep "inet " | grep wlan0
```

Example: if your Kali IP is `192.168.1.XX`, open `http://192.168.1.XX:5000` on your phone.

---

## Response Mechanisms

| Mechanism     | Tool       | Trigger                            |
|---------------|------------|------------------------------------| 
| IP Blocking   | iptables   | Automatic on detection             |
| Email Alert   | Gmail SMTP | Automatic on detection             |
| Manual Block  | Dashboard  | Manual via UI                      |
| Clean Unblock | iptables   | Ctrl+C or dashboard Unblock button |

> iptables rules are **volatile** — they are cleared on system reboot.

---
 
## Legal Notice

This tool is intended for **educational and authorized testing purposes only**. Only use it on networks you own or have explicit permission to monitor. Unauthorized network monitoring is illegal.

---

## Author

**Marie-José** — Cybersecurity Intern @ CodeAlpha
IFRI — Université d'Abomey-Calavi, Benin