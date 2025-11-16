"""
댓글 CSV 파일 검증 스크립트
사용법: python test.py [csv_파일_경로]
"""
import pandas as pd
import sys
from pathlib import Path

# CSV 파일 경로 (CLI 인자 또는 기본값)
csv_path = sys.argv[1] if len(sys.argv) > 1 else 'comments.csv'

if not Path(csv_path).exists():
    print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
    print(f"\n사용법: python test.py [csv_파일_경로]")
    print(f"예시: python test.py comments_20250101_120000.csv")
    sys.exit(1)

df = pd.read_csv(csv_path)
print(f"✅ CSV 파일: {csv_path}")
print(f"✅ 댓글 개수: {len(df)}")
print(f"✅ 컬럼: {list(df.columns)}")