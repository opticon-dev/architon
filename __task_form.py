"""
task 를 작성하는 기준

상단에 task의 내용과 필요한 경우 notion 링크를 추가한다.
혹은 같은 폴더에 task 파일과 동명의 MD 파일로 작성해도 무방하다.

튜토리얼이 라이노에서 작성되어야 하는 경우 부득이한 경우를 제외하면
이 포멧을 그래스호퍼 파이썬 컴포넌트 안에 복사 하여 사용하고
컴포넌트 1개 안에서 모든 과제가 출제, 해결 가능하도록 작성해야 한다.

task와 해결은 별도 폴더에서 관리되어야 한다.
"""

### 기타 구현, 기타 클래스 및 함수 등등###

### 기타 구현, 기타 클래스 및 함수 등등 ###


### task 함수 정의 ###
def task():
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    task()


### 아래는 예시


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
