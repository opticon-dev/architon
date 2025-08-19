import random
import os
import json
import matplotlib.pyplot as plt
import imageio

"""
TASK:
주어진 중심점을 기준으로, 지정된 반지름 범위 내에서 원이 반복하여 만들어진다.
각 반복 단계의 상태를 이미지로 저장하고, 최종적으로 GIF로 저장된다.

환경: Python
입력:
    points(원 중심 좌표 리스트)
    radii(각 원의 반지름 리스트)
출력:
    iteration_{iteration}.png
    animation.gif
    ("output/task02"에 저장)

"""


MAX_ITER = 500  # 최대 반복횟수
ALPHA = 0.1  # ALPHA = 증가율
NUM_POINTS = 100  # 생성할 원의 개수
RADIUS_RANGE = (1, 3)  # 원의 반지름 범위
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "output/task02")


### 폴더 형성 및 반복 저장 함수 정의 ###
def create_output_folder():
    output_folder = os.path.join(RESULTS_FOLDER)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


def save_iteration(folder, iteration, points, radii):
    # JSON 저장
    with open(os.path.join(folder, f"data_{iteration}.json"), "w") as f:
        json.dump({"points": points, "radii": radii}, f)

    # 이미지 저장
    plt.figure(figsize=(8, 8))
    for pt, rad in zip(points, radii):
        plt.gca().add_artist(
            plt.Circle(pt, rad, color="blue", alpha=0.6)
        )  # alpha = 투명도

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().set_aspect("equal")
    plt.title(f"반복 {iteration}")
    plt.savefig(
        os.path.join(folder, f"iteration_{iteration}.png"), dpi=100, bbox_inches="tight"
    )
    plt.close()


### task 함수 정의 ###
def task(points, radii):
    """
    아래에서 task가 실행되는 환경을 이해하고 이를 기반으로
    이터레이션 되는 하나의 액션을 구현하면 된다.
    이 TASK 내에서는 원들의 겹침 여부를 확인하고 반대방향으로 밀어낸다.
    모든 원이 겹치지 않으면 FALSE를
    하나라도 겹치면 TRUE를 리턴하라.

    Args:
        points : 원 중심 좌표 리스트
        radii : 각 원의 반지름 리스트

    - 생성된 원들 사이에서 겹침 여부를 확인한다.
    - 겹치는 원이 있으면 서로 밀어내어 분리한다.
    """
    raise NotImplementedError


### 실행 함수 정의 ###
def main():
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
        offset = (
            random.uniform(-radius / 2, radius / 2),
            random.uniform(-radius / 2, radius / 2),
        )
        points.append((center[0] + offset[0], center[1] + offset[1]))

    # GIF 생성
    gif_path = os.path.join(output_folder, "animation.gif")
    gif_writer = imageio.get_writer(gif_path, duration=0.2)

    # 메인 알고리즘
    for iteration in range(MAX_ITER):
        # 현재 상태 저장
        save_iteration(output_folder, iteration, points, radii)

        # GIF에 추가
        image_path = os.path.join(output_folder, f"iteration_{iteration}.png")
        gif_writer.append_data(imageio.imread(image_path))

        # 겹치는 원들 분리
        task(points, radii)

    gif_writer.close()


### 실행 ###
if __name__ == "__main__":
    main()
