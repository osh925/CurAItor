from fastapi import FastAPI, File, UploadFile
from model.audiomodel import Audio2Text
from model.clipmodel import Text2Image
import os

app = FastAPI()
aud_model = Audio2Text()
vis_model = Text2Image()

UPLOAD_DIR = "./uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"Home": "CurAItor"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Step 1: 파일 저장
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Step 2: interpret 호출
    interpretation = aud_model.retrieve(file_location)  # 오디오에서 텍스트(분위기, 장르) 추출
    
    # Step 3: curation 호출
    curation_path = vis_model.retrieve(interpretation)  # 텍스트(분위기, 장르)에서 유사성 높은 이미지 검색
    
    # Step 4: 업로드 디렉터리 정리
    for uploaded_file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, uploaded_file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # 결과 반환
    return {
        "text_interpretation": interpretation,
        "curation_result": curation_path,  # 생성된 이미지 경로
    }


#### Not used in practice, just for debuging ####

@app.post("/interpret")
async def interpret_audio(file_path: str):
    """오디오를 텍스트로 변환"""
    interpretation = aud_model.retrieve(file_path)  # 오디오에서 텍스트 추출
    return {"text": interpretation}

@app.post("/curation")
async def process_text(text: str):
    """텍스트를 기반으로 이미지 생성"""
    curation_path = vis_model.retrieve(text)  # 텍스트에서 이미지 생성
    return {"curation_result": curation_path}