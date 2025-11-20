# Audio Quality Benchmark

A comprehensive benchmark tool for evaluating speech and audio quality using state-of-the-art models. This project provides automated evaluation of audio through Mean Opinion Score (MOS) prediction and Automatic Speech Recognition (ASR) metrics.

## Features

- **MOS Prediction**: Predict speech quality using [NISQA](https://github.com/gabrielmittag/NISQA) (Non-Intrusive Speech Quality Assessment)
- **ASR Evaluation**: Evaluate speech recognition using NVIDIA NeMo Conformer Large model
- **REST API**: FastAPI-based service for programmatic access
- **Web Demo**: Interactive web interface for comparing results from different models

## Installation

### 1. Download ASR Model Weights

Download the NVIDIA Conformer Large model for ASR evaluation:
- Model: [stt_en_conformer_ctc_xlarge v1.10.0](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_conformer_ctc_xlarge?version=1.10.0)
- Place the weights in: `/evaluation/asr/stt_en_conformer_ctc_xlarge_v1.10.0/`

#### Configure NeMo (Optional)
To disable progress bar logging during transcription, modify the NeMo library:
**File to modify:** `nemo/collections/asr/models/ctc_models.py`

**Location:** Find the `transcribe()` function in the `EncDecCTCModel` class

**Change:**
```python
# Before
for test_batch in tqdm(temporary_datalayer, desc="Transcribing"):
```

```python
# After
for test_batch in temporary_datalayer:
```

This removes the tqdm progress bar output during transcription, which is useful for cleaner logs in production environments.

### 2. Set Up Environment

Create and activate the conda environment:

```bash
conda env create -f arts_env.yml
conda activate arts-eval
```

### 3. Install Dependencies

```bash
pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu128
conda install -y -c conda-forge cython pybind11 cmake ninja
pip install "nemo_toolkit[asr]==1.16.0" soundfile librosa
pip install --no-cache-dir "huggingface_hub==0.19.4" "transformers<4.37" "datasets<2.16" "tokenizers<0.15"
pip install "pytorch-lightning==1.9.5" "torchmetrics<=0.11.4"
conda install -y -c conda-forge "scipy>=1.10,<1.12"
```

## Usage

### Starting the Evaluation Server

Navigate to the evaluation directory and start the FastAPI server:

```bash
cd evaluation
python app.py
```

The server will start on `http://localhost:8000`.

### API Endpoints

#### Predict MOS (Mean Opinion Score)

Predict the quality score for an audio file:

```python
import requests
from pathlib import Path

file_path = Path("path/to/your/audio.wav")
response = requests.post(
    'http://localhost:8000/predict_mos',
    json={"audio_path": str(file_path.absolute())}
)

result = response.json()
print(f"MOS Score: {result['mos_pred']}")
```

**Request:**
```json
{
  "audio_path": "/absolute/path/to/audio.wav"
}
```

**Response:**
```json
{
  "audio_path": "/absolute/path/to/audio.wav",
  "mos_pred": 3.85
}
```

### Web Demo

A web-based interface is available for comparing audio quality results from different models. See the `website/` directory for more details.

## Project Structure

```
.
├── evaluation/
│   ├── asr/                  # ASR model weights
│   ├── NISQA/                # NISQA implementation
│   └── app.py                # FastAPI evaluation server
├── website/                  # Web demo interface
├── arts_env.yml              # Conda environment file
└── README.md
```

## Citation

If you use NISQA in your research, please cite:

```bibtex
@inproceedings{Mittag_2021,
  title     = {NISQA: A Deep CNN-Self-Attention Model for Multidimensional Speech Quality Prediction with Crowdsourced Datasets},
  author    = {Mittag, Gabriel and Naderi, Babak and Chehadi, Assmaa and M{\"o}ller, Sebastian},
  booktitle = {Interspeech 2021},
  year      = {2021},
  month     = aug,
  publisher = {ISCA},
  doi       = {10.21437/interspeech.2021-299},
  url       = {http://dx.doi.org/10.21437/Interspeech.2021-299}
}
```

## License

Please refer to the individual model licenses:
- [NISQA License](https://github.com/gabrielmittag/NISQA)
- [NVIDIA NeMo License](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_conformer_ctc_xlarge)
