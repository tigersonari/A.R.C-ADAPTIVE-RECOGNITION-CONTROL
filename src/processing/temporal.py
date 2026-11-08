"""Filtro de maioria para diminuir oscilacoes da estimativa entre frames."""
from collections import deque
from dataclasses import replace


class EstabilizadorExtensao:
    """Suaviza cada dedo usando uma janela curta de 5 frames.

    Nao substitui rastreamento temporal nem reconhecimento de gestos.
    Para nao reter uma mao antiga, chamar `reiniciar()` quando a mao some.
    """
    def __init__(self, janela=5):
        if janela < 3 or janela % 2 == 0:
            raise ValueError('Janela deve ser impar e >= 3.')
        self.janela = janela
        self.reiniciar()

    def reiniciar(self):
        self._historico = {}
        self._ultimo = {}

    def atualizar(self, caracteristicas):
        atual = caracteristicas.dedos_possivelmente_estendidos
        saida = {}
        for dedo, valor in atual.items():
            if dedo not in self._historico:
                self._historico[dedo] = deque(maxlen=self.janela)
            historico = self._historico[dedo]
            historico.append(bool(valor))
            positivos = sum(historico)
            # Em empate, conservar o estado anterior (evita piscar).
            if positivos * 2 == len(historico):
                estabilizado = self._ultimo.get(dedo, bool(valor))
            else:
                estabilizado = positivos * 2 > len(historico)
            self._ultimo[dedo] = estabilizado
            saida[dedo] = estabilizado
        return replace(caracteristicas, dedos_possivelmente_estendidos=saida)
