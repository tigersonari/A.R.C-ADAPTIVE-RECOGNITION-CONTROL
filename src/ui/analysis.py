"""Apresentação das características extraídas, sem reconhecimento de gestos."""
import cv2


def desenhar_analise(frame, mao, caracteristicas):
    h, w = frame.shape[:2]
    x1 = max(8, w - min(325, w - 16))
    y1 = 104
    x2 = w - 8
    y2 = min(h - 44, 275)
    if y2 <= y1 + 25:
        return
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (13, 24, 43), -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 207, 45), 1)
    base = [
        'D9+D10 | ANALISE GEOMETRICA',
        f'Escala palma: {mao.escala_palma:.3f}',
        f'Dist. polegar-indicador: {caracteristicas.distancia_polegar_indicador:.2f}',
        f'Dist. indicador-mindinho: {caracteristicas.distancia_indicador_mindinho:.2f}',
        'Polegar: ' + ('ESTENDIDO' if
            caracteristicas.dedos_possivelmente_estendidos.get('polegar')
            else 'RECOLHIDO') + ' (estimativa)',
        'Extensao estimada (5 dedos):',
        ', '.join(
            dedo[:3].upper() for dedo, ativo in
            caracteristicas.dedos_possivelmente_estendidos.items() if ativo
        ) or 'nenhum',
    ]
    for i, linha in enumerate(base):
        y = y1 + 20 + 21 * i
        if y >= y2 - 5:
            break
        cv2.putText(frame, linha, (x1 + 9, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.42, (245, 246, 255), 1, cv2.LINE_AA)
