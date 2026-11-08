import sys
from pathlib import Path
import unittest
from types import SimpleNamespace
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ui.landmarks import HAND_CONNECTIONS, desenhar_landmarks, desenhar_painel, _pixel


class DrawingTests(unittest.TestCase):
    def test_21_pontos_e_conexoes_validas(self):
        self.assertEqual(len(set([n for pair in HAND_CONNECTIONS for n in pair])), 21)
        self.assertTrue(all(0 <= a < 21 and 0 <= b < 21 for a, b in HAND_CONNECTIONS))

    def test_coordenadas_ficam_dentro_da_imagem(self):
        p = SimpleNamespace(x=-0.2, y=1.4)
        self.assertEqual(_pixel(p, 640, 480), (0, 479))

    def test_desenho_de_21_landmarks_sinteticos(self):
        frame = np.zeros((400, 600, 3), dtype=np.uint8)
        points = [SimpleNamespace(x=0.1 + i * 0.025, y=0.1 + i * 0.027) for i in range(21)]
        result = SimpleNamespace(hand_landmarks=[points])
        n = desenhar_landmarks(frame, result)
        self.assertEqual(n, 1)
        self.assertGreater(int(frame.sum()), 0)

    def test_sem_mao(self):
        frame = np.zeros((200, 400, 3), dtype=np.uint8)
        result = SimpleNamespace(hand_landmarks=[])
        self.assertEqual(desenhar_landmarks(frame, result), 0)

    def test_painel_renderiza(self):
        frame = np.zeros((400, 640, 3), dtype=np.uint8)
        desenhar_painel(frame, 'camera', 0, 25.0, True)
        self.assertGreater(int(frame.sum()), 0)
