"""
TASK: 계단으로 극복해야 하는 거리와 높이가 정해졌을 때, 계단의 3차원 형태를 리턴하는 함수를 작성한다.

환경: python shapely
입력: 계단의 거리(m), 계단의 높이(m)
출력: List[shapely.geometry.Polygon(Z)](계단의 3차원 형태, 편의상 상판만 표현한다.)

샘플 데이터:
  check/check02_stairs_output.png
"""


### task 함수 정의 ###
def task(
    total_dist: float,
    total_height: float,
):
    """
    Args:
        total_dist (float): 계단의 거리(m)
        total_height (float): 계단의 높이(m)
    """
    # shapely geometry polygon은 z 가 있는 3차원 형태를 표현할 수 있다.
    # 단 geometry 연산은 z 값을 무시하고 이뤄진다.
    # 여기서는 적절한 계단의 깊이와 높이를 구하고,
    # 계단 상판의 모양을 상상하라
    # 이를 polygon으로 구현한 후에, 리스트에 넣어 반환하라
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    total_dist = 10
    total_height = 3

    stairs = task(total_dist, total_height)
    from utils import show_polygons

    show_polygons(stairs)
