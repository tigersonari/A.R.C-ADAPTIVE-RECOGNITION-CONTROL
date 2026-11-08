import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from capture.camera import Camera


class FakeCapture:
    def __init__(self, opened=True, read_success=True):
        self.opened = opened
        self.read_success = read_success
        self.released = False
    def isOpened(self):
        return self.opened
    def set(self, prop, value):
        return True
    def read(self):
        return (self.read_success, np.zeros((16, 16, 3), dtype=np.uint8) if self.read_success else None)
    def release(self):
        self.released = True


class CameraTests(unittest.TestCase):
    def test_abertura_leitura_encerramento(self):
        device = FakeCapture()
        with patch('capture.camera.cv2.VideoCapture', return_value=device):
            with Camera() as cam:
                frame = cam.ler_frame()
                self.assertEqual(frame.shape, (16, 16, 3))
            self.assertTrue(device.released)

    def test_erro_camara_indisponivel(self):
        device = FakeCapture(opened=False)
        with patch('capture.camera.cv2.VideoCapture', return_value=device):
            with self.assertRaisesRegex(RuntimeError, 'abrir a webcam'):
                Camera().iniciar()
            self.assertTrue(device.released)

    def test_leitura_sem_iniciar(self):
        with self.assertRaisesRegex(RuntimeError, 'nao foi iniciada'):
            Camera().ler_frame()

    def test_erro_frame_invalido(self):
        device = FakeCapture(read_success=False)
        with patch('capture.camera.cv2.VideoCapture', return_value=device):
            with Camera() as cam:
                with self.assertRaisesRegex(RuntimeError, 'Falha ao capturar frame'):
                    cam.ler_frame()
