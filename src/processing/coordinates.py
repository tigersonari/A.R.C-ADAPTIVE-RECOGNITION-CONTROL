"""Desafio 9: limpeza, validação e normalização de coordenadas (21 landmarks)."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MaoNormalizada:
    # Posições em relação ao punho e divididas pelo tamanho da palma.
    pontos: tuple
    # Escala no espaço xy normalizado fornecido pelo MediaPipe.
    escala_palma: float
    origem_punho: tuple


def _distancia_xy(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def normalizar_landmarks(landmarks):
    """Retorna 21 coordenadas (x,y,z) relativas ao punho e escala da palma.

    MediaPipe fornece coordenadas normalizadas de imagem (x e y, com
    possível extrapolação fora do enquadramento) e z relativo. A função
    mantém esse referencial e NÃO estima distâncias físicas em cm.
    """
    if len(landmarks) != 21:
        raise ValueError('Esperados exatamente 21 landmarks por mao.')
    pontos = []
    for ponto in landmarks:
        try:
            x, y, z = float(ponto.x), float(ponto.y), float(ponto.z)
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError('Landmark invalido: esperado x, y e z.') from exc
        if not all(math.isfinite(v) for v in (x, y, z)):
            raise ValueError('Coordenadas nao podem ser NaN ou infinitas.')
        pontos.append((x, y, z))

    # Largura da palma: MCP do indicador (5) até MCP do mindinho (17).
    # Se a palma estiver de lado, o segmento pode se tornar muito pequeno;
    # nesse caso, usar o comprimento do punho até MCP médio (0->9).
    escala = _distancia_xy(pontos[5], pontos[17])
    if escala < 1e-6:
        escala = _distancia_xy(pontos[0], pontos[9])
    if escala < 1e-6:
        raise ValueError('Palma com escala zero: nao e possivel normalizar.')

    origem = pontos[0]
    normalizados = tuple(
        ((x - origem[0]) / escala,
         (y - origem[1]) / escala,
         (z - origem[2]) / escala)
        for x, y, z in pontos
    )
    return MaoNormalizada(
        pontos=normalizados, escala_palma=escala, origem_punho=origem
    )
