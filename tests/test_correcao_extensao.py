"""Novos testes D10: articulacoes, rotacao, flexao e suavizacao temporal."""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from processing.coordinates import normalizar_landmarks
from processing.features import extrair_caracteristicas, angulo_3d_graus
from processing.temporal import EstabilizadorExtensao
from test_processamento import mao_teste


def flexionar_indicador(pontos):
    pontos = [SimpleNamespace(x=p.x,y=p.y,z=p.z) for p in pontos]
    # MCP(5), PIP(6) mantidos; DIP e ponta dobrados em direcao a palma.
    pontos[7] = SimpleNamespace(x=.43,y=.57,z=0)
    pontos[8] = SimpleNamespace(x=.47,y=.66,z=0)
    return pontos


def inclinar_em_2d(pontos, graus=67):
    c=math.cos(math.radians(graus)); s=math.sin(math.radians(graus))
    result=[]
    for p in pontos:
        dx=p.x-.5;dy=p.y-.5
        result.append(SimpleNamespace(x=.5+dx*c-dy*s, y=.5+dx*s+dy*c,z=p.z))
    return result


class TestesRegrasExtensao(unittest.TestCase):
    def test_mao_aberta_cinco_dedos(self):
        f=extrair_caracteristicas(normalizar_landmarks(mao_teste()))
        self.assertEqual(sum(f.dedos_possivelmente_estendidos.values()), 5)
        self.assertTrue(f.dedos_possivelmente_estendidos['polegar'])

    def test_indicador_flexionado_fica_falso(self):
        f=extrair_caracteristicas(normalizar_landmarks(flexionar_indicador(mao_teste())))
        self.assertFalse(f.dedos_possivelmente_estendidos['indicador'])
        self.assertTrue(f.dedos_possivelmente_estendidos['medio'])

    def test_mao_rotacionada_continua_estendida(self):
        f1=extrair_caracteristicas(normalizar_landmarks(mao_teste()))
        f2=extrair_caracteristicas(normalizar_landmarks(inclinar_em_2d(mao_teste())))
        self.assertEqual(f1.dedos_possivelmente_estendidos, f2.dedos_possivelmente_estendidos)

    def test_translacao_e_escala_nao_alteram_estado(self):
        p=mao_teste()
        transformados=[SimpleNamespace(x=.15+q.x*.8,y=.11+q.y*.8,z=q.z*.8) for q in p]
        f1=extrair_caracteristicas(normalizar_landmarks(p))
        f2=extrair_caracteristicas(normalizar_landmarks(transformados))
        self.assertEqual(f1.dedos_possivelmente_estendidos, f2.dedos_possivelmente_estendidos)

    def test_angulo_3d_reto(self):
        self.assertAlmostEqual(angulo_3d_graus((1,0,0),(0,0,0),(0,0,1)),90)

    def test_profundidade_pode_detectar_flexao(self):
        pontos=mao_teste()
        # Dobra real na profundidade, mesmo que o XY aparente uma linha reta.
        pontos[7] = SimpleNamespace(x=.35,y=.43,z=.28)
        pontos[8] = SimpleNamespace(x=.35,y=.35,z=.31)
        f=extrair_caracteristicas(normalizar_landmarks(pontos))
        self.assertFalse(f.dedos_possivelmente_estendidos['indicador'])

    def test_segmento_degenerado_nao_classifica(self):
        pontos=mao_teste()
        pontos[6] = SimpleNamespace(x=pontos[5].x,y=pontos[5].y,z=pontos[5].z)
        f=extrair_caracteristicas(normalizar_landmarks(pontos))
        self.assertFalse(f.dedos_possivelmente_estendidos['indicador'])


class TestesFiltroTemporal(unittest.TestCase):
    def setUp(self):
        self.base=extrair_caracteristicas(normalizar_landmarks(mao_teste()))
        self.filtro=EstabilizadorExtensao(janela=5)

    def _atualizar(self, estendido):
        novos=dict(self.base.dedos_possivelmente_estendidos)
        novos['indicador']=estendido
        return self.filtro.atualizar(replace(self.base,dedos_possivelmente_estendidos=novos))            .dedos_possivelmente_estendidos['indicador']

    def test_um_frame_errado_nao_desliga_dedo(self):
        for _ in range(5): self.assertTrue(self._atualizar(True))
        self.assertTrue(self._atualizar(False))

    def test_tres_frames_mudam_estado(self):
        for _ in range(5): self._atualizar(True)
        self._atualizar(False)
        self._atualizar(False)
        self.assertFalse(self._atualizar(False))

    def test_reiniciar_remove_historico(self):
        for _ in range(5): self._atualizar(True)
        self.filtro.reiniciar()
        self.assertFalse(self._atualizar(False))

    def test_janela_valida(self):
        with self.assertRaises(ValueError): EstabilizadorExtensao(janela=4)

if __name__=='__main__': unittest.main()
