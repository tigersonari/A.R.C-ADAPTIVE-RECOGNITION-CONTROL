"""Integração simulada: verifica fluxo analise sem câmera física."""
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import main as app

class FakeCamera:
    def __init__(self, **kwargs): pass
    def iniciar(self): pass
    def ler_frame(self): return np.zeros((480, 640, 3), dtype=np.uint8)
    def encerrar(self): pass

class FakeTracker:
    def __init__(self, *args): pass
    def processar(self, frame, timestamp_ms):
        p=[SimpleNamespace(x=.4,y=.7,z=.0) for _ in range(21)]
        p[0]=SimpleNamespace(x=.5,y=.8,z=0.0)
        p[5]=SimpleNamespace(x=.35,y=.65,z=0.0)
        p[17]=SimpleNamespace(x=.65,y=.65,z=0.0)
        p[9]=SimpleNamespace(x=.5,y=.55,z=0.0)
        return SimpleNamespace(hand_landmarks=[p])
    def encerrar(self): pass

class AnaliseIntegrationTest(unittest.TestCase):
    def test_analise_roda_sem_exception(self):
        with ExitStack() as stack:
            stack.enter_context(patch('main.Camera', FakeCamera))
            stack.enter_context(patch('tracking.hand_tracker.HandTracker', FakeTracker))
            for meth in ['namedWindow','resizeWindow','imshow','destroyAllWindows']:
                stack.enter_context(patch('main.cv2.'+meth))
            stack.enter_context(patch('main.cv2.waitKey',return_value=ord('q')))
            app.executar('analise')

if __name__=='__main__': unittest.main()
