from check import verify_json_submission

"""
TASK:
프로젝트에 사용한 건축 자재의 총 비용을 알고 싶다.
건축 자재별 단가 데이터는 JSON 파일에, 프로젝트에 사용한 재료의 정보 데이터는 CSV 파일에 존재한다.
각 자재별 사용 개수에 따른 단가를 곱해 모든 자재의 총 비용을 합산한다.

환경: Python
입력: 프로젝트 사용 재료 데이터 경로(JSON), 건축 자재별 단가 데이터 경로(CSV)
출력: 프로젝트에 사용된 총 자재 비용(값)

출력 예시
"총 가격 : 12345678.9"

제공 데이터:
"input/material_for_project.csv"
"input/material.json"
"""


### task 함수 정의 ###
def task(
    csv_path,
    json_path,
) -> float:
    """
    Args:
        csv_path (str): 프로젝트에 사용된 재료 데이터 경로
        json_path (str): 건축 자재별 단가 데이터 경로
    """

    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    csv_path: str = "task1_data/input/material_for_project.csv"
    json_path: str = "task1_data/input/material.json"
    result = task(csv_path, json_path)

    # 정답 체크
    verify_json_submission(result)
