from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
import matplotlib.pyplot as plt

# Path to Image Database

img_dir = "./wikiart1000"
image_paths = [os.path.join(img_dir, file) for file in os.listdir(img_dir) if file.endswith('.jpg')]
similarity_scores = []

# CLIP Model Definition

class Text2Image:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
        self.model.eval()
    
    def retrieve(self, text):
        for img_path in image_paths:
            image = Image.open(img_path).convert("RGB")
            inputs = self.processor(text=[text], images=image, return_tensors="pt", padding=True)

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                similarity_score = logits_per_image.item()
            
            similarity_scores.append((similarity_score, img_path))

        best_match_path = max(similarity_scores, key=lambda x: x[0])[1]

        return best_match_path