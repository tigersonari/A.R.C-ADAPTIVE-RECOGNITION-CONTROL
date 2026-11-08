"""MediaPipe Hand Landmarker em modo VIDEO (Desafios 7 e 8)."""
from pathlib import Path

import cv2
import numpy as np


class HandTracker:
    """Converte frames OpenCV em 21 pontos por mao detectada.

    O modo VIDEO usa informacoes entre frames para rastrear a mao e
    evita a necessidade de executar o detector completo a cada imagem.
    """

    def __init__(
        self,
        model_path,
        max_hands=1,
        detection_confidence=0.5,
        presence_confidence=0.5,
        tracking_confidence=0.5,
    ):
        path = Path(model_path)
        if not path.is_file():
            raise FileNotFoundError(
                f'Modelo nao encontrado: {path}. '
                'Execute: python scripts/baixar_modelo.py'
            )

        try:
            import mediapipe as mp
        except ImportError as exc:
            raise RuntimeError(
                'MediaPipe nao esta instalado. Instale as dependencias com '
                'python -m pip install -r requirements.txt'
            ) from exc

        self._mp = mp
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=presence_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self._task = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self._last_timestamp_ms = -1

    def processar(self, frame_bgr, timestamp_ms):
        """Retorna HandLandmarkerResult, sem classificar gestos."""
        if timestamp_ms <= self._last_timestamp_ms:
            raise ValueError('Timestamps do video devem ser crescentes.')
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb = np.ascontiguousarray(rgb)
        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        result = self._task.detect_for_video(image, timestamp_ms)
        self._last_timestamp_ms = timestamp_ms
        return result

    def encerrar(self):
        if self._task is not None:
            self._task.close()
            self._task = None

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.encerrar()
