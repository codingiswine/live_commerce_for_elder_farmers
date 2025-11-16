# 2generate_image.py

import sys
from pathlib import Path
from openai import OpenAI

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.env_loader import load_env

# ✅ OpenAI 클라이언트 초기화
api_key = load_env()
client = OpenAI(api_key=api_key)

def generate_product_image(name, features):
    """상품 이미지를 자동 생성하는 함수"""
    try:
        # 서로게이트 페어 문자 안전 처리
        safe_name = name.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        safe_features = [f.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore') for f in features]

        prompt = f"{safe_name}, {', '.join(safe_features)} 느낌의 고화질 상품 사진, 깨끗하고 자연광 아래 촬영된 것처럼"

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        return response.data[0].url

    except Exception as e:
        print(f"❌ 이미지 생성 실패: {str(e)}")
        return None

# 🧪 사용자 입력 테스트
if __name__ == "__main__":
    print("🖼️ 상품 이미지 자동 생성기")

    name = input("상품 이름을 입력하세요: ")
    features_input = input("특징들을 쉼표로 구분해서 입력하세요 (예: 달콤함, 촉촉함): ")
    features = [f.strip() for f in features_input.split(',') if f.strip()]

    print("\n🎨 AI가 이미지를 생성 중입니다...\n")
    image_url = generate_product_image(name, features)

    if image_url:
        print("🖼️ 생성된 이미지 URL:")
        print(image_url)
    else:
        print("⚠️ 이미지 생성에 실패했습니다.")
