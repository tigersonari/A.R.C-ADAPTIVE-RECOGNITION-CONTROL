"""Verifica o contrato MediaPipe com dependencia simulada, sem inferencia real."""
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from tracking.hand_tracker import HandTracker


class FakeTask:
    def __init__(self):
        self.timestamps = []
        self.closed = False
    def detect_for_video(self, image, timestamp_ms):
        self.timestamps.append(timestamp_ms)
        return SimpleNamespace(hand_landmarks=[])
    def close(self):
        self.closed = True


class TrackerTests(unittest.TestCase):
    def test_mediapipe_video_chamado_com_frame_e_timestamp(self):
        fake_task = FakeTask()
        fake_mp = SimpleNamespace(
            tasks=SimpleNamespace(
                BaseOptions=lambda **kw: kw,
                vision=SimpleNamespace(
                    HandLandmarkerOptions=lambda **kw: kw,
                    RunningMode=SimpleNamespace(VIDEO='VIDEO'),
                    HandLandmarker=SimpleNamespace(create_from_options=lambda options: fake_task),
                ),
            ),
            ImageFormat=SimpleNamespace(SRGB='SRGB'),
            Image=lambda **kw: kw,
        )
        with tempfile.TemporaryDirectory() as tmp:
            model = Path(tmp) / 'dummy.task'
            model.write_bytes(b'nao e um modelo de verdade')
            with patch.dict(sys.modules, {'mediapipe': fake_mp}):
                with HandTracker(model) as tracker:
                    image = np.zeros((32, 32, 3), dtype=np.uint8)
                    tracker.processar(image, 10)
                    tracker.processar(image, 20)
                    with self.assertRaisesRegex(ValueError, 'crescentes'):
                        tracker.processar(image, 20)
        self.assertEqual(fake_task.timestamps, [10, 20])
        self.assertTrue(fake_task.closed)
