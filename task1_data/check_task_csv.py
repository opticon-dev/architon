# 검증 코드 (한 줄 출력 + 분류 정확도 체크)
import pandas as pd

# 정답 CSV 경로
CORRECT_PATH = r"C:\Users\이정현\Documents\architon\task1_data\output\20250729.csv"
# 답안 CSV 경로
ANSWER_PATH = r"C:\Users\이정현\Documents\architon\task1_data\output\20250708.csv"


def check_csv_task_result(ANSWER_PATH):
    df_answer = pd.read_csv(ANSWER_PATH)
    df_correct = pd.read_csv(CORRECT_PATH)

    # 컬럼 순서 정렬, 인덱스 초기화
    df_answer = df_answer[df_correct.columns]
    df_answer = df_answer.reset_index(drop=True)
    df_correct = df_correct.reset_index(drop=True)

    if df_answer.equals(df_correct):
        print("TRUE")
    else:
        print("FAUSE")


if __name__ == "__main__":
    check_csv_task_result(ANSWER_PATH)
