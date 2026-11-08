"""Desafio 10: medidas geométricas e estimativa de dedos estendidos.

IMPORTANTE: as regras abaixo sao HEURISTICAS. Elas nao classificam gestos;
exigem verificacao com webcam em diferentes perspectivas e iluminacoes.
"""
from dataclasses import dataclass
import math
from .coordinates import MaoNormalizada

# MCP = base; PIP e DIP = articulacoes intermediarias; TIP = ponta.
# O polegar usa uma regra PROPRIA (CMC/MCP/IP/TIP: landmarks 1-4).
DEDOS = {
    'indicador': (5, 6, 7, 8),
    'medio': (9, 10, 11, 12),
    'anelar': (13, 14, 15, 16),
    'mindinho': (17, 18, 19, 20),
}

# Limiares iniciais empiricos para prototipo; nao sao parametros validados.
LIMIAR_PIP_GRAUS = 145.0
LIMIAR_DIP_GRAUS = 145.0
PROJECAO_MINIMA = 1.25

# Limiar inicial do polegar: geometria diferente dos outros dedos.
# Valores experimentais; precisam ser conferidos com poses reais da webcam.
LIMIAR_POLEGAR_MCP_GRAUS = 125.0
LIMIAR_POLEGAR_IP_GRAUS = 145.0
AFASTAMENTO_POLEGAR_INDICADOR = 0.40  # escala = largura da palma
AFASTAMENTO_POLEGAR_PALMA = 1.05      # razão ponta->mindinho / MCP->mindinho


def distancia(a, b):
    """Distancia euclidiana XY em unidades relativas a largura da palma."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angulo_graus(a, b, c):
    """Angulo ABC em 2D; mantido para compatibilidade com testes existentes."""
    v1 = (a[0] - b[0], a[1] - b[1])
    v2 = (c[0] - b[0], c[1] - b[1])
    n1 = math.hypot(*v1)
    n2 = math.hypot(*v2)
    if n1 < 1e-9 or n2 < 1e-9:
        return None
    coseno = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
    return math.degrees(math.acos(max(-1.0, min(1.0, coseno))))


def angulo_3d_graus(a, b, c):
    """Angulo ABC usando (x,y,z), menos sensivel a dedos fora do plano 2D.

    O z do MediaPipe e uma estimativa de profundidade, nao um valor em cm.
    """
    v1 = tuple(a[i] - b[i] for i in range(3))
    v2 = tuple(c[i] - b[i] for i in range(3))
    n1 = math.sqrt(sum(v*v for v in v1))
    n2 = math.sqrt(sum(v*v for v in v2))
    if n1 < 1e-9 or n2 < 1e-9:
        return None
    coseno = sum(x*y for x,y in zip(v1,v2)) / (n1*n2)
    return math.degrees(math.acos(max(-1.0, min(1.0, coseno))))


def _projecao_relativa(mcp, pip, ponta):
    """Projecao da ponta na direcao MCP->PIP (independe do punho).

    Quando o dedo esta reto, a ponta avanca sobre esse eixo; quando dobra
    em direcao a palma, a projecao diminui. Retorna None se eixo degenerado.
    """
    eixo = tuple(pip[i] - mcp[i] for i in range(3))
    ponta_relativa = tuple(ponta[i] - mcp[i] for i in range(3))
    denominador = sum(v*v for v in eixo)
    if denominador < 1e-12:
        return None
    return sum(u*v for u,v in zip(eixo,ponta_relativa)) / denominador


def _distancia_3d(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def estimar_polegar_estendido(pontos):
    """Estimativa de extensão do polegar usando landmarks 1,2,3,4.

    Usa os ângulos CMC-MCP-IP e MCP-IP-TIP em 3D, combinados com
    afastamento da ponta em relação à palma (pontos 5 e 17).
    Distâncias e ângulos independem de espelhamento da webcam.
    Não equivale a reconhecer um gesto nem a medir centímetros.
    """
    cmc, mcp, ip, ponta = (pontos[i] for i in (1, 2, 3, 4))
    angulo_mcp = angulo_3d_graus(cmc, mcp, ip)
    angulo_ip = angulo_3d_graus(mcp, ip, ponta)
    # Evita divisão por zero em landmarks que se sobrepõem.
    base_palmar = _distancia_3d(mcp, pontos[17])
    if (angulo_mcp is None or angulo_ip is None or base_palmar < 1e-9):
        return False, angulo_mcp

    # Normalização já garantida por normalizar_landmarks.
    # A ponta afastada do indicador (5) e do lado do mindinho (17)
    # ajuda a separar polegar lateralmente aberto de dobrado na palma.
    dist_indicador = _distancia_3d(ponta, pontos[5])
    afastamento_palmar = _distancia_3d(ponta, pontos[17]) / base_palmar
    estendido = (
        angulo_mcp >= LIMIAR_POLEGAR_MCP_GRAUS
        and angulo_ip >= LIMIAR_POLEGAR_IP_GRAUS
        and dist_indicador >= AFASTAMENTO_POLEGAR_INDICADOR
        and afastamento_palmar >= AFASTAMENTO_POLEGAR_PALMA
    )
    return bool(estendido), angulo_mcp


@dataclass(frozen=True)
class CaracteristicasMao:
    distancia_polegar_indicador: float
    distancia_indicador_mindinho: float
    # Ângulo MCP do polegar e PIP dos demais dedos (graus).
    angulos_dedos: dict
    dedos_possivelmente_estendidos: dict


def extrair_caracteristicas(mao: MaoNormalizada):
    """Mede distâncias e estima extensão dos cinco dedos (incluindo polegar).

    Correcao em relacao a heuristica original:
      * usa dois angulos articulares PIP e DIP (nao MCP-PIP-TIP);
      * usa x, y, z para calcular esses angulos;
      * avalia a projecao na direcao da falange MCP->PIP;
      * nao depende da distancia ponta-punho, que falhava em certas poses;
      * o polegar usa suas articulações e uma medida relativa à palma.

    Mesmo assim, oclusao, angulo da camera e falhas do MediaPipe podem
    afetar as estimativas. NAO equivale a reconhecimento de gesto.
    """
    p = mao.pontos
    if len(p) != 21:
        raise ValueError('Necessarios 21 pontos normalizados.')
    polegar_estendido, angulo_polegar = estimar_polegar_estendido(p)
    angulos = {'polegar': angulo_polegar}
    estendidos = {'polegar': polegar_estendido}
    for dedo, (mcp, pip, dip, ponta) in DEDOS.items():
        angulo_pip = angulo_3d_graus(p[mcp],p[pip],p[dip])
        angulo_dip = angulo_3d_graus(p[pip],p[dip],p[ponta])
        projecao = _projecao_relativa(p[mcp], p[pip], p[ponta])
        angulos[dedo] = angulo_pip
        estendidos[dedo] = bool(
            angulo_pip is not None and angulo_dip is not None
            and projecao is not None
            and angulo_pip >= LIMIAR_PIP_GRAUS
            and angulo_dip >= LIMIAR_DIP_GRAUS
            and projecao >= PROJECAO_MINIMA
        )

    return CaracteristicasMao(
        distancia_polegar_indicador=distancia(p[4],p[8]),
        distancia_indicador_mindinho=distancia(p[8],p[20]),
        angulos_dedos=angulos,
        dedos_possivelmente_estendidos=estendidos,
    )
