"""Baixa o modelo oficial Hand Landmarker de Google AI Edge uma unica vez.

Fonte oficial: https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker
"""
from pathlib import Path
import hashlib
import sys
import urllib.error
import urllib.request

URL = (
    'https://storage.googleapis.com/mediapipe-models/hand_landmarker/'
    'hand_landmarker/float16/latest/hand_landmarker.task'
)
BASE = Path(__file__).resolve().parent.parent
DEST = BASE / 'models' / 'hand_landmarker.task'
TEMP = DEST.with_suffix('.download')


def baixar():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.is_file() and DEST.stat().st_size > 1_000_000:
        print(f'Modelo ja existe: {DEST} ({DEST.stat().st_size} bytes)')
        return 0

    print('Baixando o modelo oficial Hand Landmarker...')
    print(URL)
    try:
        urllib.request.urlretrieve(URL, TEMP)
        if TEMP.stat().st_size < 1_000_000:
            raise OSError('Arquivo muito pequeno para ser o modelo esperado.')
        TEMP.replace(DEST)
        sha = hashlib.sha256(DEST.read_bytes()).hexdigest()
        print(f'Modelo salvo em: {DEST}')
        print(f'Tamanho: {DEST.stat().st_size} bytes')
        print(f'SHA-256 local: {sha}')
        return 0
    except (OSError, urllib.error.URLError) as exc:
        TEMP.unlink(missing_ok=True)
        print(f'Falha no download: {exc}', file=sys.stderr)
        print('Baixe manualmente o arquivo da URL acima e salve como:', DEST)
        return 1


if __name__ == '__main__':
    sys.exit(baixar())
