"""Desenho dos 21 landmarks e suas conexoes (Desafio 8)."""
import cv2

# Conexoes de referencia da estrutura de 21 pontos da mao do MediaPipe.
HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
)


def _pixel(landmark, width, height):
    x = min(max(int(landmark.x * width), 0), width - 1)
    y = min(max(int(landmark.y * height), 0), height - 1)
    return x, y


def desenhar_landmarks(frame, result):
    """Anota o proprio frame BGR e devolve quantas maos foram detectadas."""
    hands = getattr(result, 'hand_landmarks', []) if result is not None else []
    height, width = frame.shape[:2]
    for points in hands:
        if len(points) != 21:
            continue
        coords = [_pixel(p, width, height) for p in points]
        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, coords[start], coords[end], (255, 214, 50), 2, cv2.LINE_AA)
        for i, coord in enumerate(coords):
            cv2.circle(frame, coord, 5 if i in (0, 4, 8, 12, 16, 20) else 4,
                       (220, 40, 230), -1, cv2.LINE_AA)
            cv2.circle(frame, coord, 2, (255, 255, 255), -1, cv2.LINE_AA)
    return len(hands)


def desenhar_painel(frame, modo, quantidade, fps, espelho):
    """Feedback de camera e deteccao, sem reconhecer gestos ainda."""
    height, width = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, 94), (16, 22, 38), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    titulo = 'A.R.C. | D6' if modo == 'camera' else ('A.R.C. | D9+D10' if modo == 'analise' else 'A.R.C. | D7+D8')
    status = 'CAPTURA OK' if modo == 'camera' else ('MAO DETECTADA' if quantidade else 'AGUARDANDO MAO')
    cv2.putText(frame, titulo, (18, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (240, 245, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, status, (18, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.66,
                (80, 220, 255) if quantidade or modo == 'camera' else (170, 180, 190), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Maos: {quantidade} | Pontos: {21 if quantidade else 0} | FPS: {fps:.1f}',
                (max(8, width - 345), 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52,
                (230, 240, 248), 1, cv2.LINE_AA)
    cv2.putText(frame, 'ESPELHO' if espelho else 'SEM ESPELHO',
                (max(8, width - 140), 64), cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                (180, 195, 205), 1, cv2.LINE_AA)

    cv2.rectangle(frame, (0, height - 38), (width, height), (16, 22, 38), -1)
    cv2.putText(frame, 'Q = sair  |  S = salvar captura em evidencias/', (15, height - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 240, 248), 1, cv2.LINE_AA)
