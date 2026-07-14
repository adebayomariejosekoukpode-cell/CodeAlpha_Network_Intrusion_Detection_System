# CodeAlpha_Network_Intrusion_Detection_System

CodeAlpha_NetworkIDS/
├── suricata/
│   ├── suricata.yaml      ← configuration principale
│   └── rules/
│       └── local.rules    ← nos règles personnalisées
├── scripts/
│   ├── parser.py          ← lit eve.json et analyse
│   ├── blocker.py         ← bloque les IPs via iptables
│   └── alerter.py         ← envoie emails d'alerte
├── dashboard/
│   ├── app.py             ← serveur web Flask
│   ├── templates/
│   │   └── index.html     ← interface web
│   └── static/
│       └── style.css      ← styles
├── requirements.txt
└── README.md