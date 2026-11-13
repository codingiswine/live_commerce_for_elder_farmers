# 🎭 감정분류 프로젝트

> KR-ELECTRA 기반 한국어 감정 분석 시스템
> 44개 감정 클래스 멀티라벨 분류 파인튜닝

## 📸 프로젝트 데모

![Emotion Classification Demo](emotion_classification.png)

---

## ⚠️ 데이터 저작권 관련 안내

### 📋 데이터 출처 및 사용 목적

본 프로젝트에서 사용된 데이터는 다음과 같습니다:

#### 1. KOTE 데이터셋 (Korean Online That-gul Emotions)
- **출처**: [https://github.com/searle-j/KOTE](https://github.com/searle-j/KOTE) (44개 감정 라벨 멀티라벨 데이터셋)
- **라이선스**: 원 저장소의 이용 조건 참조
- **사용 목적**: 학습 및 연구 목적 (포트폴리오)
- **포함 데이터**: `train.tsv`, `test.tsv`, `val.tsv` (총 50,000개 샘플)

#### 2. 댓글 데이터 (comments_YYYYMMDD_HHMMSS.csv)
- **출처**: 네이버 쇼핑라이브 공개 댓글
- **사용 목적**: 실습 및 PoC (Proof of Concept)
- **개인정보 처리**: 모든 개인 식별 정보 제거됨
- **상태**: **예시 데이터로만 사용** (상업적 사용 불가)

#### 3. 학습된 모델 가중치
- **베이스 모델**: snunlp/KR-ELECTRA-discriminator (MIT License)
- **파인튜닝 모델**: 본 프로젝트에서 학습 (비공개)
- **재배포**: 불가 (포트폴리오 목적으로만 사용)

---

## 🔒 데이터 사용 제한 사항

### ✅ 허용 사항
- 학습 및 연구 목적 사용
- 포트폴리오 및 면접 목적 공개
- 코드 및 학습 방법론 공개

### ❌ 금지 사항
- 상업적 사용
- 데이터 재배포
- 학습된 모델 가중치 공개 배포
- 개인정보가 포함된 원본 데이터 공개

---

## 📊 프로젝트 개요

### 목표
- 44개 감정 클래스 멀티라벨 분류
- KR-ELECTRA 기반 한국어 감정 분석 모델 파인튜닝
- 네이버 쇼핑라이브 실시간 댓글 감정 분석

### 성능
- **F1 Score**: 학습 중 최고 validation F1 0.6105 (Epoch 8, multi-label, logit > 0.5 기준(시그모이드 확률 약 0.62))
- **참고**: 동일 평가 기준(test set, single-label — argmax 1개 vs 첫 번째 정답 라벨) 사전학습 모델 F1 0.0166 → 파인튜닝 후 0.2196. 위 validation multi-label F1 0.6105와는 다른 평가 방식이다. 사전학습 모델의 0.0166은 분류 헤드가 학습되지 않은 무작위 수준이라, 이 차이를 성능 향상 배수로 환산하지 않는다

---

## 🏗️ 프로젝트 구조

```
감정분류/
├── comment.py             # Selenium 댓글 수집
├── 1analyze-sentiment.py # LangChain 감정 분석
├── 2analyze-sentiment-graph.py   # 감정 분포 시각화
├── test.py                       # CSV 파일 검증 스크립트
│
├── sentiment_classification/     # KR-ELECTRA 파인튜닝
│   ├── train.ipynb              # 학습 노트북 (Google Colab)
│   ├── config.json              # 모델 설정
│   ├── tokenizer_config.json    # 토크나이저 설정
│   ├── special_tokens_map.json  # 특수 토큰
│   ├── tokenizer.json           # 토크나이저
│   ├── vocab.txt                # 어휘 사전
│   └── train_log.csv            # 학습 로그 — 마지막 epoch 기록만 포함 (epoch별 값은 train.ipynb 출력 참조)
│
├── sentiment_plot.png            # 감정별 분포 (시각화 결과)
├── type_plot.png                 # 유형별 분포 (시각화 결과)
└── README.md
```

**📁 사용자가 직접 생성하는 파일:**
- `comments_YYYYMMDD_HHMMSS.csv` - comment.py 실행 시 생성 (개인정보 보호로 저장소 제외)
- `live_comments_result.csv` - 1analyze-sentiment.py 실행 시 생성
- `chromedriver` - 시스템 PATH에 설치 (brew install chromedriver 권장)

**📁 학습 데이터 (저장소 제외):**
- `train.tsv`, `val.tsv`, `test.tsv` - KOTE 저장소(https://github.com/searle-j/KOTE)에서 다운로드 필요
- KR-ELECTRA 파인튜닝 재현 시에만 필요

---

## 🚀 실행 방법

### 1. 환경 설정

```bash
# 프로젝트 루트에서 패키지 설치 (모든 의존성 포함)
cd ..
pip install -r requirements.txt

# ChromeDriver 설치 (Selenium용 - comment.py 실행 시 필요)
# macOS: brew install chromedriver
# 또는 https://chromedriver.chromium.org/ 에서 다운로드
```

### 2. 댓글 수집

```bash
# ChromeDriver 설치 확인 (PATH에 있어야 함)
which chromedriver  # macOS/Linux
# 없다면: brew install chromedriver

# 댓글 수집 실행
python comment.py

# 생성된 파일: comments_YYYYMMDD_HHMMSS.csv
# 예: comments_20250116_140530.csv
```

**CSV 파일 형식:**
```csv
comment,timestamp
"좋아요!",2025-01-16 14:05:30
"배송 빠르네요",2025-01-16 14:05:32
```

**⚠️ 주의**:
- ChromeDriver는 시스템 PATH에 설치되어 있어야 합니다
- 실제 서비스 댓글 수집 시 해당 플랫폼의 이용약관을 준수해야 합니다
- 저장소에는 개인정보 보호를 위해 CSV 파일이 포함되지 않습니다

### 3. 감정 분석 (LangChain)

```bash
# 프로젝트 루트에 .env 파일 생성 및 OpenAI API 키 설정
cd ..
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 감정 분석 실행
cd 감정분류

# 방법 1: 기본 파일명 사용 (comments.csv로 저장한 경우)
python 1analyze-sentiment.py

# 방법 2: 특정 CSV 파일 지정
python 1analyze-sentiment.py --input comments_20250116_140530.csv

# 출력: live_comments_result.csv (분석 결과)
```

**필수 조건:**
- OpenAI API 키가 `.env` 파일에 설정되어 있어야 함
- `comments.csv` 또는 `--input`으로 지정한 CSV 파일이 존재해야 함

### 4. KR-ELECTRA 파인튜닝

```bash
# train.ipynb는 Google Colab 전용 (google.colab drive.mount, apt-get,
# DATA_DIR=/content/drive/... 경로 사용) — 로컬 Jupyter에서는 그대로 실행되지 않음
# sentiment_classification/train.ipynb를 Colab에서 열어 실행
```

### 5. 감정 분포 시각화

```bash
# 감정 분석 결과가 있어야 함 (live_comments_result.csv)
python 2analyze-sentiment-graph.py

# 출력:
# - sentiment_plot.png (감정별 분포)
# - type_plot.png (유형별 분포)
```

**필수 조건:**
- `1analyze-sentiment.py` 실행 후 생성된 `live_comments_result.csv` 필요

---

## 🧠 모델 아키텍처

### KR-ELECTRA 파인튜닝

```python
# 베이스 모델
model_name = "snunlp/KR-ELECTRA-discriminator"

# 하이퍼파라미터
BATCH_SIZE = 16
EPOCHS = 10
LEARNING_RATE = 2e-5
PATIENCE = 3  # Early Stopping (10 epoch 내 미발동)
NUM_LABELS = 44  # 멀티라벨 분류
MAX_LENGTH = 128

# 손실 함수
criterion = torch.nn.BCEWithLogitsLoss()

# 옵티마이저
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
```

### 학습 과정

1. **데이터 로드**: KOTE 데이터셋 (train: 40,000 / val: 5,000 / test: 5,000)
2. **토큰화**: KR-ELECTRA 토크나이저 (Max Length: 128)
3. **학습**: 10 Epochs — Early Stopping(patience=3) 설정, 10 epoch 내 미발동(카운터 최대 2/3), 최고 성능(Epoch 8) 체크포인트 저장. LR 2e-5 고정 (스케줄러·튜닝 없음)
4. **평가**: F1 Score (Micro Averaging)

### 학습 결과

| Epoch | Train Loss | Val F1 Score |
|-------|-----------|--------------|
| 1 | 0.3406 | 0.4873 |
| 2 | 0.2852 | 0.5428 |
| 3 | 0.2642 | 0.5812 |
| 4 | 0.2481 | 0.5695 |
| 5 | 0.2335 | 0.5837 |
| 6 | 0.2191 | 0.6022 |
| 7 | 0.2055 | 0.6055 |
| **8** | **0.1932** | **0.6105** ⭐ |
| 9 | 0.1814 | 0.6104 |
| 10 | 0.1706 | 0.6011 |

**Best Model: Epoch 8 (F1 Score: 0.6105)**

---

## 📊 감정 분류 체계

### 44개 감정 클래스

모델 출력은 인덱스 0~43의 44개 라벨입니다 (`config.json`에는 `LABEL_0`~`LABEL_43`으로만 저장, 감정명 매핑은 저장소에 없음). 각 인덱스의 감정 정의는 KOTE 데이터셋 원 저장소([https://github.com/searle-j/KOTE](https://github.com/searle-j/KOTE))의 라벨 정의를 따릅니다.

`train.ipynb`의 댓글 예측 단계에서는 44개 인덱스를 3개 그룹으로 묶어 댓글별 요약 감정을 산출합니다 (학습·평가에는 사용하지 않고, 댓글 예측 요약에만 사용):

- 🟢 **긍정 (12개 인덱스)**: `positive_idx = [1, 2, 4, 8, 14, 15, 16, 19, 33, 41, 42, 43]`
- 🔴 **부정 (16개 인덱스)**: `negative_idx = [0, 3, 5, 6, 10, 12, 20, 21, 22, 23, 25, 26, 27, 36, 38, 40]`
- ⚪ **중립 (16개 인덱스)**: `neutral_idx = [7, 9, 11, 13, 17, 18, 24, 28, 29, 30, 31, 32, 34, 35, 37, 39]`

---

## 🎯 활용 방안

### 1. 미술품 투자 플랫폼 (열매컴퍼니)
- **투자자 리뷰 감정 분석**: 긍정·부정·중립 자동 분류
- **시장 심리 지표 생성**: 투자 트렌드 파악
- **작품 평가 자동화**: 리뷰 기반 작품 평점 산출

### 2. 전자상거래 플랫폼
- **상품 리뷰 자동 분석**: CS 업무 자동화
- **고객 만족도 모니터링**: 실시간 감정 추적
- **위기 상황 조기 감지**: 부정 감정 급증 알림

### 3. 소셜 미디어 모니터링
- **브랜드 평판 관리**: 실시간 여론 분석
- **인플루언서 마케팅**: 댓글 반응 분석
- **위기 관리**: 부정 여론 조기 감지

---

## 🛠️ 기술 스택

### ML/DL
- **PyTorch**: ~=2.1 (requirements.txt 기준)
- **Transformers**: 4.40.2
- **HuggingFace**: AutoTokenizer, AutoModelForSequenceClassification (커스텀 PyTorch 학습 루프)

### 데이터 처리
- **Pandas**: 데이터 전처리
- **NumPy**: 수치 연산
- **Scikit-learn**: F1 Score 평가

### 웹 크롤링
- **Selenium**: 실시간 댓글 수집

### 프롬프트 AI
- **LangChain**: 프롬프트 기반 감정 분석
- **OpenAI API**: GPT-4o

### 시각화
- **Matplotlib**: 감정 분포 그래프

---

## 📈 성능 비교

| 모델 | F1 Score (Micro, test set·single-label) | 비고 |
|-----|-----------------|------|
| snunlp/KR-ELECTRA (사전학습) | 0.0166 | 베이스라인 |
| **파인튜닝 모델 (Epoch 8)** | **0.2196** | 베이스라인은 분류 헤드 미학습 상태라 향상 배수로 환산하지 않음 |

> 참고: 학습 중 validation set에서 multi-label, logit > 0.5 기준(시그모이드 확률 약 0.62)으로 측정한 최고 F1은 0.6105(Epoch 8)입니다. 위 표는 사전학습 모델과 동일한 평가 방식(test set·single-label)으로 비교한 수치입니다.

---

## 🔮 향후 계획

- [ ] Vision AI 추가 (이미지 기반 감정 분석)
- [ ] 실시간 스트리밍 댓글 분석 시스템
- [ ] MLOps 파이프라인 구축 (Docker, K8s, MLflow)
- [ ] FastAPI 기반 REST API 서버 구축
- [ ] React 기반 대시보드 개발

---

## 📝 라이선스 및 저작권

### 코드
- **라이선스**: 별도 LICENSE 파일 없음

### 데이터
- **KOTE 데이터셋**: 원 저장소(https://github.com/searle-j/KOTE)의 이용 조건 참조
- **댓글 데이터**: 예시 데이터로만 사용 (상업적 사용 불가)
- **재배포 금지**: 원본 데이터 재배포 불가

### 모델
- **베이스 모델**: snunlp/KR-ELECTRA-discriminator (MIT License)
- **파인튜닝 모델**: 비공개 (포트폴리오 목적으로만 사용)

**⚠️ 중요**: 본 프로젝트는 **학습 및 포트폴리오 목적**으로만 제작되었으며, 상업적 사용을 목적으로 하지 않습니다.

---

## 👨‍💻 개발자

**Daniel_Shin**
- 📧 Email: codingiswine@gmail.com
- 💻 GitHub: https://github.com/codingiswine

---

## 🙏 참고 자료

- **KR-ELECTRA**: [https://github.com/snunlp/KR-ELECTRA](https://github.com/snunlp/KR-ELECTRA)
- **KOTE (Korean Online That-gul Emotions) Dataset**: [https://github.com/searle-j/KOTE](https://github.com/searle-j/KOTE)
- **HuggingFace Transformers**: [https://huggingface.co/docs/transformers](https://huggingface.co/docs/transformers)
- **PyTorch**: [https://pytorch.org/](https://pytorch.org/)
