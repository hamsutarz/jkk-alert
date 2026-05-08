from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://www.to-kousya.or.jp/chintai/reco/?op_support=ファミリーウィーク"

TARGET_KEYWORDS = [
    "八王子泉町",
]

def send_mail(body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "JKK空室通知"
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = os.environ["MAIL_TO"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            os.environ["MAIL_FROM"],
            os.environ["MAIL_APP_PASSWORD"]
        )
        server.send_message(msg)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)

    html = page.content()

    browser.close()

matched = [x for x in TARGET_KEYWORDS if x in html]

if matched:
    body = "空室候補を検知:\n\n"
    body += "\n".join(matched)
    body += f"\n\n{URL}"

    send_mail(body)

    print("通知送信")
else:
    print("該当なし")
