"""Configuracoes da prova de conceito A.R.C. (desafios 5 a 10)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'hand_landmarker.task'
EVIDENCE_DIR = BASE_DIR / 'evidencias'
WINDOW_TITLE = 'A.R.C. | Visao Computacional'
CAMERA_WIDTH = 960
CAMERA_HEIGHT = 720
MAX_HANDS = 1
HAND_DETECTION_CONFIDENCE = 0.5
HAND_PRESENCE_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5
