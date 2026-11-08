"""Prova de conceito do A.R.C. - desafios 5 a 10.

Exemplos:
    python src/main.py --modo camera
    python src/main.py --modo maos
    python src/main.py --modo analise
"""
import argparse
from datetime import datetime
import sys
import time

import cv2

from config import (
    CAMERA_WIDTH, CAMERA_HEIGHT, EVIDENCE_DIR, WINDOW_TITLE,
    MODEL_PATH, MAX_HANDS, HAND_DETECTION_CONFIDENCE,
    HAND_PRESENCE_CONFIDENCE, TRACKING_CONFIDENCE,
)
from capture.camera import Camera
from ui.landmarks import desenhar_landmarks, desenhar_painel


def args_cli():
    parser = argparse.ArgumentParser(description='A.R.C. - Webcam e rastreamento de maos')
    parser.add_argument('--modo', choices=['camera', 'maos', 'analise'], default='maos',
                        help='camera = D6; maos = D7/D8; analise = D9/D10')
    parser.add_argument('--camera', type=int, default=0, help='Indice da webcam (padrao: 0)')
    parser.add_argument('--sem-espelho', action='store_true', help='Nao espelhar a imagem')
    return parser.parse_args()


def executar(modo, indice_camera=0, espelho=True):
    tracker = None
    estabilizador = None
    if modo == 'analise':
        from processing.temporal import EstabilizadorExtensao
        estabilizador = EstabilizadorExtensao(janela=5)
    camera = Camera(index=indice_camera, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
    try:
        # Importacao tardia: modo camera funciona sem arquivo de modelo.
        if modo in ('maos', 'analise'):
            from tracking.hand_tracker import HandTracker
            tracker = HandTracker(
                MODEL_PATH, MAX_HANDS, HAND_DETECTION_CONFIDENCE,
                HAND_PRESENCE_CONFIDENCE, TRACKING_CONFIDENCE,
            )

        camera.iniciar()
        cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_TITLE, 960, 720)
        inicio = time.perf_counter()
        anterior = inicio
        ultimo_timestamp = -1
        print('A.R.C. em execucao. Pressione Q para sair e S para salvar evidencia.')

        while True:
            frame = camera.ler_frame()
            if espelho:
                frame = cv2.flip(frame, 1)

            agora = time.perf_counter()
            fps = 1.0 / max(agora - anterior, 1e-6)
            anterior = agora
            quantidade = 0

            if tracker is not None:
                # VIDEO exige timestamp inteiro estritamente crescente (ms).
                timestamp_ms = max(ultimo_timestamp + 1, int((agora - inicio) * 1000))
                ultimo_timestamp = timestamp_ms
                resultado = tracker.processar(frame, timestamp_ms)
                quantidade = desenhar_landmarks(frame, resultado)
                if modo == 'analise' and getattr(resultado, 'hand_landmarks', None):
                    from processing.coordinates import normalizar_landmarks
                    from processing.features import extrair_caracteristicas
                    from ui.analysis import desenhar_analise
                    try:
                        mao = normalizar_landmarks(resultado.hand_landmarks[0])
                        caracteristicas = extrair_caracteristicas(mao)
                        caracteristicas = estabilizador.atualizar(caracteristicas)
                        desenhar_analise(frame, mao, caracteristicas)
                    except ValueError as exc:
                        # Frames ruidosos nao devem interromper a captura.
                        estabilizador.reiniciar()
                        print(f'AVISO: Coordenadas descartadas neste frame: {exc}')
                elif modo == 'analise':
                    estabilizador.reiniciar()

            desenhar_painel(frame, modo, quantidade, fps, espelho)
            cv2.imshow(WINDOW_TITLE, frame)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla in (ord('q'), ord('Q'), 27):
                break
            if tecla in (ord('s'), ord('S')):
                EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
                caminho = EVIDENCE_DIR / f'arc_{modo}_{datetime.now():%Y%m%d_%H%M%S}.png'
                if cv2.imwrite(str(caminho), frame):
                    print(f'Evidencia registrada: {caminho}')
                else:
                    print('Nao foi possivel salvar o print. Confira permissoes da pasta.')

    finally:
        camera.encerrar()
        if tracker is not None:
            tracker.encerrar()
        cv2.destroyAllWindows()


def main():
    args = args_cli()
    if args.camera < 0:
        print('ERRO: O indice da camera deve ser zero ou positivo.', file=sys.stderr)
        return 2
    try:
        executar(args.modo, args.camera, not args.sem_espelho)
        return 0
    except (RuntimeError, FileNotFoundError, ValueError, OSError) as exc:
        print(f'ERRO: {exc}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('\nAplicacao interrompida.')
        return 130


if __name__ == '__main__':
    sys.exit(main())
