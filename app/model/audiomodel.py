from transformers import AutoProcessor, Qwen2AudioForConditionalGeneration
import torch
import os
from io import BytesIO
import librosa

class Audio2Text:
    def __init__(self):
        self.model = Qwen2AudioForConditionalGeneration.from_pretrained("Qwen/Qwen2-Audio-7B", device_map="auto")
        self.processor = AutoProcessor.from_pretrained("Qwen/Qwen2-Audio-7B", trust_remote_code=True)
        self.model.eval()
    
    def retrieve(self, file_path):
        prompt = "<|audio_bos|><|AUDIO|><|audio_eos|>This is a song. Tell me both the mood and genre of the song in the form of (mood, genre):"
        audio, sr = librosa.load(file_path, sr=self.processor.feature_extractor.sampling_rate)
        inputs = self.processor(text=prompt, audios=audio, return_tensors="pt")
        generated_ids = self.model.generate(**inputs, max_length=256)
        generated_ids = generated_ids[:, inputs.input_ids.size(1):]
        response = self.processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        return response
