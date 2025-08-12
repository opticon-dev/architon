# 검증 코드 (한 줄 출력 + 분류 정확도 체크)
import pandas as pd


# 정답 CSV 경로
CORRECT_PATH = r"task1_data\check\버스혼잡도_solution.csv"
# 답안 CSV 경로
ANSWER_PATH = r"task1_data\output\버스혼잡도_answer.csv"


def verify_csv_submission(ANSWER_PATH):
    df_answer = pd.read_csv(ANSWER_PATH)
    df_correct = pd.read_csv(CORRECT_PATH)

    # 컬럼 순서 정렬, 인덱스 초기화
    df_answer = df_answer[df_correct.columns]
    df_answer = df_answer.reset_index(drop=True)
    df_correct = df_correct.reset_index(drop=True)

    is_correct = df_answer.equals(df_correct)
    print(f"정답여부 : {is_correct}")
