# Base 이미지
FROM python:3.8-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 파일 복사 및 설치
COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# CLIP 모델 미리 다운로드 (optional)
RUN python -c "from transformers import CLIPProcessor, CLIPModel; CLIPModel.from_pretrained('openai/clip-vit-base-patch16'); CLIPProcessor.from_pretrained('openai/clip-vit-base-patch16')"

# QWEN2 미리 다운로드 (optional)
RUN python -c "from transformers import AutoProcessor, Qwen2AudioForConditionalGeneration; Qwen2AudioForConditionalGeneration.from_pretrained('Qwen/Qwen2-Audio-7B', device_map='auto'); AutoProcessor.from_pretrained('Qwen/Qwen2-Audio-7B', trust_remote_code=True)"

# 애플리케이션 파일 복사
COPY app/ .

EXPOSE 8000

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]