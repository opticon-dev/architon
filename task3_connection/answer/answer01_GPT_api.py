import os
import base64
from typing import Optional
from openai import OpenAI

GPT_API_KEY = None  # 본인의 api key를 사용한다.


def _encode_image_to_base64(image_path: str) -> str:
    # 이미지 파일을 base64로 인코딩한다.
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def task(image_path: str, prompt: str) -> str:
    """
    ChatGPT API에 이미지와 프롬프트를 전송하여 평가 텍스트를 받아온다.

    Args:
        image_path (str): 이미지 경로
        prompt (str): 프롬프트

    Returns:
        str: 모델의 응답 텍스트
    """

    # 키 우선순위: 환경변수 -> 파일에 정의된 상수
    client = OpenAI(api_key=GPT_API_KEY)

    image_b64 = _encode_image_to_base64(image_path)

    messages = [
        {
            "role": "system",
            "content": (
                "당신은 세계적인 건축가입니다. 사용자가 제공한 건축 이미지를 정교하게 분석하고,"
                " 재료, 비례, 빛, 공간 구성, 맥락성 등을 다각도로 평가하세요."
            ),
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_b64}",
                    },
                },
            ],
        },
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=800,
    )

    return resp.choices[0].message.content or ""


if __name__ == "__main__":
    image_path = "task3_connection/input/task01_GPT_api.png"
    prompt = "당신은 세계적인 건축가 안도다다오다. 이 이미지를 건축적으로 해석하고 자신만의 독창적인 의견을 내도록 하라"
    print(task(image_path, prompt))
