import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SLACK_WEBHOOK = "SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

PC_URL = "https://search.naver.com/search.naver?query="
MO_URL = "https://m.search.naver.com/search.naver?query="

# 키워드 파일 읽기
def load_keywords():
    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]
    return keywords

def send_slack(msg):
    if SLACK_WEBHOOK:
        requests.post(SLACK_WEBHOOK, json={"text": msg})

def check_brand(keyword, url, device):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 모바일 user-agent 적용
    if device == "MO":
        options.add_argument(
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )

    driver = webdriver.Chrome(options=options)
    driver.get(url + keyword)
    time.sleep(2)

    try:
        driver.find_element(By.CSS_SELECTOR, "._cs_brand")
        print(f"[OK] {keyword} / {device} 브랜드검색 있음")
    except:
        print(f"[NO] {keyword} / {device} 브랜드검색 없음")
        send_slack(f"❗브랜드검색 미노출: {keyword} ({device})")

    driver.quit()

if __name__ == "__main__":
    keywords = load_keywords()   # ← keywords.txt 내용 불러오기
    for kw in keywords:
        check_brand(kw, PC_URL, "PC")
        check_brand(kw, MO_URL, "MO")

