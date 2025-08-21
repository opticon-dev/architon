from shapely.geometry import Polygon

"""
TASK: 주어진 임의의 가로, 세로 사각형에 대해 주차장을 계획하는 함수를 작성한다.

환경: python shapely
입력: shapely.geometry.Polygon(가로, 세로 사각형)
출력: List[shapely.geometry.Polygon](주차장 cell의 리스트)

샘플 데이터:
  check/check01_parking_output.png
"""


### task 함수 정의 ###
def task(
    parking_lot_boundary: Polygon,
):
    """
    Args:
        parking_lot_boundary (Polygon): 주차장 경계
    """
    # 주차장 경계를 기준으로 주차장 cell을 생성한다.
    # 주차장 cell의 크기는 2.5m x 5m 이다.
    # 주차장에서 차의 양방 교행을 위한 차선의 폭은 6m 이다, 회전구간에 별다른 조치를 할 필요는 없다.
    # 주차 계획은 아래 두가지를 포함해야 한다.
    # 1. 주차장 외곽을 돌면서 형성되는 주차 cell들
    # 2. 주차장 내측으로 들어와서 주차 가능한 cell들
    # 모든 주차 cell들은 주행로에 연결되어야 한다.
    # 위 조건은 output/task01_parking_output.png 을 참고하도록 한다.
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    # parking lot 의 폭은 M를 사용한다.
    # 한 parking cell의 크기는 2.5m x 5m 이다.
    parking_lot_width = 100
    parking_lot_height = 100
    parking_lot_boundary = Polygon(
        [
            (0, 0),
            (parking_lot_width, 0),
            (parking_lot_width, parking_lot_height),
            (0, parking_lot_height),
        ]
    )
    parking_cells = task(parking_lot_boundary)
    from utils import show_polygons

    show_polygons(parking_lot_boundary, *parking_cells)
