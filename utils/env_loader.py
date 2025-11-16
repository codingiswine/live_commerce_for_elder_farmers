"""
환경 변수 로딩 공통 유틸리티
모든 스크립트에서 일관되게 .env 파일을 로드하기 위한 모듈
"""

from pathlib import Path
from dotenv import load_dotenv
import os


def load_env():
    """
    프로젝트 루트의 .env 파일을 로드하고 OPENAI_API_KEY를 반환

    Returns:
        str: OpenAI API Key

    Raises:
        FileNotFoundError: .env 파일이 없을 경우
        ValueError: OPENAI_API_KEY가 설정되지 않은 경우
    """
    # ✅ 현재 파일부터 상위 디렉토리들을 순회하며 .env 탐색
    current = Path(__file__).resolve()
    env_path = None

    # 현재 파일 위치 + 모든 상위 디렉토리 순회
    for parent in [current.parent] + list(current.parents):
        candidate = parent / ".env"
        if candidate.exists():
            env_path = candidate
            break

    if env_path is None:
        raise FileNotFoundError(
            f".env 파일을 찾을 수 없습니다.\n"
            f"현재 파일 위치: {current}\n"
            f"프로젝트 루트에 .env 파일을 생성하고 OPENAI_API_KEY를 설정하세요."
        )

    # .env 파일 로드
    load_dotenv(env_path)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            f".env 파일이 존재하지만 OPENAI_API_KEY가 설정되지 않았습니다.\n"
            f"파일 위치: {env_path}\n"
            f".env 파일에 다음과 같이 추가하세요:\n"
            f"OPENAI_API_KEY=your_api_key_here"
        )

    return api_key


def get_project_root():
    """
    프로젝트 루트 경로 반환

    Returns:
        Path: 프로젝트 루트 경로
    """
    return Path(__file__).resolve().parents[1]
