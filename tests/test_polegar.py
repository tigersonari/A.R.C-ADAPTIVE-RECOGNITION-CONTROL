"""Testes sintéticos do polegar (não substituem webcam)."""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from processing.coordinates import normalizar_landmarks
from processing.features import extrair_caracteristicas, estimar_polegar_estendido
from processing.temporal import EstabilizadorExtensao
from test_processamento import mao_teste


def trocar(pontos, alteracoes):
    p = [SimpleNamespace(x=q.x, y=q.y, z=q.z) for q in pontos]
    for indice, xyz in alteracoes.items():
        p[indice] = SimpleNamespace(x=xyz[0], y=xyz[1], z=xyz[2])
    return p


def fechar_polegar(pontos):
    # Polegar dobrado sobre a palma, ponta apontando na direção dos outros dedos.
    return trocar(pontos, {
        1:(.43,.77,0), 2:(.43,.73,0), 3:(.50,.71,0), 4:(.56,.70,0)
    })


def polegar_para_cima(pontos):
    # Estendido junto à lateral da mão (com os demais dedos arbitrários).
    return trocar(pontos, {
        1:(.43,.77,0), 2:(.41,.65,0), 3:(.40,.53,0), 4:(.40,.40,0)
    })


class TestesPolegar(unittest.TestCase):
    def extrair(self, pontos):
        return extrair_caracteristicas(normalizar_landmarks(pontos))

    def test_polegar_consta_da_lista(self):
        self.assertIn('polegar', self.extrair(mao_teste()).dedos_possivelmente_estendidos)

    def test_polegar_aberto(self):
        self.assertTrue(self.extrair(mao_teste()).dedos_possivelmente_estendidos['polegar'])

    def test_polegar_dobrado_na_palma(self):
        self.assertFalse(self.extrair(fechar_polegar(mao_teste())).dedos_possivelmente_estendidos['polegar'])

    def test_polegar_para_cima(self):
        self.assertTrue(self.extrair(polegar_para_cima(mao_teste())).dedos_possivelmente_estendidos['polegar'])

    def test_polegar_e_indicador_sao_independentes(self):
        p=fechar_polegar(mao_teste())
        f=self.extrair(p)
        self.assertFalse(f.dedos_possivelmente_estendidos['polegar'])
        self.assertTrue(f.dedos_possivelmente_estendidos['indicador'])

    def test_reflexo_horizontal_nao_altera_o_polegar(self):
        p=mao_teste()
        espelho=[SimpleNamespace(x=1-q.x, y=q.y, z=q.z) for q in p]
        self.assertEqual(self.extrair(p).dedos_possivelmente_estendidos['polegar'],
                         self.extrair(espelho).dedos_possivelmente_estendidos['polegar'])

    def test_escala_e_translacao_nao_alteram_o_polegar(self):
        p=mao_teste()
        alterados=[SimpleNamespace(x=.1+.8*q.x, y=.2+.8*q.y, z=.8*q.z) for q in p]
        self.assertEqual(self.extrair(p).dedos_possivelmente_estendidos['polegar'],
                         self.extrair(alterados).dedos_possivelmente_estendidos['polegar'])

    def test_landmarks_do_polegar_degenerados_nao_travam(self):
        p=mao_teste()
        p=trocar(p,{2:(.43,.77,0),3:(.43,.77,0),4:(.43,.77,0)})
        f=self.extrair(p)
        self.assertFalse(f.dedos_possivelmente_estendidos['polegar'])

    def test_polegar_mantem_estabilidade_em_um_quadro_ruidoso(self):
        f=self.extrair(mao_teste())
        filtro=EstabilizadorExtensao(janela=5)
        for _ in range(5):
            s=filtro.atualizar(f)
        self.assertTrue(s.dedos_possivelmente_estendidos['polegar'])
        falha=replace(f,dedos_possivelmente_estendidos={**f.dedos_possivelmente_estendidos,'polegar':False})
        s=filtro.atualizar(falha)
        self.assertTrue(s.dedos_possivelmente_estendidos['polegar'])

    def test_polegar_eh_inserido_em_angulos_dedos(self):
        f=self.extrair(mao_teste())
        self.assertIn('polegar',f.angulos_dedos)
        self.assertIsNotNone(f.angulos_dedos['polegar'])

if __name__=='__main__':
    unittest.main()
