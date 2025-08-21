from typing import List
from shapely.geometry import Polygon, LineString
import numpy as np

# 전역 규격: 주차 셀 가로(주행 방향) 2.5m, 세로(진입 깊이) 5.0m, 차선 6.0m
CELL_WIDTH = 2.5
CELL_DEPTH = 5.0
LANE_WIDTH = 6.0


def explode_polygon(polygon: Polygon) -> List[LineString]:

    coords = list(polygon.exterior.coords)
    lines = []
    for i in range(len(coords) - 1):
        lines.append(LineString([coords[i], coords[(i + 1)]]))
    return lines


def create_parking_cells_from_parallel_lines(
    line1: LineString, line2: LineString
) -> List[Polygon]:
    # line의 방향을 확인하고
    # line의 시작점과 끝점을 비교해 주차가 생길 수 있는 구간을 파악한다.
    # 그 구간을 2.5로 나누어서 포인트를 만들고, 그 포인트를 활용해서 주차칸을 만든다.

    # 가정: line1, line2는 서로 평행하며 축에 정렬된 직선(수평 또는 수직)이다.
    (x1a, y1a), (x1b, y1b) = list(line1.coords)[0], list(line1.coords)[-1]
    (x2a, y2a), (x2b, y2b) = list(line2.coords)[0], list(line2.coords)[-1]

    cells: List[Polygon] = []

    # 수평선 처리
    if abs(y1a - y1b) < 1e-9 and abs(y2a - y2b) < 1e-9:
        y_low = min(y1a, y2a)
        y_high = max(y1a, y2a)
        x_min = max(min(x1a, x1b), min(x2a, x2b))
        x_max = min(max(x1a, x1b), max(x2a, x2b))

        x_start = x_min
        x_end = x_max
        x_current = x_start
        while x_current + CELL_WIDTH <= x_end + 1e-9:
            cells.append(
                Polygon(
                    [
                        (x_current, y_low),
                        (x_current + CELL_WIDTH, y_low),
                        (x_current + CELL_WIDTH, y_high),
                        (x_current, y_high),
                    ]
                )
            )
            x_current += CELL_WIDTH
        return cells

    # 수직선 처리
    if abs(x1a - x1b) < 1e-9 and abs(x2a - x2b) < 1e-9:
        x_low = min(x1a, x2a)
        x_high = max(x1a, x2a)
        y_min = max(min(y1a, y1b), min(y2a, y2b))
        y_max = min(max(y1a, y1b), max(y2a, y2b))

        y_start = y_min
        y_end = y_max
        y = y_start
        while y + CELL_WIDTH <= y_end + 1e-9:
            cells.append(
                Polygon(
                    [
                        (x_low, y),
                        (x_high, y),
                        (x_high, y + CELL_WIDTH),
                        (x_low, y + CELL_WIDTH),
                    ]
                )
            )
            y += CELL_WIDTH
        return cells

    # 그 외의 경우(일반 선분)는 여기서는 지원하지 않는다.
    return cells


def create_round_cells(parking_lot_boundary: Polygon) -> List[Polygon]:
    # 꼭지점을 제외한 위, 아래, 좌, 우 변을 활용해 주차를 만드는 것을 목표로 한다.
    # 1. 내부로 5m offset 한다.
    # 2. 외곽선과 offset한 선을 explode 한 후 각자의 짝을 찾는다.
    # 3. create_parking_cells_from_parallel_lines를 통해 주차장으로 만든다.
    #
    # 단순화: 입력이 직교 사각형이라고 가정하고, bounds를 이용해 4면에 대해 생성한다.
    parking_lot_boundary_offset = parking_lot_boundary.buffer(-5)
    offset_segs = explode_polygon(parking_lot_boundary_offset)
    segs = explode_polygon(parking_lot_boundary)
    cells: List[Polygon] = []
    for seg in segs:
        offset_seg = seg.parallel_offset(5, side="left")
        # 양 끝에서 길이 5m 만큼 자른다.
        pt1 = offset_seg.interpolate(5)
        pt2 = offset_seg.interpolate(seg.length - 5)
        trimmed_offset_seg = LineString([pt1, pt2])

        # 평행하고, 거리가  5 미만인 선이면 주차칸을 만든다.
        cells += create_parking_cells_from_parallel_lines(seg, trimmed_offset_seg)

    return cells


def get_inside_parking_plan(short_len: float) -> List[str]:
    # 모든 차가 접도가 가능한 구성은 다음과 같다.
    # O, OO, OOXO, OOXOO, OOXOOXO 여기서 규칙성을 도출해보면
    # OXO 이 구성이 기본 모듈이다. 이 모듈의 개수를 구하고, 이 좌우에 한대씩을 선택적으로 붙일 수 있다.
    # OXO = 5 + 6 + 5(M) = 17미터이다.
    # OO = 5 + 5 (M) = 10미터이다.
    # 그러므로 짧은방향 길이를 17m로 나눈 값만큼 OXO가 들어가고, 나머지를 5로 나눈 개수 만큼 앞뒤에 붙일 수 있다.
    plan = []
    default_module_length = 17
    deault_module_count = int(short_len // default_module_length)

    additional_module_length = 5
    remain_length = short_len - default_module_length * deault_module_count
    additional_module_count = remain_length // additional_module_length
    plan = "OXO" * deault_module_count
    if additional_module_count == 1:
        plan += "O"
    elif additional_module_count == 2:
        plan = "O" + plan + "O"
    print(plan)
    return plan


def create_inside_cells(parking_lot_boundary: Polygon) -> List[Polygon]:
    # 1. 내부 영역을 구한다. 내부 영역은 외부 영역을 11m 오프셋한 결과다
    # 2. 11m 오프셋한 영역에서 긴 방향과 짧은 방향을 구한다.
    # 3. 짧은 방향의 길이를 재고, 주차 계획을 세운다.
    # 4. 긴방향 선을 주차계획에 맞게 띄워서 만든다.
    # 5. 긴방향선을 create_parking_cells_from_parallel_lines를 통해서 주차장으로 만든다.

    offset_polygon = parking_lot_boundary.buffer(-11)
    segs = explode_polygon(offset_polygon)
    long_length_seg = max(segs, key=lambda x: x.length)
    short_length_seg = min(segs, key=lambda x: x.length)
    print(short_length_seg, short_length_seg.length)
    parking_plan = get_inside_parking_plan(short_length_seg.length)
    parking_cells: List[Polygon] = []
    current_value = 0
    for plan in parking_plan:
        if plan == "O":
            width = 6
            line1 = long_length_seg.parallel_offset(current_value, side="right")
            line2 = long_length_seg.parallel_offset(current_value + width, side="right")
            parking_cells.extend(create_parking_cells_from_parallel_lines(line1, line2))

        elif plan == "X":
            width = 5

        else:
            raise ValueError(f"Invalid parking plan: {plan}")

        current_value += width
    return parking_cells


### task 함수 정의 ###
def task(parking_lot_boundary: Polygon) -> List[Polygon]:
    """
    주어진 주차장 경계에 따라 주차장 cell을 생성합니다.

    Args:
        parking_lot_boundary (Polygon): 주차장 경계

    Returns:
        List[Polygon]: 주차장 cell의 리스트
    """
    # 외곽 주차 cell 생성
    round_cells = create_round_cells(parking_lot_boundary)
    inside_cells = create_inside_cells(parking_lot_boundary)

    return round_cells + inside_cells


### 실행 ###
if __name__ == "__main__":
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
    from utils._viauslize_utils import show_polygons

    show_polygons(parking_lot_boundary, *parking_cells)
