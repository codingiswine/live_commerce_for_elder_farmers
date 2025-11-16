"""
네이버 쇼핑라이브 실시간 댓글 수집 스크립트
Selenium 4.x 최신 문법 사용
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
from pathlib import Path
from datetime import datetime


def setup_driver(driver_path=None):
    """
    Chrome WebDriver 설정

    Args:
        driver_path (str, optional): ChromeDriver 경로.
            None이면 시스템 PATH에서 자동 탐색 (brew install chromedriver 권장)
    """
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # driver_path가 지정되지 않으면 시스템 PATH 사용
    if driver_path is None:
        try:
            # PATH에서 chromedriver 자동 탐색
            return webdriver.Chrome(options=options)
        except Exception as e:
            raise FileNotFoundError(
                f"ChromeDriver를 찾을 수 없습니다.\n"
                f"다음 중 하나를 실행하세요:\n"
                f"  macOS: brew install chromedriver\n"
                f"  또는 https://chromedriver.chromium.org/ 에서 다운로드\n"
                f"에러: {e}"
            )

    # driver_path가 지정된 경우 해당 경로 사용
    if not Path(driver_path).exists():
        raise FileNotFoundError(
            f"ChromeDriver를 찾을 수 없습니다: {driver_path}\n"
            f"파일이 존재하는지 확인하세요."
        )

    service = Service(str(driver_path))
    return webdriver.Chrome(service=service, options=options)


def save_comments_to_csv(comments, output_path=None):
    """댓글을 CSV 파일로 저장"""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(__file__).resolve().parent / f"comments_{timestamp}.csv"

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['comment', 'timestamp'])
        for comment_text, comment_time in comments:
            writer.writerow([comment_text, comment_time])

    print(f"✅ {len(comments)}개 댓글이 저장되었습니다: {output_path}")
    return output_path


def collect_comments(live_url, duration=60, driver_path=None):
    """
    네이버 쇼핑라이브 댓글 수집

    Args:
        live_url (str): 쇼핑라이브 URL
        duration (int): 수집 시간 (초)
        driver_path (str): ChromeDriver 경로 (선택)

    Returns:
        list: [(댓글, 타임스탬프), ...]
    """
    # ✅ 함수 시작 시 즉시 초기화 (페이지 로드 실패해도 UnboundLocalError 방지)
    collected_comments = []
    driver = None

    try:
        driver = setup_driver(driver_path)
        print(f"⏳ {live_url} 접속 중...")
        driver.get(live_url)
        time.sleep(3)  # 페이지 로딩 대기

        print("⏳ 댓글 수집 시작...")
        prev_comments = set()
        start_time = time.time()

        while time.time() - start_time < duration:
            try:
                time.sleep(2)  # 2초 간격

                # ⚠️ 주의: CSS 클래스명은 네이버 UI 업데이트 시 변경될 수 있습니다
                # 실패 시 브라우저 개발자 도구에서 최신 클래스명을 확인하세요
                # 네이버 쇼핑라이브 댓글 CSS Selector
                comments = driver.find_elements(By.CSS_SELECTOR, '.CommentListItem_comment__text__1xgxd')

                for comment in comments:
                    text = comment.text.strip()
                    if text and text not in prev_comments:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"💬 [{timestamp}] {text}")
                        collected_comments.append((text, timestamp))
                        prev_comments.add(text)

            except Exception as e:
                print(f"⚠️ 댓글 추출 오류 (계속 시도): {e}")
                continue

        return collected_comments

    except KeyboardInterrupt:
        print("\n🛑 사용자가 수집을 중단했습니다.")
        return collected_comments

    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return collected_comments

    finally:
        if driver is not None:
            driver.quit()
            print("✅ 브라우저 종료 완료")


if __name__ == "__main__":
    # ✅ 예시: 네이버 쇼핑라이브 댓글 수집
    live_url = input("네이버 쇼핑라이브 URL을 입력하세요 (기본값: 예시 URL): ").strip()

    if not live_url:
        live_url = 'https://view.shoppinglive.naver.com/replays/1694229?fm=shoppinglive&sn=home'

    duration = input("수집 시간(초)을 입력하세요 (기본값: 60초): ").strip()
    duration = int(duration) if duration.isdigit() else 60

    print(f"\n📌 URL: {live_url}")
    print(f"📌 수집 시간: {duration}초\n")

    # 댓글 수집
    comments = collect_comments(live_url, duration=duration)

    # CSV 저장
    if comments:
        save_comments_to_csv(comments)
        print(f"\n✅ 총 {len(comments)}개 댓글 수집 완료!")
    else:
        print("\n⚠️ 수집된 댓글이 없습니다.")
