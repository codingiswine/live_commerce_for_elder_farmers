import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')  # headless 환경 대응
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from pathlib import Path
import sys
import platform

# ✅ 1. 한글 폰트 자동 탐지 (macOS/Linux/Windows 대응)
def find_korean_font():
    """시스템에서 사용 가능한 한글 폰트 찾기"""
    korean_fonts = [
        "NanumGothic",
        "Malgun Gothic",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "Noto Sans KR",
        "DejaVu Sans"
    ]

    available_fonts = [f.name for f in fm.fontManager.ttflist]

    for font in korean_fonts:
        if any(font in available for available in available_fonts):
            return font

    # 폰트를 찾지 못한 경우 기본 폰트 사용
    print("⚠️ 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    return "DejaVu Sans"

# ✅ 2. 폰트 적용
korean_font = find_korean_font()
plt.rcParams["font.family"] = korean_font
plt.rcParams["axes.unicode_minus"] = False
sns.set(style="whitegrid")

# ✅ 3. 데이터 로드 (상대 경로 사용)
current_dir = Path(__file__).resolve().parent
data_file = current_dir / "live_comments_result.csv"

if not data_file.exists():
    raise FileNotFoundError(
        f"분석 결과 파일을 찾을 수 없습니다: {data_file}\n"
        f"먼저 1analyze-sentiment.py를 실행하여 데이터를 생성하세요."
    )

df = pd.read_csv(data_file)

# ✅ 안전한 JSON 파싱 함수
def safe_parse_result(raw):
    """JSON 문자열을 안전하게 파싱 (실패 시 None 반환)"""
    if not isinstance(raw, str):
        return None
    try:
        # JSON 파싱 시도
        return json.loads(raw)
    except json.JSONDecodeError:
        # ast.literal_eval fallback (이전 데이터 호환용)
        try:
            import ast
            return ast.literal_eval(raw)
        except Exception:
            return None
    except Exception:
        return None

# 파싱 및 필드 추출
df["분석결과_parsed"] = df["분석결과"].apply(safe_parse_result)

# dict 타입 확인 후 필드 추출 (안전성 강화)
df["감정"] = df["분석결과_parsed"].apply(lambda x: x.get("감정") if isinstance(x, dict) else None)
df["유형"] = df["분석결과_parsed"].apply(lambda x: x.get("유형") if isinstance(x, dict) else None)

# 유효한 데이터만 필터링
df_valid = df.dropna(subset=["감정", "유형"])

# ✅ 4. 저장 경로 (현재 디렉토리)
output_dir = current_dir
sentiment_img_path = output_dir / "sentiment_plot.png"
type_img_path = output_dir / "type_plot.png"

# ✅ 5. 감정별 그래프 (유효한 데이터만 사용)
plt.figure(figsize=(6, 4))
sns.countplot(data=df_valid, x="감정", palette="pastel")
plt.title("감정별 댓글 수")
plt.xlabel("감정")
plt.ylabel("댓글 수")
plt.tight_layout()
plt.savefig(sentiment_img_path, dpi=150, bbox_inches='tight')
plt.close()  # 리소스 해제
print(f"✅ 감정별 그래프 저장: {sentiment_img_path}")


# ✅ 6. 유형별 그래프 (유효한 데이터만 사용)
plt.figure(figsize=(7, 4))
sns.countplot(data=df_valid, x="유형", palette="muted")
plt.title("유형별 댓글 수")
plt.xlabel("유형")
plt.ylabel("댓글 수")
plt.tight_layout()
plt.savefig(type_img_path, dpi=150, bbox_inches='tight')
plt.close()  # 리소스 해제
print(f"✅ 유형별 그래프 저장: {type_img_path}")

print(f"\n📊 분석 완료!")
print(f"전체 댓글: {len(df)}개 / 유효한 댓글: {len(df_valid)}개")
print(f"감정별 분포: {dict(df_valid['감정'].value_counts())}")
print(f"유형별 분포: {dict(df_valid['유형'].value_counts())}")
