# CurAItor
좋아하는 음악과 어울리는 분위기의 예술작품 큐레이션 서비스 데모입니다.

## Project Introduction
`Qwen2-Audio-7B` 모델을 이용하여 오디오 파일로부터 음악의 분위기와 장르를 텍스트 형태로 얻습니다.

그 텍스트를 `clip-vit-base-patch16` 모델에 태워서 예술작품 데이터베이스에서 가장 유사도가 높은 작품을 추천합니다.

예술품 데이터베이스는 `wikiart` 데이터셋에서 랜덤하게 1000개를 샘플하여 사용하였습니다.

## How to Run

### Access via Distributed Webpage

[CurAItor](https://curaitor.streamlit.app/)

### Building Docker Image from Local

1. Docker 이미지 빌드:
```bash
docker build -t curaitor .
```

2. Docker 백엔드 로컬에서 실행:
```bash
docker run -p 8000:8000 curaitor
```

3. Streamlit 프런트엔드 로컬에서 실행:
```bash
streamlit run frontend/app.py --server.port 8501
```

## Expected Improvements
`Qwen2-Audio-7B` 모델이 상당히 무겁고 inference가 느립니다. 단독으로 사용해 보면 음원파일의 물리적인 분석(조성, 템포 같은 것)에 상당히 집착하는 것으로 보이는데 task에 맞게 fine-tuning할 수 있다면 더 좋을 것입니다. 현 버전에서는 prompt engineering 수준에서 적당히 때우고 넘겼습니다. 

원래 목표는 그림 띄워 주면서 작기 및 작품 이름 정도는 같이 알려주고 싶었는데, 안타깝게도 `wikiart` 데이터셋은 원래 비전 모델 트레이닝셋이라 작품 이름은 데이터베이스에 포함되어 있지 않았습니다. 일일이 labeling하기는 기말이 급했기 때문에 넘어가 주시면 고맙겠습니다...

## Citation
```bash
@article{Qwen2-Audio,
  title={Qwen2-Audio Technical Report},
  author={Chu, Yunfei and Xu, Jin and Yang, Qian and Wei, Haojie and Wei, Xipin and Guo,  Zhifang and Leng, Yichong and Lv, Yuanjun and He, Jinzheng and Lin, Junyang and Zhou, Chang and Zhou, Jingren},
  journal={arXiv preprint arXiv:2407.10759},
  year={2024}
}
```
