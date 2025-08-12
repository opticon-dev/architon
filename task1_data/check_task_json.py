# 검증 함수 (한 줄 출력 + 분류 정확도 체크)

friend_submission = {"total_price": 17490989}


def verify_submission(submitted_dict):
    correct_total = 17490989.0
    submitted_total = submitted_dict.get("total_price")
    if submitted_total is None:
        print("총 비용 값이 제출되지 않았습니다.")
        return False
    # 정수 비교로 오차 허용
    if int(submitted_total) == int(correct_total):
        print(True)
        return True
    else:
        print(False)
        return False


verify_submission(friend_submission)
