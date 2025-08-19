import random
import math
import time
import matplotlib.pyplot as plt
from task4_search.optimization.opt_genetic_algorithm import GeneticAlgorithm  

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
    x_points = [min_x + i * resolution for i in range(int((max_x - min_x) / resolution) + 1)]
    y_points = [min_y + i * resolution for i in range(int((max_y - min_y) / resolution) + 1)]
    grid_points = [(x, y) for x in x_points for y in y_points]
    return grid_points

# 원의 면적 계산
def calculate_area(radius):
    return math.pi * radius ** 2

# 가장 먼 점을 찾아 원 생성
def create_circle(center, points):
    distances = [math.hypot(center[0] - pt[0], center[1] - pt[1]) for pt in points]
    radius = max(distances)
    area = calculate_area(radius)
    return radius, area

# 점들에 대해 전수조사 방식으로 최소 원을 찾는 함수
def find_minimum_bounding_circle(points, resolution=1.0):
    bounds = create_bounding_box(points)
    grid_points = generate_grid_points(bounds, resolution)
    
    best_radius = float('inf')
    best_area = float('inf')
    best_center = None
    
    # 각 그리드 점에 대해 전수조사 수행
    for center in grid_points:
        radius, area = create_circle(center, points)
        
        if area < best_area:  # 가장 작은 면적의 원을 선택
            best_radius = radius
            best_area = area
            best_center = center

    return best_center, best_radius

# 시각화 함수
def visualize_comparison(points, ga_center, ga_radius, rule_center, rule_radius, ga_time, rule_time, ga_area, rule_area):
    # 그래프 크기를 조정하여 텍스트를 위한 공간 확보
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal', 'box')

    # 점들 표시
    ax.scatter(*zip(*points), color='blue', label="Points")

    # 유전 알고리즘 결과 (파란 원)
    ga_circle = plt.Circle(ga_center, ga_radius, color='blue', fill=False, linewidth=2, label="GA Circle")
    ax.add_artist(ga_circle)

    # 규칙 기반 결과 (빨간 원)
    rule_circle = plt.Circle(rule_center, rule_radius, color='red', fill=False, linewidth=2, label="Rule-based Circle")
    ax.add_artist(rule_circle)

    # 원의 중심점 표시
    ax.scatter(*ga_center, color='blue', zorder=5)  # GA 중심점 (파란색)
    ax.scatter(*rule_center, color='red', zorder=5)  # Rule-based 중심점 (빨간색)

    # 그래프 설정
    plt.xlim(min(x for x, _ in points) - 10, max(x for x, _ in points) + 10)
    plt.ylim(min(y for _, y in points) - 10, max(y for _, y in points) + 10)
    plt.legend()
    plt.title("GA vs Rule-based Minimum Bounding Circles")
    
    # 텍스트를 그래프 영역 밖에 표시 (전체 figure 좌표계 사용)
    fig.text(0.02, 0.95, f"GA Time: {ga_time:.4f}s", fontsize=12, verticalalignment="top", 
             bbox=dict(facecolor='lightblue', alpha=0.8, edgecolor='blue'))
    fig.text(0.02, 0.90, f"Rule-based Time: {rule_time:.4f}s", fontsize=12, verticalalignment="top", 
             bbox=dict(facecolor='lightcoral', alpha=0.8, edgecolor='red'))
    fig.text(0.02, 0.85, f"GA Area: {ga_area:.4f}", fontsize=12, verticalalignment="top", 
             bbox=dict(facecolor='lightblue', alpha=0.8, edgecolor='blue'))
    fig.text(0.02, 0.80, f"Rule-based Area: {rule_area:.4f}", fontsize=12, verticalalignment="top", 
             bbox=dict(facecolor='lightcoral', alpha=0.8, edgecolor='red'))
    
    # 그래프와 텍스트 사이에 여백 추가
    plt.tight_layout()
    plt.show()

# 설정 및 실행
bounds = (0, 60, 0, 60)  # x, y 좌표 범위
num_points = 20  # 점의 수
resolution = 1.0  # 그리드 해상도
points = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[2], bounds[3])) for _ in range(num_points)]

# 유전 알고리즘 실행
ga_start_time = time.time()
ga = GeneticAlgorithm(population_size=100, generations=50, crossover_rate=0.6, mutation_rate=0.05, bounds=bounds, points=points)
ga_center, ga_radius = ga.run()[0], max([math.hypot(ga.run()[0][0] - pt[0], ga.run()[0][1] - pt[1]) for pt in points])
ga_end_time = time.time()
ga_time = ga_end_time - ga_start_time
ga_area = math.pi * ga_radius**2

# 규칙 기반 방법 실행
rule_start_time = time.time()
rule_center, rule_radius = find_minimum_bounding_circle(points, resolution)
rule_end_time = time.time()
rule_time = rule_end_time - rule_start_time
rule_area = math.pi * rule_radius**2

# 결과 출력
print(f"GA Method Time: {ga_time:.4f} seconds, Area: {ga_area:.4f}")
print(f"Rule-based Method Time: {rule_time:.4f} seconds, Area: {rule_area:.4f}")

# 시각화
visualize_comparison(points, ga_center, ga_radius, rule_center, rule_radius, ga_time, rule_time, ga_area, rule_area)
