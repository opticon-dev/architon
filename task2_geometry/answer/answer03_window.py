from typing import List, Tuple
from shapely.geometry import Polygon


def _compute_unit_window_layout(
    unit_left_x: float,
    unit_right_x: float,
    mid_height: float,
    side_height: float,
    margin: float = 1.0,
    min_gap: float = 1.0,
) -> List[Tuple[float, float]]:
    """
    한 세대(unit) 구간 내에서 3베이 창문의 가로 배치를 계산한다.

    반환: [(lx0,lx1), (mx0,mx1), (rx0,rx1)]  (모두 단위 m)
    실제 Y 구간은 층별 규칙에 따라 외부에서 적용한다.

    규칙:
    - 중간 창: 높이 2.0m, 좌/우 창: 높이 0.8m(1.2~2.0m 구간)를 가정
    - 가로:세로 ≈ 1.618(황금비) 기반 기본 폭 산정
    - 세대 경계에서 1m 마진, 창 사이 최소 1m 간격 보장
    - 공간 부족 시 창문 폭을 동일 비율로 스케일 다운, 간격은 최소 유지
    """

    phi = 1.61803398875
    unit_width = max(0.0, unit_right_x - unit_left_x)
    inner_width = max(0.0, unit_width - 2.0 * margin)

    # 창문 기본 가로 폭(황금비)
    w_mid_base = phi * mid_height
    w_side_base = phi * side_height
    base_total = w_mid_base + 2.0 * w_side_base

    # 최소 간격 2개 확보 후 남는 폭
    available_for_windows = inner_width - 2.0 * min_gap

    if available_for_windows <= 0.0:
        return []

    if base_total <= available_for_windows + 1e-9:
        # 기본 폭이 들어가면, 남는 폭은 간격으로 균등 분배
        w_mid = w_mid_base
        w_side = w_side_base
        extra = available_for_windows - base_total
        gap = min_gap + 0.5 * extra  # 양쪽 간격에 동일 배분
    else:
        # 기본 폭이 너무 크면 폭을 축소, 간격은 최소값 유지
        scale = max(0.0, available_for_windows / base_total)
        w_mid = w_mid_base * scale
        w_side = w_side_base * scale
        gap = min_gap

    # 좌측 마진
    x = unit_left_x + margin
    left_x0, left_x1 = x, x + w_side
    x = left_x1 + gap
    mid_x0, mid_x1 = x, x + w_mid
    x = mid_x1 + gap
    right_x0, right_x1 = x, x + w_side

    # 우측 마진 보장(정밀도 보정은 생략)
    if right_x1 > unit_right_x - margin + 1e-6:
        # 아주 드물게 반올림 문제로 초과할 경우, 우측에서 살짝 당겨 정렬
        delta = right_x1 - (unit_right_x - margin)
        left_x0 -= delta
        left_x1 -= delta
        mid_x0 -= delta
        mid_x1 -= delta
        right_x0 -= delta
        right_x1 -= delta

    return [
        ((left_x0, left_x1)),
        ((mid_x0, mid_x1)),
        ((right_x0, right_x1)),
    ]


def task(
    apt_elevation_width: float,
    apt_floor_count: int,
    apt_floor_height: float = 3.0,
) -> List[Polygon]:
    """
    아파트 정면 입면에서 층/세대 기준에 맞추어 3베이 창문(층별 3개)을 배치한다.

    규칙 요약:
    - 층고: 3m, 층 수에 따라 층 분리
    - 세대 폭: 최소 10m 기준으로 균등 분할
    - 창 배치: 세대 경계 1m 마진, 창 사이 최소 1m 간격
    - 창 개수: 3개(좌/중/우). 중간 창 높이 0~2m, 좌/우 창 높이 1.2~2m
    - 가로 길이: 황금비 기반 기본 폭, 공간에 맞춰 폭/간격 조정
    """

    if apt_elevation_width <= 0 or apt_floor_count <= 0 or apt_floor_height <= 0:
        return []

    # 세대 수: 최소 10m 기준으로 균등 분할
    num_units = max(1, int(apt_elevation_width // 10.0))
    unit_width = apt_elevation_width / num_units

    windows: List[Polygon] = []

    for f in range(apt_floor_count):
        floor_y0 = f * apt_floor_height
        # 세로 높이 설정
        mid_y0, mid_y1 = floor_y0 + 0.0, floor_y0 + 2.0
        side_y0, side_y1 = floor_y0 + 1.2, floor_y0 + 2.0

        for u in range(num_units):
            unit_left_x = u * unit_width
            unit_right_x = (u + 1) * unit_width

            layout = _compute_unit_window_layout(
                unit_left_x=unit_left_x,
                unit_right_x=unit_right_x,
                mid_height=(mid_y1 - mid_y0),
                side_height=(side_y1 - side_y0),
                margin=1.0,
                min_gap=1.0,
            )

            if not layout:
                continue

            # 좌/중/우 창문 생성
            (lx0, lx1), (mx0, mx1), (rx0, rx1) = layout
            windows.append(
                Polygon(
                    [(lx0, side_y0), (lx1, side_y0), (lx1, side_y1), (lx0, side_y1)]
                )
            )
            windows.append(
                Polygon([(mx0, mid_y0), (mx1, mid_y0), (mx1, mid_y1), (mx0, mid_y1)])
            )
            windows.append(
                Polygon(
                    [(rx0, side_y0), (rx1, side_y0), (rx1, side_y1), (rx0, side_y1)]
                )
            )

    return windows


if __name__ == "__main__":
    # 간단 실행 예제
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

    from utils._viauslize_utils import show_polygons

    show_polygons([apt_elevation_polygon] + window_polygons)
