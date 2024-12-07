import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Streamlit 제목
st.title("CurAItor")
st.subheader("Fine Art Curation Based on Your Music Taste")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("Upload an mp3 file", type=["mp3"])

FASTAPI_URL = "http://127.0.0.1:8000/upload/"

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    if st.button("Process File"):
        # File processing 진행 중 스피너 표시
        with st.spinner("Processing... This might take an eternity cuz underoptimized... fxxk final exam :("):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(FASTAPI_URL, files=files)

            if response.status_code == 200:
                st.success("File processed successfully!")
                # 이미지 파일 반환
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="Curation Result")
            else:
                st.error("Failed to process the file.")
