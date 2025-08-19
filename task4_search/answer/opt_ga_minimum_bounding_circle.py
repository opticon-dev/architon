import random
import math
import matplotlib.pyplot as plt
from task4_search.optimization.opt_genetic_algorithm import GeneticAlgorithm  
# 랜덤 점 생성
def generate_random_points(num_points, bounds):
    min_x, max_x, min_y, max_y = bounds
    return [(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) for _ in range(num_points)]

# 최대 범위 원을 찾는 목적 함수
def objective_function(individual, points):
    # 각 개체 (x, y)에 대해 점들과의 거리를 계산하고, 가장 먼 점과의 거리를 반지름으로 설정
    distances = [math.hypot(individual[0] - pt[0], individual[1] - pt[1]) for pt in points]
    radius = max(distances)
    if radius == 0:
        return float("inf")
    area = math.pi * radius**2
    return 1 / area

# 유전 알고리즘을 이용하여 최적의 원 찾기
def find_bounding_circle(points, bounds, generations=100, population_size=100, crossover_rate=0.7, mutation_rate=0.1):
    ga = GeneticAlgorithm(population_size, generations, crossover_rate, mutation_rate, bounds, points)
    best_individual, best_fitness, best_solutions = ga.run()

    # 최적의 원의 중심과 반지름 계산
    best_x, best_y = best_individual
    distances = [math.hypot(best_x - pt[0], best_y - pt[1]) for pt in points]
    radius = max(distances)
    return (best_x, best_y), radius

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
    plt.title("Minimum Bounding Circle")
    plt.show()

# 설정 및 실행
bounds = (0, 50, 0, 50)  # x, y 좌표 범위
num_points = 30  # 점의 수
points = generate_random_points(num_points, bounds)

# 유전 알고리즘을 이용해 최적의 원을 찾기
center, radius = find_bounding_circle(points, bounds)

# 결과 시각화
visualize_bounding_circle(points, center, radius)
