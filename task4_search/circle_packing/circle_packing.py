import random
import os
import json
import matplotlib.pyplot as plt
import imageio
from datetime import datetime


MAX_ITER = 500
ALPHA = 0.1
NUM_POINTS = 100
RADIUS_RANGE = (1, 3)
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')

def create_output_folder():
    """결과 저장 폴더 생성"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join(RESULTS_FOLDER, timestamp)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def save_iteration(folder, iteration, points, radii):
    """반복 결과 저장"""
    # JSON 저장
    with open(os.path.join(folder, f'data_{iteration}.json'), 'w') as f:
        json.dump({"points": points, "radii": radii}, f)
    
    # 이미지 저장
    plt.figure(figsize=(8, 8))
    for pt, rad in zip(points, radii):
        plt.gca().add_artist(plt.Circle(pt, rad, color='blue', alpha=0.6))
    
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().set_aspect('equal')
    plt.title(f'반복 {iteration}')
    plt.savefig(os.path.join(folder, f'iteration_{iteration}.png'), dpi=100, bbox_inches='tight')
    plt.close()

def check_overlap(p1, r1, p2, r2):
    """두 원 겹침 확인"""
    distance = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    return distance < (r1 + r2)

def separate_overlapping_circles(points, radii):
    """겹치는 원들을 분리"""
    moved = False
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if check_overlap(points[i], radii[i], points[j], radii[j]):
                # 방향 벡터 계산
                dx = points[i][0] - points[j][0]
                dy = points[i][1] - points[j][1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance > 0:
                    # 단위 벡터
                    ux, uy = dx/distance, dy/distance
                    move_dist = (radii[i] + radii[j] - distance + ALPHA) / 2
                    
                    # 원들을 밀어내기
                    points[i] = (points[i][0] + ux * move_dist, points[i][1] + uy * move_dist)
                    points[j] = (points[j][0] - ux * move_dist, points[j][1] - uy * move_dist)
                    moved = True
    
    return moved

def main():
    """메인 실행 함수"""
    # 출력 폴더 생성
    output_folder = create_output_folder()
    print(f"결과 저장 위치: {output_folder}")
    
    # 초기 원 생성 (모두 겹치도록)
    center = (50, 50)
    points = []
    radii = []
    
    for _ in range(NUM_POINTS):
        radius = random.uniform(*RADIUS_RANGE)
        radii.append(radius)
        # 반지름의 절반 이내에서 랜덤 위치
        offset = (random.uniform(-radius/2, radius/2), random.uniform(-radius/2, radius/2))
        points.append((center[0] + offset[0], center[1] + offset[1]))
    
    # GIF 생성
    gif_path = os.path.join(output_folder, 'animation.gif')
    gif_writer = imageio.get_writer(gif_path, duration=0.2)
    
    # 메인 알고리즘
    for iteration in range(MAX_ITER):
        # 현재 상태 저장
        save_iteration(output_folder, iteration, points, radii)
        
        # GIF에 추가
        image_path = os.path.join(output_folder, f'iteration_{iteration}.png')
        gif_writer.append_data(imageio.imread(image_path))
        
        # 겹치는 원들 분리
        if not separate_overlapping_circles(points, radii):
            print(f"수렴 완료: {iteration}번째 반복")
            break
    
    gif_writer.close()
    print("처리 완료!")

if __name__ == "__main__":
    main()
