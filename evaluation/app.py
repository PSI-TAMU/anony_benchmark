import os
import re
import torch
import uvicorn
import nemo.collections.asr as nemo_asr
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from NISQA.nisqa.NISQA_model import nisqaModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
asr = nemo_asr.models.EncDecCTCModelBPE.restore_from("asr/stt_en_conformer_ctc_xlarge_v1.10.0/stt_en_conformer_ctc_xlarge.tar.gz")

app = FastAPI()
class AudioRequest(BaseModel):
    audio_path: str

def normalize(text):
    # lowercase
    text = text.lower()
    # remove punctuation (anything not word or whitespace)
    text = re.sub(r"[^\w\s]", "", text)
    return text

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)