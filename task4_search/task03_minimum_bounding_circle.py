import random
import math
import time
import matplotlib.pyplot as plt

"""
TASK:
points를 모두 감싸는 최소 크기의 원을 찾아 원의 중심과 반지름을 리턴하라.
관심이 생긴다면 answer 폴더에 있는 opt_ prefix가 있는 파일들을 확인하라.
Genetic 알고리즘과의 비교도 확인할 수 있다.

환경: Python
입력:
    points(점 좌표 리스트)
    resolution(탐색할 공간의 간격)
출력:
    

"""


### task 함수 정의 ###


# 점들에 대해 전수조사 방식으로 최소 원을 찾는 함수
def task(points, resolution=1.0):
    """
    points를 모두 감싸는 최소 크기의 원을 찾아 원의 중심과 반지름을 리턴하라.

    hint :
    이 원의 중심은 points의 bounding box 안에 있을 수 밖에 없다.(상식)


    Args:
        points : 점 좌표 리스트
        resolution : 탐색할 공간의 간격

    """
    raise NotImplementedError


# 시각화 함수
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
    plt.title("GA vs Rule-based Minimum Bounding Circles")

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
