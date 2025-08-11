# architon
Architon Repository

## 💻 Python venv 환경 세팅

### 1. Python 버전 확인
Python **3.10 이상**을 권장합니다.

    python --version
    # 또는
    python3 --version

### 2. 가상환경 생성

    # Windows
    python -m venv venv

    # macOS / Linux
    python3 -m venv venv

### 3. 가상환경 활성화

    # Windows (PowerShell)
    venv\Scripts\activate
    # Windows (cmd)
    venv\Scripts\activate.bat

    # macOS / Linux
    source venv/bin/activate

> 활성화되면 터미널 프롬프트 앞에 `(venv)` 가 표시됩니다.

### 4. 패키지 설치

    pip install --upgrade pip
    pip install -r requirements.txt

### 5. 실행 방법

    python [폴더이름]/[파일이름].py
    # 예시
    python task1_data/task_dictionary.py

### 📌 참고
- 새 패키지를 설치한 경우, 아래 명령어로 `requirements.txt`를 업데이트하세요.

      pip freeze > requirements.txt

- 모든 참가자는 **동일한** `requirements.txt`를 사용해야 합니다.
