import math

# 검증 함수 (한 줄 출력 + 분류 정확도 체크)


def verify_json_submission(submitted_price):
    correct_total = 17490989.0

    if submitted_price is None:
        print("총 비용 값이 제출되지 않았습니다.")

    # 정수 비교로 오차 허용
    is_correct = math.isclose(submitted_price, correct_total, rel_tol=1e-9)
    print(f"정답 여부 : {is_correct}")
