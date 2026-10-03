import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


# .env 파일에서 GEMINI_API_KEY 불러오기
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY가 없습니다. .env 파일에 키를 입력했는지 확인하세요.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"

IMAGE_PATH = "images/prodeut.jpg"


# 프롬프트
PROMPT = """당신은 마인크래프트 건축을 도와주는 AI입니다.

사용자가 제공한 이미지를 분석하고,
이미지 속 대상을 마인크래프트에서 건축할 수 있도록
건축 가이드를 만들어주세요.

이미지는 건물, 동물, 캐릭터, 음식, 자동차, 사물 등
어떤 대상이든 될 수 있습니다.

다음 형식으로 답변해주세요.

- 이미지 대상: 이미지에서 무엇을 표현하고 있는지 설명
- 주요 특징: 대상의 형태, 색상, 구조 등 중요한 특징 3~5개
- 추천 블록: 마인크래프트에서 대상을 표현하기 적합한 블록
- 색상 조합: 이미지의 주요 색상과 어울리는 블록 조합
- 예상 크기: 마인크래프트에서 구현하기 적절한 대략적인 크기
- 건축 구조: 전체적인 구조와 블록 배치 방법
- 건축 순서: 처음부터 완성까지의 단계별 건축 방법
- 추가 아이디어: 건축물을 더 잘 표현하거나 꾸밀 수 있는 방법 3개

사용자가 입력한 추가 요구사항이 있다면 반드시 반영해주세요.

이미지에서 확인할 수 없는 정보를 사실처럼 단정하지 마세요.
정확하게 판단하기 어려운 부분은 '추정'이라고 표시해주세요.
"""


def main():

    # 이미지 파일 확인
    if not os.path.exists(IMAGE_PATH):
        print(f"이미지를 찾을 수 없습니다: {IMAGE_PATH}")
        print("images 폴더에 prodeut.jpg 파일이 있는지 확인하세요.")
        sys.exit(1)

    # 사용자에게 건축 요구사항 입력받기
    user_request = input(
        "원하는 건축 스타일이나 크기 등을 입력하세요: "
    )

    # 이미지 읽기
    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    # 이미지 데이터 생성
    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg",  # PNG라면 image/png로 변경
    )

    # Gemini에 이미지 + 텍스트 전달
    print("\nGemini API 호출 중...\n")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                image_part,
                PROMPT + user_request
            ],
        )

    except Exception as e:
        print("API 호출 중 오류가 발생했습니다:", e)
        sys.exit(1)

    # 결과 출력
    print("\n=== BlockBuild AI 건축 가이드 ===\n")
    print(response.text)


if __name__ == "__main__":
    main()