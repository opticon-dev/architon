from shapely.geometry import Polygon
from typing import List


def task(parking_lot_boundary: Polygon) -> List[Polygon]:
    """
    주어진 주차장 경계에 따라 주차장 cell을 생성합니다.

    Args:
        parking_lot_boundary (Polygon): 주차장 경계

    Returns:
        List[Polygon]: 주차장 cell의 리스트
    """
    parking_cells = []
    cell_width = 2.5
    cell_height = 5.0
    lane_width = 6.0

    min_x, min_y, max_x, max_y = parking_lot_boundary.bounds

    # 외곽 주차 cell 생성
    x = min_x
    while x + cell_width <= max_x:
        parking_cells.append(
            Polygon(
                [
                    (x, min_y),
                    (x + cell_width, min_y),
                    (x + cell_width, min_y + cell_height),
                    (x, min_y + cell_height),
                ]
            )
        )
        x += cell_width

    # 내측 주차 cell 생성
    y = min_y + cell_height + lane_width
    while y + cell_height <= max_y:
        x = min_x
        while x + cell_width <= max_x:
            parking_cells.append(
                Polygon(
                    [
                        (x, y),
                        (x + cell_width, y),
                        (x + cell_width, y + cell_height),
                        (x, y + cell_height),
                    ]
                )
            )
            x += cell_width
        y += cell_height + lane_width

    return parking_cells


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
    from utils import show_polygons

    show_polygons(parking_lot_boundary, *parking_cells)
