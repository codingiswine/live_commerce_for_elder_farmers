# 3poc_web_app.py

import sys
from pathlib import Path
import gradio as gr
from openai import OpenAI

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.env_loader import load_env

# ✅ OpenAI 클라이언트 초기화
api_key = load_env()
client = OpenAI(api_key=api_key)

# ✍️ 상품 설명 생성 함수
def generate_description(name, weight, features):
    prompt = f"""
    아래 상품 정보를 바탕으로 고객의 관심을 끌 수 있는 상품 설명을 작성해줘.
    너가 직접 재배하고 판매하는 농부의 마음으로 따뜻하고 신뢰감 있는 말투로 써줘. 이모지도 포함해줘.

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
    return content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

# 🖼️ 상품 이미지 생성 함수
def generate_image(name, features):
    # 서로게이트 페어 문자 안전 처리
    safe_name = name.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    safe_features = [f.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore') for f in features]

    prompt = f""" {safe_name}, {', '.join(safe_features)}
                프로 사진 작가가 아닌 직접 재배하고 판매하는 농부가 자연광 아래 촬영한 것처럼 보이는 현실적인 사진.
                                        과장되지 않고 생생하게 보이며, 배경은 흐릿하게 처리되어 상품이 강조됨.
                                        포장은 제거되어 있고, 상품의 신선함과 질감을 자연스럽게 보여줌.
                                        """

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )

    return response.data[0].url

# 🎯 Gradio용 통합 함수
def generate_all(name, weight, features_str):
    """상품 설명과 이미지를 동시에 생성하는 함수"""
    try:
        # 입력 검증
        if not name or not name.strip():
            return "❌ 상품 이름을 입력해주세요.", None

        if not weight or not weight.strip():
            return "❌ 무게를 입력해주세요.", None

        if not features_str or not features_str.strip():
            return "❌ 특징을 입력해주세요.", None

        features = [f.strip() for f in features_str.split(',') if f.strip()]

        if not features:
            return "❌ 유효한 특징을 입력해주세요.", None

        # 설명 생성
        description = generate_description(name, weight, features)

        # 이미지 생성
        image_url = generate_image(name, features)

        if not image_url:
            return description, None

        return description, image_url

    except Exception as e:
        return f"❌ 생성 실패: {str(e)}", None

# 🎨 Gradio UI 구성
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 농담터 상품 설명 + 이미지 자동 생성기")

    with gr.Row():
        name = gr.Textbox(label="상품 이름", placeholder="예: 무농약 감자")
        weight = gr.Textbox(label="무게", placeholder="예: 5kg")

    features = gr.Textbox(label="특징 (쉼표로 구분)", placeholder="예: 아삭함, 달콤함, 무농약")

    btn = gr.Button("🎨 생성하기")

    description_output = gr.Textbox(label="생성된 상품 설명", lines=4)
    # DALL·E는 URL을 반환하므로 HTML로 이미지 렌더링
    image_output = gr.HTML(label="생성된 상품 이미지")

    def format_output(description, image_url):
        """설명과 이미지 URL을 포맷팅"""
        if image_url:
            html = f'<img src="{image_url}" style="max-width: 100%; height: auto; border-radius: 8px;">'
            return description, html
        return description, "<p>이미지 생성 실패</p>"

    btn.click(
        fn=lambda n, w, f: format_output(*generate_all(n, w, f)),
        inputs=[name, weight, features],
        outputs=[description_output, image_output]
    )

# 🚀 실행
if __name__ == "__main__":
    demo.launch()