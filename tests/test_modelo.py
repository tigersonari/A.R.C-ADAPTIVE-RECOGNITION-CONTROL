import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from tracking.hand_tracker import HandTracker


class ModelTests(unittest.TestCase):
    def test_mensagem_se_modelo_ausente(self):
        with self.assertRaisesRegex(FileNotFoundError, 'Modelo nao encontrado'):
            HandTracker(Path('arquivo_que_nao_existe.task'))
