"""
TASK: ChatGPT API를 사용하여 input/task01_GPT_api.png 이미지와 프롬프트를 전송하여,
스스로 유명 건축가라고 생각하고 해당 이미지에 대하여 내리는 평가를 받아오는 코드를 작성한다.

환경: python openai
입력: 이미지(input/task01_GPT_api.png), 프롬프트(str)
출력: 평가(str)

샘플 데이터:

"""


### task 함수 정의 ###
def task(
    image_path: str,
    prompt: str,
):
    """
    Args:
        image_path (str): 이미지 경로
        prompt (str): 프롬프트
    """
    # openai 문서를 참조하여 이 과제를 해결하라
    # https://platform.openai.com/docs/overview

    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    image_path = "input/task01_GPT_api.png"
    prompt = "당신은 세계적인 건축가 안도다다오다. 이 이미지를 건축적으로 해석하고 자신만의 독창적인 의견을 내도록 하라"
    result = task(image_path, prompt)
    print(result)
