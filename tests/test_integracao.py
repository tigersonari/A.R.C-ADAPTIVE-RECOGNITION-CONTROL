"""Testes de integracao simulados; nao substituem teste real da webcam."""
import sys
from pathlib import Path
from contextlib import ExitStack
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import main as app


class FakeCamera:
    aberta = False
    encerrada = False
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    def iniciar(self):
        type(self).aberta = True
    def ler_frame(self):
        return np.zeros((480, 640, 3), dtype=np.uint8)
    def encerrar(self):
        type(self).encerrada = True


class FakeTracker:
    encerrado = False
    processou = 0
    def __init__(self, *args):
        pass
    def processar(self, frame, timestamp_ms):
        type(self).processou += 1
        points = [SimpleNamespace(x=0.15 + i * 0.03, y=0.25 + i * 0.01) for i in range(21)]
        return SimpleNamespace(hand_landmarks=[points])
    def encerrar(self):
        type(self).encerrado = True


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        FakeCamera.aberta = False
        FakeCamera.encerrada = False
        FakeTracker.encerrado = False
        FakeTracker.processou = 0

    def _fake_window(self):
        return (
            patch('main.cv2.namedWindow'),
            patch('main.cv2.resizeWindow'),
            patch('main.cv2.imshow'),
            patch('main.cv2.waitKey', return_value=ord('q')),
            patch('main.cv2.destroyAllWindows'),
        )

    def test_modo_camera_inicia_e_fecha(self):
        patches = self._fake_window()
        with ExitStack() as stack:
            stack.enter_context(patch('main.Camera', FakeCamera))
            for p in patches:
                stack.enter_context(p)
            app.executar('camera')
        self.assertTrue(FakeCamera.aberta)
        self.assertTrue(FakeCamera.encerrada)

    def test_modo_maos_encadeia_detecao_e_desenho(self):
        patches = self._fake_window()
        with ExitStack() as stack:
            stack.enter_context(patch('main.Camera', FakeCamera))
            stack.enter_context(patch('tracking.hand_tracker.HandTracker', FakeTracker))
            for p in patches:
                stack.enter_context(p)
            app.executar('maos')
        self.assertTrue(FakeCamera.aberta)
        self.assertTrue(FakeCamera.encerrada)
        self.assertTrue(FakeTracker.encerrado)
        self.assertEqual(FakeTracker.processou, 1)
