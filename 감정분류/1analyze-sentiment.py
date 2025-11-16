import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import sys
from pathlib import Path
from tqdm import tqdm
import json

# utils 모듈 import를 위한 경로 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.env_loader import load_env

# ✅ 1. .env에서 API 키 불러오기
openai_api_key = load_env()

# ✅ 2. GPT 모델 설정
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o",
    openai_api_key=openai_api_key
)

# ✅ 3. 프롬프트 템플릿 (감정 + 유형 + 요약 포함)
prompt = PromptTemplate(
    input_variables=["comment"],
    template="""
아래 채팅 내용을 분석하여 다음 정보를 제공해주세요:

- 감정 (하나 선택): 매우 긍정 / 긍정 / 중립 / 부정 / 매우 부정
- 유형 (하나 선택): 감탄 / 질문 / 불만 / 요청 / 제안 / 잡담 / 기타
- 요약: 한 줄로 이 채팅의 특징을 설명해주세요.

결과는 JSON 형식으로 작성해주세요. 예:
{{
  "감정": "긍정",
  "유형": "감탄",
  "요약": "기분 좋게 칭찬한 말이에요."
}}

채팅: "{comment}"
"""
)

# ✅ 4. LangChain 체인 생성 (최신 문법)
chain = prompt | llm

# ✅ 5. 댓글 CSV 불러오기
import argparse
from pathlib import Path

# CLI 인자 파싱
parser = argparse.ArgumentParser(description='댓글 감정 분석')
parser.add_argument('--input', type=str, default='comments.csv',
                    help='분석할 댓글 CSV 파일 경로 (기본값: comments.csv)')
args = parser.parse_args()

# CSV 파일 존재 확인
csv_path = Path(args.input)
if not csv_path.exists():
    raise FileNotFoundError(
        f"CSV 파일을 찾을 수 없습니다: {csv_path}\n\n"
        f"다음 단계를 따라주세요:\n"
        f"1. comment.py를 실행하여 댓글 수집\n"
        f"   python comment.py\n"
        f"2. 생성된 CSV 파일을 입력으로 지정\n"
        f"   python 1analyze-sentiment.py --input comments_YYYYMMDD_HHMMSS.csv\n\n"
        f"또는 기본 파일명(comments.csv)으로 저장한 후 실행하세요."
    )

df = pd.read_csv(csv_path)
print(f"✅ CSV 파일 로드 완료: {csv_path} ({len(df)}개 댓글)")

# ✅ 6. 감정 분석 실행 (재시도 로직 + 중간 저장)
print("🔍 댓글 감정 분석 중...")
results = []
failed_indices = []

for idx, comment in enumerate(tqdm(df["comment"], desc="분석 진행중")):
    success = False
    result_content = "{}"

    # 재시도 로직 (최대 3회)
    for attempt in range(3):
        try:
            result = chain.invoke({"comment": comment})
            # ChatOpenAI는 AIMessage 객체 반환하므로 content 추출
            result_content = result.content if hasattr(result, 'content') else str(result)
            success = True
            break
        except Exception as e:
            if attempt == 2:  # 마지막 시도 실패
                print(f"\n⚠️ 분석 실패 (Row {idx}): {e}")
                failed_indices.append(idx)
            else:
                import time
                time.sleep(1)  # 1초 대기 후 재시도

    results.append(result_content)

    # 20개마다 중간 저장
    if (idx + 1) % 20 == 0:
        df_temp = df.copy()
        df_temp["분석결과"] = results + ["{}"] * (len(df) - len(results))
        df_temp.to_csv("live_comments_checkpoint.csv", index=False)
        print(f"\n💾 중간 저장 완료: {idx + 1}/{len(df)}")

# 실패한 row 정보 저장
if failed_indices:
    print(f"\n⚠️ 총 {len(failed_indices)}개 댓글 분석 실패")
    with open("failed_analysis.txt", "w") as f:
        f.write("\n".join(map(str, failed_indices)))

# ✅ 7. 결과를 DataFrame에 저장
df["분석결과"] = results

# ✅ 8. JSON 문자열을 파싱하여 감정, 유형, 요약 분리
def extract_field(row, key):
    try:
        # JSON 파싱 시도
        parsed = json.loads(row)
        return parsed.get(key)
    except json.JSONDecodeError:
        # JSON이 아닌 경우 빈 값 반환
        return None
    except Exception as e:
        print(f"⚠️ 파싱 오류: {e}")
        return None

df["감정"] = df["분석결과"].apply(lambda x: extract_field(x, "감정"))
df["유형"] = df["분석결과"].apply(lambda x: extract_field(x, "유형"))
df["요약"] = df["분석결과"].apply(lambda x: extract_field(x, "요약"))

# ✅ 9. 감정·유형 통계 출력
print("\n📊 감정별 개수:")
print(df["감정"].value_counts())

print("\n📊 유형별 개수:")
print(df["유형"].value_counts())

print("\n📋 요약 샘플:")
print(df[["comment", "요약"]].head())

# ✅ 10. 결과 저장
df.to_csv("live_comments_result.csv", index=False)
print("\n✅ 감정 분석 완료 → live_comments_result.csv 저장됨")
