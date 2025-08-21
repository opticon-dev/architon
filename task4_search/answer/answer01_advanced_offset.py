import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import os
from datetime import datetime


### task 함수 정의 ###
def offset_polygon(polygon, distances):

    # 1. 반시계방향 확인 및 변환
    coords = list(polygon.exterior.coords)[:-1]
    area = sum(
        (
            coords[i][0] * coords[(i + 1) % len(coords)][1]
            - coords[(i + 1) % len(coords)][0] * coords[i][1]
        )
        for i in range(len(coords))
    )
    if area < 0:  # 시계방향이면 뒤집기
        coords = coords[::-1]

    # 2. 엣지 추출
    edges = [(coords[i], coords[(i + 1) % len(coords)]) for i in range(len(coords))]

    # 3-6. 각 엣지를 오프셋하고 연장
    offset_lines = []
    for i, (p1, p2) in enumerate(edges):
        # 4. 오프셋 계산
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = np.sqrt(dx**2 + dy**2)
        nx, ny = -dy / length, dx / length  # 수직벡터 (반시계방향 기준 왼쪽)

        d = abs(distances[i])
        offset_p1 = (p1[0] + nx * d, p1[1] + ny * d)
        offset_p2 = (p2[0] + nx * d, p2[1] + ny * d)

        # 5. 양끝을 100만큼 연장
        dir_x, dir_y = dx / length, dy / length
        extend_p1 = (offset_p1[0] - dir_x * 100, offset_p1[1] - dir_y * 100)
        extend_p2 = (offset_p2[0] + dir_x * 100, offset_p2[1] + dir_y * 100)

        # 6. 연장된 선분 저장
        offset_lines.append(LineString([extend_p1, extend_p2]))

    # 7-8. 연속된 선분들의 교차점 찾기
    intersections = []
    for i in range(len(offset_lines)):
        line1 = offset_lines[i - 1]  # i-1 (마지막일 때는 -1이므로 자동으로 마지막 요소)
        line2 = offset_lines[i]  # i

        # 8. 교차점 계산
        try:
            point = line1.intersection(line2)
            if hasattr(point, "x"):
                intersections.append((point.x, point.y))
        except:
            pass

    # 9. 교차점으로 폴리라인 생성
    return Polygon(intersections) if len(intersections) >= 3 else polygon


### 시각화 함수 정의 ###
def visualize(original, new, distances):
    fig, ax = plt.subplots(figsize=(10, 8))

    # 원본 (회색)
    x1, y1 = original.exterior.xy
    ax.fill(x1, y1, "lightgray", alpha=0.7, label="Original")
    ax.plot(x1, y1, "gray", linewidth=2)

    # 새로운 폴리곤 (빨간색)
    x2, y2 = new.exterior.xy
    ax.fill(x2, y2, "red", alpha=0.5, label="Offset")
    ax.plot(x2, y2, "darkred", linewidth=2)

    # 거리 표시
    coords = list(original.exterior.coords)[:-1]
    for i, d in enumerate(distances):
        p1, p2 = coords[i], coords[(i + 1) % len(coords)]
        mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        ax.text(
            mid[0],
            mid[1],
            f"{d:.2f}",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()

    # 저장
    os.makedirs(f"task4_search/output/task01", exist_ok=True)
    plt.savefig(f"task4_search/output/task01/offset.png", dpi=300, bbox_inches="tight")
    plt.show()


### 실행 ###
if __name__ == "__main__":
    # 테스트 1: 랜덤 폴리곤
    angles = np.sort(np.random.uniform(0, 2 * np.pi, 6))
    points = [
        (np.random.uniform(2, 5) * np.cos(a), np.random.uniform(2, 5) * np.sin(a))
        for a in angles
    ]
    poly = Polygon(points)
    distances = [np.random.uniform(0.1, 1.0) for _ in range(len(points))]
    new_poly = offset_polygon(poly, distances)
    visualize(poly, new_poly, distances)

    # 테스트 2: 사각형
    square = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    sq_distances = [0.5, 0.3, 0.8, 0.4]
    new_square = offset_polygon(square, sq_distances)
    visualize(square, new_square, sq_distances)
