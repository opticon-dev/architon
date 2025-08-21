from shapely.geometry import Polygon
from utils._viauslize_utils import show_polygons

"""
TASK: 아파트 입면의 사이즈가 주어지면 아래 작업을 완료해야 한다.

1. 한 층의 층고는 3미터 이다. 이를 기준으로 층을 분리해야 한다.
2. 한 세대가 정면과 마주하는 폭은 최소 10미터 이다. 이를 기준으로 세대를 분리해야 한다. 단 각 세대가 정면과 마주하는 폭은 모두 같다.
3. 정면에서 층과 세대 구분 선을 작성했다면, 아래 기준에 따라 창문을 계획해야 한다. 
    3_1. 이 아파트는 오래된 아파트라서 3베이로 계획되어 있다. 그러므로 창은 3개이다.
        중간 창은 0-2m 높이를 갖고, 좌우 창은 1.2m - 2m 높이를 갖는다.
    3_2. 창문은 세대 구분선 좌우에서 1m 떨어진 곳에서 시작한다.
    3_3. 모든 창은 가로가 긴 창으로 황금비를 추구하지만, 창문 사이의 최소 간격은 1m 이상을 확보해야 한다.


환경: python shapely
입력: 아파트 입면의 사이즈(m), 아파트의 층수(int)
출력: List[shapely.geometry.Polygon](창문의 2차원 형태)

샘플 데이터:
  check/check03_window_output.png
"""


### task 함수 정의 ###
def task(
    apt_elevation_width: float, apt_floor_count: int, apt_floor_height: float = 3.0
):
    """
    아파트 정면 입면에서 층/세대 기준에 맞추어 3베이 창문(층별 3개)을 배치한다.

    규칙 요약:
    - 층고: 3m, 층 수에 따라 층을 분리한다.
    - 세대 폭: 최소 10m, 전체 폭을 균등 분할하여 세대를 만든다.
    - 창 배치: 세대 경계로부터 좌우 1m 내부에서 시작, 창 사이 최소 1m 유지.
    - 창 개수: 3개(좌/중/우). 중간 창 높이 0~2m, 좌우 창 높이 1.2~2m.
    - 가로 길이는 황금비(가로:세로 ≈ 1.618)를 추구하되, 공간에 맞춰 폭 또는 간격을 조정.
    """

    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    apt_elevation_width = 40
    apt_floor_height = 3
    apt_floor_count = 10
    apt_elevation_polygon = Polygon(
        [
            (0, 0),
            (apt_elevation_width, 0),
            (apt_elevation_width, apt_floor_height * apt_floor_count),
            (0, apt_floor_height * apt_floor_count),
        ]
    )
    window_polygons = task(apt_elevation_width, apt_floor_count, apt_floor_height)

    show_polygons([apt_elevation_polygon] + window_polygons)
