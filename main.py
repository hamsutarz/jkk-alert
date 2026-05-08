from playwright.sync_api import sync_playwright

URL = "https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyokenDirect"

TARGET_KEYWORDS = [
    "検索",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)

    page.wait_for_timeout(5000)

    text = page.locator("body").inner_text()

    print("========== PAGE TEXT START ==========")
    print(text[:5000])
    print("========== PAGE TEXT END ==========")

    browser.close()

matched = [x for x in TARGET_KEYWORDS if x in text]

if matched:
    print("ヒットしました:", matched)
else:
    print("該当なし")
