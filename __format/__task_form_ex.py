"""
TASK: 주어진 점 데이터에서 볼록 껍질(Convex Hull) 계산하기
Notion: https://www.notion.so/example

환경: Grasshopper Python Component
입력: points.csv (x,y 좌표 목록)
출력: hull.csv (볼록 껍질을 이루는 점의 좌표 순서)

샘플 데이터:
  input/points_sample.csv
  output/hull_sample.csv
"""


### task 함수 정의 ###
def task(
    input_path: str = "input/points_sample.csv", output_path: str = "output/hull.csv"
):
    """
    Args:
        input_path (str): 입력 CSV 파일 경로
        output_path (str): 출력 CSV 파일 경로
    """
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    task()
