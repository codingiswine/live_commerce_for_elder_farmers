# 1generate_description.py

import sys
from pathlib import Path
from openai import OpenAI

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.env_loader import load_env

# ✅ OpenAI 클라이언트 초기화
api_key = load_env()
client = OpenAI(api_key=api_key)

def generate_description(name, weight, features):
    """상품 설명을 자동 생성하는 함수"""
    try:
        prompt = f"""
        아래 상품 정보를 바탕으로 고객의 관심을 끌 수 있는 상품 설명을 작성해줘.
        직접 제배하고 판매하는 농부의 마음으로 따뜻하고 신뢰감 있는 말투로 써줘. 이모지도 포함해줘.

        상품 이름: {name}
        무게: {weight}
        특징: {', '.join(features)}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 직접 재배하고 판매하는 농부이자 농산물 마케터야. 감성적인 상품 설명을 잘 써."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300
        )

        # 서로게이트 페어 문자 안전 처리
        content = response.choices[0].message.content
        # 서로게이트 문자를 제거하고 안전한 문자열로 변환
        safe_content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        return safe_content

    except Exception as e:
        return f"❌ 설명 생성 실패: {str(e)}"

# 🧪 사용자 입력 테스트
if __name__ == "__main__":
    print("📝 상품 설명 자동 생성기")

    name = input("상품 이름을 입력하세요: ")
    weight = input("무게를 입력하세요 (예: 5kg): ")
    features_input = input("특징들을 쉼표로 구분해서 입력하세요 (예: 아삭함, 달콤함): ")

    features = [f.strip() for f in features_input.split(',') if f.strip()]

    print("\n🧠 AI가 설명을 생성 중입니다...\n")
    description = generate_description(name, weight, features)
    print("📦 생성된 상품 설명:\n")
    print(description)
