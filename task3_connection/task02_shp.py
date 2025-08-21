from typing import List
from shapely.geometry import LineString, MultiLineString

"""
TASK: input 폴더에 있는 SHP 파일을 geopandas를 사용해 읽어 등고(콘투어)선을 matplotlib로 시각화한다.

환경: python shapely, geopandas
입력: SHP 파일 경로(str)
출력:  List[shapely.geometry.LineString](등고선 목록)

요구사항:
1. SHP 파일의 feature 중 라인(등고선)만 추출한다. MultiLineString은 개별 LineString으로 분리한다.
2. 좌표계는 그대로 사용한다. 별도의 reprojection은 하지 않는다.
3. 시각화는 utils의 show_linestrings를 사용한다.

샘플 데이터:
  input/*.shp (예시)
  output/task02_shp_output.png
"""


### task 함수 정의 ###
def task(shp_path: str) -> List[LineString]:
    """
    Args:
        shp_path (str): 입력 SHP 파일 경로

    Returns:
        List[LineString]: 등고선 LineString 리스트

    주의:
    - MultiLineString은 호출자가 아닌 내부에서 개별 LineString으로 분해하여 반환하는 구현을 권장
      (정답 파일 참조). 이 과제 스켈레톤은 타입만 정의한다.
    """
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    # 예시 경로. 실제 파일명을 input 폴더에 맞게 수정해서 사용한다.
    shp_path = "task3_connection/input/N3L_F0010000.shp"

    contours = task(shp_path)
    from utils._viauslize_utils import show_linestrings

    show_linestrings(contours)
