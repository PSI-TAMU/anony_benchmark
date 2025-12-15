import os
import re
import torch
import librosa
import uvicorn
import argparse
import warnings
import nemo.collections.asr as nemo_asr
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from NISQA.nisqa.NISQA_model import nisqaModel
from transformers import Wav2Vec2FeatureExtractor, WavLMForXVector

warnings.filterwarnings(
    "ignore",
    message="PySoundFile failed. Trying audioread instead.",
    category=UserWarning,
)
warnings.filterwarnings(
    "ignore",
    message="librosa.core.audio.__audioread_load",
    category=FutureWarning,
)

warnings.filterwarnings(
    "ignore",
    message="Support for mismatched key_padding_mask and attn_mask is deprecated. Use same type for both instead.",
    category=UserWarning,
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
asr = nemo_asr.models.EncDecCTCModelBPE.restore_from("asr/stt_en_conformer_ctc_xlarge_v1.10.0/stt_en_conformer_ctc_xlarge.tar.gz")

sv_feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained('microsoft/wavlm-base-sv')
sv_model = WavLMForXVector.from_pretrained('microsoft/wavlm-base-sv')
sv_model.to(device)

app = FastAPI()
class AudioRequest(BaseModel):
    audio_path: str

def normalize(text):
    # lowercase
    text = text.lower()
    # remove punctuation (anything not word or whitespace)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def get_wavlm_embedding(utt_path):
    audio1, _ = librosa.load(utt_path, sr=16000)
    inputs = sv_feature_extractor([audio1], return_tensors="pt", sampling_rate=16000, padding=True)
    inputs = {k: v.to(sv_model.device) for k, v in inputs.items()}
    with torch.no_grad():
        embeddings = sv_model(**inputs).embeddings
    embeddings = torch.nn.functional.normalize(embeddings, dim=-1).cpu()
    return embeddings.squeeze(0).cpu().numpy()

@app.post("/predict_mos")
def predict_mos(request: AudioRequest):
    if not os.path.exists(request.audio_path):
        raise HTTPException(status_code=404, detail=f"File not found")

    args = {
        'mode': 'predict_file',
        'deg': request.audio_path,
        'pretrained_model': './NISQA/weights/nisqa.tar',
        'ms_channel': None,
        'output_dir': None
    }
    nisqa = nisqaModel(args, verbose=False)
    result = nisqa.predict()

    return {
        "audio_path": request.audio_path,
        "mos_pred": float(result['mos_pred'][0])
    }

@app.post("/predict_asr")
def predict_asr(request: AudioRequest):
    if not os.path.exists(request.audio_path):
        raise HTTPException(status_code=404, detail=f"File not found")
    
    transcription = asr.transcribe([request.audio_path], batch_size=1)[0]

    return {
        "audio_path": request.audio_path,
        "transcription": transcription
    }

@app.post("/speaker_embedding")
def get_speaker_embedding(request: AudioRequest):
    if not os.path.exists(request.audio_path):
        raise HTTPException(status_code=404, detail=f"File not found")
    
    embedding = get_wavlm_embedding(request.audio_path)
    return {
        "audio_path": request.audio_path,
        "speaker_embedding": embedding.tolist()
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    
    uvicorn.run(app, host=args.host, port=args.port)