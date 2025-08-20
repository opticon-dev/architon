import random
import math
import time
import matplotlib.pyplot as plt

"""
TASK:
points를 모두 감싸는 최소 크기의 원을 찾아 원의 중심과 반지름을 리턴한다.

자세한 내용은 answer 폴더에 있는 opt_ prefix가 있는 파일에 있으며,
Genetic 알고리즘과의 비교 가능하다.


환경: Python
입력:
    points(점 좌표 리스트)
    resolution(탐색할 공간의 간격)
출력:

"""


### task 함수 정의 ###
# 바운딩 박스 생성 함수
def create_bounding_box(points):
    x_coords = [pt[0] for pt in points]
    y_coords = [pt[1] for pt in points]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    return min_x, max_x, min_y, max_y


# 그리드 포인트 생성 함수
def generate_grid_points(bounds, resolution):
    min_x, max_x, min_y, max_y = bounds
    x_points = [
        min_x + i * resolution for i in range(int((max_x - min_x) / resolution) + 1)
    ]
    y_points = [
        min_y + i * resolution for i in range(int((max_y - min_y) / resolution) + 1)
    ]
    grid_points = [(x, y) for x in x_points for y in y_points]
    return grid_points


# 원의 면적 계산
def calculate_area(radius):
    return math.pi * radius**2


# 가장 먼 점을 찾아 원 생성
def create_circle(center, points):
    distances = [math.hypot(center[0] - pt[0], center[1] - pt[1]) for pt in points]
    radius = max(distances)
    area = calculate_area(radius)
    return radius, area


# 점들에 대해 전수조사 방식으로 최소 원을 찾는 함수
def task(points, resolution=1.0):
    bounds = create_bounding_box(points)
    grid_points = generate_grid_points(bounds, resolution)

    best_radius = float("inf")
    best_area = float("inf")
    best_center = None

    # 각 그리드 점에 대해 전수조사 수행
    for center in grid_points:
        radius, area = create_circle(center, points)

        if area < best_area:  # 가장 작은 면적의 원을 선택
            best_radius = radius
            best_area = area
            best_center = center

    return best_center, best_radius


### 시각화 함수 정의 ###
def visualize_result(
    points,
    rule_center,
    rule_radius,
    rule_time,
    rule_area,
):
    # 그래프 크기를 조정하여 텍스트를 위한 공간 확보
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect("equal", "box")

    # 점들 표시
    ax.scatter(*zip(*points), color="blue", label="Points")

    # 규칙 기반 결과 (빨간 원)
    rule_circle = plt.Circle(
        rule_center,
        rule_radius,
        color="red",
        fill=False,
        linewidth=2,
        label="Rule-based Circle",
    )
    ax.add_artist(rule_circle)

    # 원의 중심점 표시
    ax.scatter(*rule_center, color="red", zorder=5)  # Rule-based 중심점 (빨간색)

    # 그래프 설정
    plt.xlim(min(x for x, _ in points) - 10, max(x for x, _ in points) + 10)
    plt.ylim(min(y for _, y in points) - 10, max(y for _, y in points) + 10)
    plt.legend()
    plt.title("Rule-based Minimum Bounding Circles")

    fig.text(
        0.02,
        0.90,
        f"Rule-based Time: {rule_time:.4f}s",
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="lightcoral", alpha=0.8, edgecolor="red"),
    )

    fig.text(
        0.02,
        0.80,
        f"Rule-based Area: {rule_area:.4f}",
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="lightcoral", alpha=0.8, edgecolor="red"),
    )

    # 그래프와 텍스트 사이에 여백 추가
    plt.tight_layout()
    plt.show()


### 실행 함수 정의 ###
def main():

    # 설정 및 실행
    bounds = (0, 60, 0, 60)  # x, y 좌표 범위
    num_points = 20  # 점의 수
    resolution = 1.0  # 그리드 해상도
    points = [
        (random.uniform(bounds[0], bounds[1]), random.uniform(bounds[2], bounds[3]))
        for _ in range(num_points)
    ]

    # 규칙 기반 방법 실행
    rule_start_time = time.time()
    rule_center, rule_radius = task(points, resolution)
    rule_end_time = time.time()
    rule_time = rule_end_time - rule_start_time
    rule_area = math.pi * rule_radius**2

    # 결과 출력
    print(f"Rule-based Method Time: {rule_time:.4f} seconds, Area: {rule_area:.4f}")

    # 시각화
    visualize_result(
        points,
        rule_center,
        rule_radius,
        rule_time,
        rule_area,
    )


### 실행 ###
if __name__ == "__main__":
    main()
