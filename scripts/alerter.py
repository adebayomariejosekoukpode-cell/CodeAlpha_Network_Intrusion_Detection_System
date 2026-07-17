import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logging.basicConfig(
    filename="logs/alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

from email_config import EMAIL_CONFIG

def send_alert(alert_info):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[IDS ALERT] {alert_info['signature']} - {alert_info['src_ip']}"
        msg["From"] = EMAIL_CONFIG["sender"]
        msg["To"] = EMAIL_CONFIG["receiver"]

        body_text = f"""

NETWORK INTRUSION DETECTED
==========================
Time      : {alert_info['timestamp']}
Signature : {alert_info['signature']}
Source IP : {alert_info['src_ip']}
Dest IP   : {alert_info['dest_ip']}
Protocol  : {alert_info['protocol']}
Severity  : {alert_info['severity']}
==========================
This alert was generated automatically by Network IDS.send_alert
        """
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; background:#0a0a1a; color:#e8eaf0; padding:20px;">
    <div style="border:2px solid #ff3333; border-radius:8px; padding:20px; max-width:600px;">
        <h2 style="color:#ff3333;">⚠️ Network Intrusion Detected</h2>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="padding:8px; color:#9ca3af;">Time</td>
                <td style="padding:8px; color:#00d4ff;">{alert_info['timestamp']}</td></tr>
            <tr><td style="padding:8px; color:#9ca3af;">Signature</td>
                <td style="padding:8px; color:#ff3333;"><b>{alert_info['signature']}</b></td></tr>
            <tr><td style="padding:8px; color:#9ca3af;">Source IP</td>
                <td style="padding:8px; color:#e8eaf0;">{alert_info['src_ip']}</td></tr>
            <tr><td style="padding:8px; color:#9ca3af;">Dest IP</td>
                <td style="padding:8px; color:#e8eaf0;">{alert_info['dest_ip']}</td></tr>
            <tr><td style="padding:8px; color:#9ca3af;">Protocol</td>
                <td style="padding:8px; color:#e8eaf0;">{alert_info['protocol']}</td></tr>
            <tr><td style="padding:8px; color:#9ca3af;">Severity</td>
                <td style="padding:8px; color:#f59e0b;">{alert_info['severity']}</td></tr>
        </table>
        <p style="color:#6b7280; font-size:12px; margin-top:20px;">
            This alert was generated automatically by NetworkIDS.
        </p>
    </div>
</body>
</html>
        """
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html,"html"))

        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            server.sendmail(EMAIL_CONFIG["sender"], EMAIL_CONFIG["receiver"], msg.as_string())

        logging.info(f"Email envoyé pour : {alert_info['signature']} depuis {alert_info['src_ip']}")
        print(f"[ALERTER] Email envoyé : {alert_info['signature']} depuis {alert_info['src_ip']}")
        return True
    
    except Exception as e:
        logging.error(f"Erreur envoi email : {e}")
        print(f"[ALERTER] Erreur envoi email : {e}")
        return False