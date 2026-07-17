import sys
import os
import threading
from flask import Flask, jsonify, render_template

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

import ids_parser
from blocker import get_blocked_ips, block_ip

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/alerts")
def get_alerts():
    alerts = ids_parser.alerts_history
    return jsonify({
        "alerts": alerts,
        "total": len(alerts),
        "blocked_ips": get_blocked_ips(),
        "total_blocked": len(get_blocked_ips())
    })

@app.route("/api/block/<ip>", methods=["POST"])
def block_ip_manually(ip):
    success = block_ip(ip)
    return jsonify({
        "success": success,
        "ip": ip,
        "message": f"IP {ip} bloquée avec succès" if success else f"IP {ip} déjà bloquée"
    })

@app.route("/api/unblock/<ip>", methods=["POST"])
def unblock_ip_manually(ip):
    from blocker import unblock_ip
    success = unblock_ip(ip)
    return jsonify({
        "success": success,
        "ip": ip,
        "message": f"IP {ip} débloquée avec succès" if success else f"IP {ip} non trouvée"
    })

if __name__ == "__main__":
    parser_thread = threading.Thread(target=ids_parser.follow_eve_log, daemon=True)
    parser_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=False)