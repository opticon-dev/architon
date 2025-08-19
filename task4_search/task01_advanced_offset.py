from datetime import datetime
from shapely.geometry import Polygon, LineString
import numpy as np
import matplotlib.pyplot as plt
import os

"""
TASK:
원본 폴리곤을 각 변마다 지정된 거리만큼 오프셋된 새로운 폴리곤을 생성한다.
원본 폴리곤과 오프셋 폴리곤을 시각화하여 .png로 저장한다.


환경: Python
입력: shapely.geometry.Polygon (원본 폴리곤)
     distances (각 변마다 오프셋 거리)


출력:
   offset.png("output/task01"에 저장)
   원본 폴리곤, 새로운 폴리곤의 면적 값

"""


### task 함수 정의 ###
def task(polygon, distances):
    """
    Args:
        polygon : 원본 폴리곤
        distances : 오프셋 거리

    1. 폴리곤의 좌표를 이용해 엣지(선분)들을 추출한다.
    2. 각 엣지를 지정된 거리만큼 오프셋하고 충분히 연장한다.
    3. 연장된 선분 간의 교차점을 찾는다.
    4. 교차점끼리 폴리라인을 형성하여 새로운 폴리곤을 생성한다.
    5. 원본 폴리곤과 새로운 폴리곤의 면적 값을 출력하고 이미지와 GIF로 시각화한다.
    """
    raise NotImplementedError


### 시각화 함수 정의 ###
def visualize(original, new, distances):
    fig, ax = plt.subplots(figsize=(8, 8))

    # 원본 폴리곤 (회색)
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

    os.makedirs(f"output/task01", exist_ok=True)
    plt.savefig(f"output/task01/offset.png", dpi=300, bbox_inches="tight")
    plt.show()


### 실행 ###
if __name__ == "__main__":
    # 테스트 1: 랜덤 폴리곤
    print("=== 랜덤 폴리곤 테스트 ===")
    angles = np.sort(np.random.uniform(0, 2 * np.pi, 6))
    points = [
        (np.random.uniform(2, 5) * np.cos(a), np.random.uniform(2, 5) * np.sin(a))
        for a in angles
    ]
    poly = Polygon(points)
    distances = [np.random.uniform(0.1, 1.0) for _ in range(len(points))]
    new_poly = task(poly, distances)
    visualize(poly, new_poly, distances)

    # 테스트 2: 사각형
    print("\n=== 사각형 테스트 ===")
    square = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    sq_distances = [0.5, 0.3, 0.8, 0.4]
    new_square = task(square, sq_distances)
    visualize(square, new_square, sq_distances)
