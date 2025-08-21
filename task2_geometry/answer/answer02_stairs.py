from typing import List
import math
from shapely.geometry import Polygon
from utils import show_polygons, show_polygons_Z


def _range_penalty(value: float, low: float, high: float) -> float:
    """값이 [low, high] 범위를 벗어나는 정도를 반환한다. 범위 내면 0."""

    # 값이 허용 범위를 벗어나면 초과/미달분만큼 패널티를 준다.
    if value < low:
        return low - value
    if value > high:
        return value - high
    return 0.0


def get_polygon(idx: int, rise: float, tread: float, width: float) -> Polygon:
    """i번째 단의 상판을 나타내는 3D Polygon을 생성한다.

    좌표계/단위: X=수평 진행(m), Y=계단 폭(m), Z=상판 고도(m)
    """
    z_top = (idx + 1) * rise
    x0 = idx * tread
    x1 = (idx + 1) * tread
    y0 = 0.0
    y1 = width

    # 3D Polygon: 꼭짓점 좌표에 Z 포함
    return Polygon(
        [
            (x0, y0, z_top),
            (x1, y0, z_top),
            (x1, y1, z_top),
            (x0, y1, z_top),
        ]
    )


def task(
    total_dist: float,
    total_height: float,
) -> List[Polygon]:
    """
    계단의 총 수평거리와 총 높이를 입력으로 받아, 각 단의 상판을 3D Polygon(Z)으로 반환한다.

    설계 규칙(경험적):
    - 단높이(라이트) r: 0.14m ~ 0.18m 권장
    - 단폭(디딤폭) t: 0.25m ~ 0.32m 권장

    편의 가정:
    - 계단 폭(Y 방향)은 1.0m로 고정한다.
    - 각 단의 상판은 X 방향으로 연속한 직사각형으로 모델링한다.
    - i번째 단의 상판 Z 값은 (i+1) * r 로 둔다. (상판 상면의 높이 표현)

    Args:
            total_dist (float): 계단 총 수평거리(m)
            total_height (float): 계단 총 높이(m)

    Returns:
            List[Polygon]: 각 단의 상판을 나타내는 3D Polygon(Z) 리스트
    """

    # 기본 검증
    if total_dist <= 0 or total_height <= 0:
        raise ValueError("total_dist와 total_height는 양수여야 한다.")

    # 설계 목표 범위
    preferred_riser_min, preferred_riser_max = 0.14, 0.18
    preferred_tread_min, preferred_tread_max = 0.25, 0.32
    preferred_stride = 0.63  # 2r + t ≈ 0.63m

    # 후보 단수 범위(라이트 기준으로 가능한 범위 산정)
    min_steps = max(1, math.floor(total_height / preferred_riser_max))
    max_steps = max(1, math.ceil(total_height / preferred_riser_min))
    if min_steps > max_steps:
        min_steps, max_steps = max_steps, min_steps

    # 후보 단수 중 패널티 최소화 기준으로 선택
    best_step_count = None
    best_penalty = float("inf")
    for step_count in range(min_steps, max_steps + 1):
        # 각 후보에서의 실제 r, t
        riser = total_height / step_count
        tread = total_dist / step_count

        penalty_rise = _range_penalty(riser, preferred_riser_min, preferred_riser_max)
        penalty_tread = _range_penalty(tread, preferred_tread_min, preferred_tread_max)
        penalty_stride = abs(2 * riser + tread - preferred_stride)

        # 가중 합 패널티 (보폭식에 조금 더 가중치)
        penalty = 2.0 * penalty_rise + 2.0 * penalty_tread + 3.0 * penalty_stride

        if penalty < best_penalty:
            best_penalty = penalty
            best_step_count = step_count

    # 혹시라도 위 루프에서 선택이 안 되면, 합리적 기본값으로 설정
    if best_step_count is None:
        best_step_count = max(1, round(total_height / 0.16))

    # 최종 r, t 확정
    final_rise = total_height / best_step_count
    final_tread = total_dist / best_step_count

    # 계단 폭(Y 방향) 가정
    stair_width = 1.0

    # 각 단의 상판(3D Polygon) 생성
    polygons: List[Polygon] = []
    for i in range(best_step_count):
        polygon = get_polygon(i, final_rise, final_tread, stair_width)
        polygons.append(polygon)

    return polygons


if __name__ == "__main__":
    # 간단 실행 예제
    # 총 수평 10m, 총 높이 3m인 직선 계단의 상판을 생성한다.
    stairs = task(10.0, 3.0)

    # 2D 상(top view)으로 확인 (Z는 무시됨)
    show_polygons_Z(stairs)
