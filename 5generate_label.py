# 5generate_label.py

import sys
from pathlib import Path
from openai import OpenAI

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.env_loader import load_env

# ✅ OpenAI 클라이언트 초기화
api_key = load_env()
client = OpenAI(api_key=api_key)

def generate_label(name, farmer_name, region, features):
    prompt = f"""
    아래 정보를 기반으로 상품 라벨에 들어갈 감성 문구를 1~2줄 생성해줘.
    따뜻하고 신뢰감 있는 문장을 원해. 이모지도 포함해줘.

    상품명: {name}
    농부명: {farmer_name}
    지역: {region}
    특징: {features}

    출력은 꼭 문장만 해줘.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 감성 있는 문구를 잘 만드는 카피라이터야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=200
    )

    # 서로게이트 페어 문자 안전 처리
    content = response.choices[0].message.content.strip()
    return content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

# 🧪 테스트 실행
if __name__ == "__main__":
    print("🧷 라벨 문구 자동 생성기\n")
    name = input("상품명: ")
    farmer_name = input("농부 이름: ")
    region = input("지역: ")
    features = input("상품 특징 (쉼표로 구분): ")

    result = generate_label(name, farmer_name, region, features)
    print("\n🏷️ 생성된 라벨 문구:\n" + result)
