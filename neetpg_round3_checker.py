import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
import re

# ---------------- CONFIG ----------------
URL = "https://mcc.nic.in/current-events-pg/"
STATE_FILE = "neetpg_round3_seen.txt"

EMAIL_FROM = ""
EMAIL_TO = [
    "",
    ""
]

EMAIL_PASSWORD = ""
# ---------------------------------------

KEYWORDS = ["final result", "round 3", "pg counselling"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)


def main():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.find_all("tr")

    found_links = []

    for row in rows:
        text = row.get_text(" ", strip=True).lower()
        if all(k in text for k in KEYWORDS):
            link = row.find("a", href=True)
            if link:
                found_links.append(link["href"])

    if not found_links:
        print("No Round 3 final result yet")
        return

    seen = set()
    if os.path.exists(STATE_FILE):
        seen = set(open(STATE_FILE).read().splitlines())

    new_links = [l for l in found_links if l not in seen]

    if new_links:
        body = (
            "🚨 NEET PG ROUND 3 FINAL RESULT IS OUT!\n\n"
            f"Time: {datetime.now()}\n\n"
            "Links:\n" + "\n".join(new_links)
        )
        send_email("🚨 NEET PG Round 3 Final Result घोषित!", body)

        with open(STATE_FILE, "a") as f:
            for l in new_links:
                f.write(l + "\n")

        print("EMAIL SENT")
    else:
        print("Already notified earlier")

if __name__ == "__main__":
    main()

