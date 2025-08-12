"""
TASK:

1. 버스 혼잡도 데이터 파일을 열어 2025년 07월 29일의 데이터만 추출한다.
2. 추출한 데이터를 정류장 ARS 번호를 기준으로 승객수를 합산한다.
3. 각 정류장의 ARS 번호(ARS_ID)를 기준으로 하여 버스 위치 정보 파일과 결합해 하나의 데이터 프레임을 생성하고, 이를 CSV 형태로 저장한다.

환경: Python
입력: 버스 위치 및 혼잡도 데이터 (제공 데이터)
출력: 20250729_버스혼잡도.csv(output 폴더에 있는 csv 파일)

출력 데이터
    컬럼명 : "버스정류장ARS번호", "역명", "승차총승객수", "하차총승객수", "경도", "위도"
    row  : 01001,종로2가사거리,588,574,1162,37.5698055407,126.9877522923

제공 데이터:
"input/서울시버스정류소위치정보(20250801).xlsx"
"input/BUS_STATION_BOARDING_MONTH_202507.csv"
"""


### task 함수 정의 ###
def task(
    input_path1: str = "input/서울시버스정류소위치정보(20250801).xlsx",
    input_path2: str = "input/BUS_STATION_BOARDING_MONTH_202507.csv",
    output_path: str = "output/20250729_버스혼잡도.csv",
):
    """
    Args:
        input_path1 (str): 버스 위치 정보 데이터 경로
        input_path2 (str): 버스 혼잡도 데이터 경로
        output_path (str): 출력 결과 CSV 경로
    """
    raise NotImplementedError


### 실행 ###
if __name__ == "__main__":
    task()
