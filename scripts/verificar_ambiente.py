"""Confere instalacao das dependencias e a disponibilidade do modelo."""
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import platform
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL = BASE_DIR / 'models' / 'hand_landmarker.task'

print('A.R.C. | VERIFICACAO DO AMBIENTE')
print('Python:', sys.version.split()[0], '| Sistema:', platform.platform())
print('Executavel:', sys.executable)

pacotes = ('opencv-contrib-python', 'mediapipe', 'numpy')
erros = []
for pacote in pacotes:
    try:
        print(f'[OK] {pacote}: {version(pacote)}')
    except PackageNotFoundError:
        erros.append(pacote)
        print(f'[FALTA] {pacote}')

if not erros:
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
        _ = cv2.VideoCapture
        _ = mp.tasks.vision.HandLandmarker
        _ = np.ndarray
        print('[OK] Importacao e APIs principais verificadas.')
    except (ImportError, AttributeError) as exc:
        print('[ERRO] API indisponivel:', exc)
        erros.append('API de runtime')

if MODEL.is_file() and MODEL.stat().st_size > 1_000_000:
    print(f'[OK] Modelo localizado: {MODEL.name} ({MODEL.stat().st_size} bytes)')
else:
    print('[PENDENTE] Modelo de mao. Execute: python scripts/baixar_modelo.py')

if erros:
    print('Falha na verificacao. Instale: python -m pip install -r requirements.txt')
    sys.exit(1)
print('Dependencias OK. O modelo e exigido somente no modo maos.')
