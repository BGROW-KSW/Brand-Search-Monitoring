import requests
import time

SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
SEARCH_PC = "https://search.naver.com/search.naver?query="
SEARCH_MO = "https://m.search.naver.com/search.naver?query="

PC_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

MO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/14.0 Mobile/15E148 Safari/604.1"
    )
}


def load_keywords():
    with open("keywords.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def send_slack(msg: str):
    try:
        requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=5)
    except Exception as e:
        print("[ERROR] Slack 알림 실패:", e)


def has_brand_block(html: str) -> bool:
    """
    네이버 브랜드검색 영역이 HTML에 존재하는지 판단.
    """
    keywords = [
        'data-dss-logarea="brand"',
        'class="_cs_brand"',
        "브랜드검색",  # 혹시 텍스트 기반 노출
    ]
    return any(k in html for k in keywords)


def check_keyword(keyword: str, device: str):
    """
    검색 요청 → HTML 확인 → 결과 반환(V/X)
    """
    if device == "PC":
        url = SEARCH_PC + keyword
        headers = PC_HEADERS
    else:
        url = SEARCH_MO + keyword
        headers = MO_HEADERS

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        html = resp.text
    except Exception as e:
        print(f"[ERROR] {keyword} / {device} 요청 실패:", e)
        return f"{keyword} (요청 실패 :x:)"

    if has_brand_block(html):
        return f"{keyword} (정상노출 :white_check_mark:)"
    else:
        return f"{keyword} (미노출 :x:)"


if __name__ == "__main__":
    keywords = load_keywords()

    pc_results = []
    mo_results = []

    # PC 체크
    for kw in keywords:
        pc_results.append(check_keyword(kw, "PC"))
        time.sleep(0.7)

    # 모바일 체크
    for kw in keywords:
        mo_results.append(check_keyword(kw, "MO"))
        time.sleep(0.7)

    # Slack 메시지 구성
    msg = "BGROW - Naver Brand Search Monitoring\n\n"
    msg += "[PC]\n" + "\n".join(pc_results) + "\n\n"
    msg += "[MO]\n" + "\n".join(mo_results)

    print(msg)  # Render 로그에서도 보기 위해 출력
    send_slack(msg)
