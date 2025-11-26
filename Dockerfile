FROM python:3.10-slim

# 기본 패키지
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 스크립트 복사
COPY worker.py .
COPY keywords.txt .

# 실행
CMD ["python", "worker.py"]
