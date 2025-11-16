# 6faq_chatbot.py

import json
from pathlib import Path
import gradio as gr

def load_faq_data():
    """FAQ 데이터 로드"""
    faq_path = Path(__file__).resolve().parent / "faq_data.json"
    with open(faq_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ 프로세스 시작 시 한 번만 로드
FAQ_DATA = load_faq_data()

def get_answer(question):
    """질문 → 답변 반환 함수"""
    for faq in FAQ_DATA:
        if faq["question"] == question:
            return f"**Q. {faq['question']}**\n\n{faq['answer']}"
    return "해당 질문에 대한 답변을 찾을 수 없습니다."

def create_ui():
    """Gradio UI 생성"""

    with gr.Blocks(title="농담터 고객 FAQ 챗봇") as demo:
        gr.Markdown("## 💬 궁금하신 내용을 선택해보세요!")

        output = gr.Textbox(label="답변", lines=6, interactive=False)

        # ✅ 각 FAQ 버튼 생성 (클로저 문제 해결)
        with gr.Row():
            for faq in FAQ_DATA:
                btn = gr.Button(faq["question"])
                # 클로저 문제 해결: 람다 기본 인자로 값 고정
                btn.click(fn=lambda q=faq["question"]: get_answer(q), inputs=None, outputs=output)

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
