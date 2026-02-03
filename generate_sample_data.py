import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
np.random.seed(42)

OUTPUT_PATH = Path("data/itsm_tickets_sample_v1.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

start_date = datetime(2025, 11, 1)
days = 90
n = 850

categories = {
    "Network": ["VPN", "WiFi", "DNS"],
    "End User Computing": ["Endpoint Management", "Printers", "VDI"],
    "Collaboration": ["Email", "Teams/Zoom", "Calendar"],
    "Identity & Access": ["SSO", "MFA", "Password Reset"],
    "Business Apps": ["ERP", "HRIS", "CRM"],
    "Security": ["Phishing", "EDR Alerts", "Account Lockout"],
}

ci_map = {
    "VPN": ("VPN Service", "CI-VPN-GW-01"),
    "WiFi": ("Corporate WiFi", "CI-WIFI-CTRL-02"),
    "DNS": ("DNS Service", "CI-DNS-CORE-01"),
    "Endpoint Management": ("Endpoint Management", "CI-EPM-01"),
    "Printers": ("Print Services", "CI-PRINT-SRV-03"),
    "VDI": ("VDI Platform", "CI-VDI-POOL-01"),
    "Email": ("Email Service", "CI-MAIL-01"),
    "Teams/Zoom": ("Collaboration Suite", "CI-COLLAB-01"),
    "Calendar": ("Calendar Service", "CI-CAL-01"),
    "SSO": ("SSO Platform", "CI-SSO-01"),
    "MFA": ("MFA Platform", "CI-MFA-01"),
    "Password Reset": ("Password Services", "CI-PWD-01"),
    "ERP": ("ERP", "CI-ERP-01"),
    "HRIS": ("HRIS", "CI-HRIS-01"),
    "CRM": ("CRM", "CI-CRM-01"),
    "Phishing": ("Security Awareness", "CI-SEC-AWARE-01"),
    "EDR Alerts": ("EDR Platform", "CI-EDR-01"),
    "Account Lockout": ("SSO Platform", "CI-SSO-01"),
}

rows = []

for i in range(n):
    day_offset = random.randint(0, days - 1)
    opened_at = start_date + timedelta(days=day_offset, hours=random.randint(8, 18))

    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])
    service, ci = ci_map[subcategory]

    priority = random.choices(["P1", "P2", "P3", "P4"], weights=[5, 15, 60, 20])[0]
    mttr = random.randint(30, 240)

    resolved_at = opened_at + timedelta(minutes=mttr)

    rows.append({
        "ticket_id": f"INC{202600000 + i}",
        "opened_at": opened_at,
        "resolved_at": resolved_at,
        "category": category,
        "subcategory": subcategory,
        "service": service,
        "ci": ci,
        "priority": priority,
        "assignment_group": f"{category} Ops",
        "short_description": f"{subcategory} related issue reported by user",
        "mttr_minutes": mttr,
    })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_PATH, index=False)

print(f"CSV generated at: {OUTPUT_PATH.resolve()}")
print(f"Row count: {len(df)}")
