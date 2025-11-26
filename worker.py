import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# ==========================
# 환경 변수
# ==========================
SLACK_WEBHOOK_URL = os.getenv("https://hooks.slack.com/services/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L")

NAVER_PC_URL = "https://search.naver.com/search.naver?query={}"
NAVER_MO_URL = "https://m.search.naver.com/search.naver?query={}"

HEADER_PC = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}
HEADER_MO = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36"
}

# ==========================
# 브랜드 검색 노출 여부 확인
# ==========================
def check_brand_search(keyword: str, device: str) -> bool:
    """브랜드검색이 있는지 brand_block/div id=brand_area 기반으로 판별"""

    if device == "PC":
        url = NAVER_PC_URL.format(keyword)
        header = HEADER_PC
    else:
        url = NAVER_MO_URL.format(keyword)
        header = HEADER_MO

    html = requests.get(url, headers=header).text
    soup = BeautifulSoup(html, "html.parser")

    # 브랜드검색 광고는 아래 요소가 반드시 포함됨
    exists = (
        soup.find("div", class_="brand_block") or
        soup.find("div", id="brand_area")
    )

    return True if exists else False


# ==========================
# Slack 메시지 전송
# ==========================
def send_slack(message: str):
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL is missing.")
        return

    requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message}
    )


# ==========================
# MAIN
# ==========================
def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords = [k.strip() for k in f.readlines() if k.strip()]

    pc_results = []
    mo_results = []

    for kw in keywords:
        pc_ok = check_brand_search(kw, "PC")
        mo_ok = check_brand_search(kw, "MO")

        pc_results.append(f"{kw} ({'☑️ 정상노출' if pc_ok else '❌ 미노출'})")
        mo_results.append(f"{kw} ({'☑️ 정상노출' if mo_ok else '❌ 미노출'})")

    # 최종 슬랙 메시지
    slack_message = (
        f"📢 *BGROW - Naver Brand Search Monitoring*\n"
        f"⏱ {now}\n\n"
        f"*[PC]*\n" + "\n".join(pc_results) +
        "\n\n*[MO]*\n" + "\n".join(mo_results)
    )

    print(slack_message)
    send_slack(slack_message)


if __name__ == "__main__":
    main()

