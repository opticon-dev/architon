import random
import math
import matplotlib.pyplot as plt


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


# 점들에 대해 전수조사 방식으로 원을 찾는 함수
def find_bounding_circle(points, resolution=1.0):
    # 바운딩 박스 생성
    bounds = create_bounding_box(points)
    
    # 바운딩 박스 내부에 그리드 포인트 생성
    grid_points = generate_grid_points(bounds, resolution)
    
    best_radius = float('inf')
    best_area = float('inf')
    best_center = None
    
    # 각 그리드 점에 대해 전수조사 수행
    for center in grid_points:
        radius, area = create_circle(center, points)
        
        # 가장 작은 면적의 원을 선택
        if area < best_area:
            best_radius = radius
            best_area = area
            best_center = center

    return best_center, best_radius


# 시각화 함수
def visualize_bounding_circle(points, center, radius):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.scatter(*zip(*points), color='blue', label="Points")
    circle = plt.Circle(center, radius, color='red', fill=False, linewidth=2)
    ax.add_artist(circle)
    plt.xlim(min(x for x, _ in points) - 10, max(x for x, _ in points) + 10)
    plt.ylim(min(y for _, y in points) - 10, max(y for _, y in points) + 10)
    plt.legend()
    plt.title("Bounding Circle with Minimum Area")
    plt.show()


# 설정 및 실행
bounds = (0, 100, 0, 100)  # x, y 좌표 범위
num_points = 30  # 점의 수
resolution = 1.0  # 그리드 해상도 (작을수록 더 많은 포인트)
points = [(random.uniform(bounds[0], bounds[1]), random.uniform(bounds[2], bounds[3])) for _ in range(num_points)]

# 전수조사 방식으로 최적의 원을 찾기
center, radius = find_bounding_circle(points, resolution)

# 결과 시각화
visualize_bounding_circle(points, center, radius)
