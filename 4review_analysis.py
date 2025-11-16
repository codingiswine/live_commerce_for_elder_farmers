# 4review_analysis.py

import sys
from pathlib import Path
from openai import OpenAI

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.env_loader import load_env

# ✅ OpenAI 클라이언트 초기화
api_key = load_env()
client = OpenAI(api_key=api_key)

def analyze_review(review_text):
    prompt = f"""
    다음은 고객 리뷰야:

    "{review_text}"

    이 리뷰에 대해 다음을 판단해줘:
    1. 감정이 긍정인지 부정인지 중립인지
    2. 핵심 키워드 2~3개만 뽑아줘

    출력 형식:
    감정: [긍정/부정/중립]
    키워드: [키워드1, 키워드2, ...]
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 리뷰 감정 분석 전문가야"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    # 서로게이트 페어 문자 안전 처리
    content = response.choices[0].message.content
    return content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

# 🧪 반복 입력 실행
if __name__ == "__main__":
    print("🧠 리뷰 감정 분석기")
    print("리뷰를 입력하면 감정과 키워드를 분석해줘요.")
    print("끝내려면 '끝' 이라고 입력하세요.\n")

    while True:
        review = input("고객 리뷰: ")

        if review.strip() == "끝":
            print("👋 분석을 종료합니다!")
            break

        result = analyze_review(review)
        print("\n📊 분석 결과:")
        print(result)
        print("-" * 40)
