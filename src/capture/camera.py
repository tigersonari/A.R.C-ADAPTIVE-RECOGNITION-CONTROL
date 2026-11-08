"""Modulo de captura de video (Desafio 6)."""
import cv2


class Camera:
    """Abre, le e libera uma webcam convencional."""

    def __init__(self, index=0, width=960, height=720):
        self.index = index
        self.width = width
        self.height = height
        self._capture = None

    def iniciar(self):
        if self._capture is not None:
            return
        # O backend padrao costuma funcionar no Windows e em outros sistemas.
        cap = cv2.VideoCapture(self.index)
        if not cap.isOpened():
            cap.release()
            raise RuntimeError(
                f'Nao foi possivel abrir a webcam {self.index}. '
                'Verifique permissoes do Windows e outros aplicativos usando a camera.'
            )
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._capture = cap

    def ler_frame(self):
        if self._capture is None:
            raise RuntimeError('A camera nao foi iniciada.')
        ok, frame = self._capture.read()
        if not ok or frame is None or frame.size == 0:
            raise RuntimeError('Falha ao capturar frame da webcam.')
        return frame

    def encerrar(self):
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def __enter__(self):
        self.iniciar()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.encerrar()
