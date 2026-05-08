from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyokenDirect"

TARGET_KEYWORDS = [
    "世田谷", 
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

    # JavaScriptの描画待ち
    page.wait_for_timeout(5000)

    text = page.locator("body").inner_text()

    print("========== PAGE TEXT START ==========")
    print(text[:5000])
    print("========== PAGE TEXT END ==========")

    browser.close()

matched = [x for x in TARGET_KEYWORDS if x in text]

if matched:
    body = "空室候補を検知:\n\n"
    body += "\n".join(matched)
    body += f"\n\n{URL}"

    send_mail(body)

    print("通知送信")
else:
    print("該当なし")
