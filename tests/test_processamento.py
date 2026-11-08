"""Testes sintéticos das regras geométricas D9 e D10: não testam a webcam."""
import math
import sys
from pathlib import Path
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from processing.coordinates import normalizar_landmarks
from processing.features import distancia, angulo_graus, extrair_caracteristicas


def mao_teste():
    p = [SimpleNamespace(x=0.5, y=0.7, z=0.0) for _ in range(21)]
    # Palmar MCPs: 5 a 17, escala horizontal 0.30.
    dados = {
        0:(0.50,0.90), 1:(0.43,0.77),2:(0.35,0.66),3:(0.30,0.61),4:(0.25,0.55),
        5:(0.35,0.68),6:(0.35,0.55),7:(0.35,0.43),8:(0.35,0.35),
        9:(0.45,0.65),10:(0.45,0.51),11:(0.45,0.39),12:(0.45,0.31),
        13:(0.55,0.66),14:(0.55,0.53),15:(0.55,0.42),16:(0.55,0.34),
        17:(0.65,0.69),18:(0.65,0.58),19:(0.65,0.49),20:(0.65,0.43),
    }
    for i,(x,y) in dados.items(): p[i] = SimpleNamespace(x=x,y=y,z=0.0)
    return p

class TestesCoordenadas(unittest.TestCase):
    def test_mantem_21_pontos(self):
        self.assertEqual(len(normalizar_landmarks(mao_teste()).pontos),21)
    def test_punho_vira_origem(self):
        self.assertEqual(normalizar_landmarks(mao_teste()).pontos[0],(0,0,0))
    def test_normaliza_pela_largura_palma(self):
        mao=normalizar_landmarks(mao_teste())
        self.assertAlmostEqual(distancia(mao.pontos[5],mao.pontos[17]),1.0)
    def test_rejeita_quantidade_incorreta(self):
        with self.assertRaises(ValueError): normalizar_landmarks(mao_teste()[:20])
    def test_rejeita_nan(self):
        p=mao_teste();p[6].x=float('nan')
        with self.assertRaises(ValueError): normalizar_landmarks(p)
    def test_fallback_escala(self):
        p=mao_teste();p[17]=SimpleNamespace(x=p[5].x,y=p[5].y,z=0)
        self.assertGreater(normalizar_landmarks(p).escala_palma,0)
    def test_falha_escala_zero(self):
        p=[SimpleNamespace(x=0.5,y=0.5,z=0) for _ in range(21)]
        with self.assertRaises(ValueError): normalizar_landmarks(p)

class TestesCaracteristicas(unittest.TestCase):
    def test_distancia_conhecida(self):
        self.assertAlmostEqual(distancia((0,0),(3,4)),5)
    def test_angulo_reto(self):
        self.assertAlmostEqual(angulo_graus((1,0),(0,0),(0,1)),90)
    def test_segmento_degenerado(self):
        self.assertIsNone(angulo_graus((0,0),(0,0),(1,2)))
    def test_caracteristicas_da_mao_aberta(self):
        feat=extrair_caracteristicas(normalizar_landmarks(mao_teste()))
        self.assertGreater(feat.distancia_polegar_indicador,0)
        self.assertEqual(set(feat.angulos_dedos),{'polegar','indicador','medio','anelar','mindinho'})
        self.assertTrue(feat.dedos_possivelmente_estendidos['indicador'])
    def test_translacao_nao_muda_distancia_relativa(self):
        p1=mao_teste()
        p2=[SimpleNamespace(x=p.x+0.1,y=p.y-0.2,z=p.z) for p in p1]
        f1=extrair_caracteristicas(normalizar_landmarks(p1))
        f2=extrair_caracteristicas(normalizar_landmarks(p2))
        self.assertAlmostEqual(f1.distancia_polegar_indicador,
                               f2.distancia_polegar_indicador)

if __name__=='__main__': unittest.main()
