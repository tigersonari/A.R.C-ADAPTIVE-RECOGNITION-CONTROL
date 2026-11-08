# A.R.C. — Adaptive Recognition & Control

**Protótipo de interface gestual baseada em visão computacional**  
Projeto acadêmico de Estágio Supervisionado — Sistemas de Informação | UNITINS | 2026

> **Estado do desenvolvimento:** atividades técnicas dos **Desafios 5 a 10**, abrangendo configuração, captura de vídeo, detecção de uma mão, visualização de 21 landmarks, tratamento de coordenadas e extração de características geométricas. **Ainda não há classificação de gestos completos nem execução de comandos por gesto** (etapas posteriores).

## Sumário

1. [Visão geral e recursos](#1-visão-geral-e-recursos)
2. [Requisitos](#2-requisitos)
3. [Instalação completa no Windows](#3-instalação-completa-no-windows)
4. [Como executar a aplicação](#4-como-executar-a-aplicação)
5. [Testes automatizados](#5-testes-automatizados)
6. [Estrutura dos arquivos](#6-estrutura-dos-arquivos)
7. [Evidências e resultados](#7-evidências-e-resultados)
8. [Solução de problemas](#8-solução-de-problemas)
9. [Limitações e próximos passos](#9-limitações-e-próximos-passos)
10. [Referências](#10-referências)

## 1. Visão geral e recursos

O A.R.C. utiliza **OpenCV** para capturar frames da webcam e apresentar a interface; **MediaPipe Hand Landmarker** para detectar/rastrear uma mão e produzir **21 pontos de referência**; e rotinas próprias em **Python** para validar, normalizar e analisar coordenadas.

| Desafio | Módulo / funcionalidade | Situação observada |
|:--|:--|:--|
| **05** — Ambiente | Python 3.11, ambiente virtual, instalação e verificação de dependências | Verificado no Windows da desenvolvedora |
| **06** — Captura | Webcam em tempo real com OpenCV, modo `camera` | Validado com captura real |
| **07** — Detecção | Hand Landmarker no modo de vídeo, uma mão | Validado com uma mão detectada |
| **08** — Landmarks | Desenho dos 21 pontos e suas conexões, modo `maos` | Validado com sobreposição real |
| **09** — Coordenadas | Verificação e normalização de `x`, `y` e `z` relativas à palma | Implementado e observado em execução |
| **10** — Características | Distâncias relativas, ângulos, estimativa de dedos estendidos (inclusive polegar), filtro temporal | Testado com várias poses; sujeito a erros de perspectiva |

**Tecnologias:** Python 3.11, `opencv-contrib-python`, `mediapipe==1.2.2`, NumPy, `unittest` (biblioteca padrão). O arquivo `requirements.txt` contém as restrições de versões.

O processamento das imagens da câmera ocorre localmente. O modelo `.task` deve ser baixado separadamente na primeira configuração.

## 2. Requisitos

- Computador **Windows 10 ou 11 (64 bits)** com **webcam** e permissão de acesso à câmera.
- **Python 3.11 (64 bits)** e Python Launcher (`py`). A versão **3.11.9** foi utilizada na validação inicial.
- Terminal PowerShell do VS Code, PowerShell do Windows ou CMD (os comandos abaixo são de **PowerShell**).
- Acesso à internet **na primeira instalação** para instalar bibliotecas e baixar o modelo oficial.
- Espaço suficiente para instalar as bibliotecas e o modelo.

**Importante:** não instale o programa dentro da pasta `.venv` e não execute os comandos a partir de `src`. Abra no VS Code **a pasta raiz**, que contém `README.md`, `requirements.txt`, `scripts/` e `src/`.

## 3. Instalação completa no Windows

### 3.1. Baixe e abra o projeto

1. No GitHub, selecione **Code → Download ZIP** e extraia o arquivo; alternativamente, clone o repositório com Git.
2. No VS Code, clique em **Arquivo → Abrir Pasta** e selecione a pasta extraída, onde aparece `requirements.txt`.
3. Clique em **Terminal → Novo Terminal** e use o PowerShell. Os comandos a seguir devem ser executados **nessa pasta**.

### 3.2. Verifique o Python

```powershell
py --list
py -3.11 --version
```

O segundo comando deve responder `Python 3.11.x`.

Se aparecer `No suitable Python runtime found`, instale o Python 3.11 sem remover outras versões:

```powershell
winget install --id Python.Python.3.11 -e
```

Feche e reabra o terminal antes de repetir `py -3.11 --version`.

### 3.3. Crie o ambiente virtual

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe --version
```

O diretório `.venv` será criado localmente. **Não é necessário ativá-lo**, porque os comandos usam diretamente seu executável Python. Isso evita bloqueios de execução de scripts do PowerShell.

### 3.4. Instale as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

A instalação deve terminar sem erros; o `requirements.txt` instala as bibliotecas de processamento e rastreamento. Não instale `opencv-python` em paralelo com `opencv-contrib-python` sem necessidade, pois ambos fornecem `cv2`.

### 3.5. Verifique as bibliotecas

```powershell
.\.venv\Scripts\python.exe scripts\verificar_ambiente.py
```

Espere linhas `[OK]` para OpenCV, MediaPipe, NumPy e importação das APIs principais. **Antes do download do modelo**, a indicação `[PENDENTE] Modelo de mao` é normal e não significa que as bibliotecas falharam.

### 3.6. Baixe o modelo Hand Landmarker

```powershell
.\.venv\Scripts\python.exe scripts\baixar_modelo.py
```

O script baixa o modelo oficial do Google AI Edge e o grava em `models/hand_landmarker.task`. O download é necessário para os modos `maos` e `analise` e não precisa ser repetido se o modelo já estiver presente.

**Verifique novamente:**

```powershell
.\.venv\Scripts\python.exe scripts\verificar_ambiente.py
```

Desta vez, deve aparecer `[OK] Modelo localizado: hand_landmarker.task (...)`.

> **Por que o modelo não está no GitHub?** É um arquivo externo de inferência que pode ser obtido novamente pelo script, por isso `models/*.task` consta no `.gitignore`.

## 4. Como executar a aplicação

Abra o terminal na raiz do projeto. Há três modos independentes:

| Modo | Comando | O que aparece |
|:--|:--|:--|
| **Captura** (D6) | `.\.venv\Scripts\python.exe src\main.py --modo camera` | Vídeo da webcam, FPS e indicação de captura. Não executa detecção; `Mãos: 0` é esperado. |
| **Mãos** (D7–D8) | `.\.venv\Scripts\python.exe src\main.py --modo maos` | Mão detectada, 21 landmarks e conexões sobre os frames. |
| **Análise** (D9–D10) | `.\.venv\Scripts\python.exe src\main.py --modo analise` | Landmarks, escala relativa da palma, distâncias e estimativa dos cinco dedos (`POL`, `IND`, `MED`, `ANE`, `MIN`). |

**Teste por etapas:**

**Etapa A — Webcam:**

```powershell
.\.venv\Scripts\python.exe src\main.py --modo camera
```

**Etapa B — Detecção e 21 pontos:**

```powershell
.\.venv\Scripts\python.exe src\main.py --modo maos
```

**Etapa C — Coordenadas e características:**

```powershell
.\.venv\Scripts\python.exe src\main.py --modo analise
```

Na janela do aplicativo:

- **S:** salva o frame anotado como `evidencias/arc_<modo>_AAAAMMDD_HHMMSS.png`.
- **Q** ou **Esc:** encerra a aplicação e libera a câmera.
- **Movimente a mão** diante da webcam para verificar o acompanhamento dos pontos e a atualização das medidas.

Opções adicionais:

```powershell
# Quando a câmera padrão (índice 0) não abre
.\.venv\Scripts\python.exe src\main.py --modo analise --camera 1

# Exibir a imagem sem espelhamento horizontal
.\.venv\Scripts\python.exe src\main.py --modo analise --sem-espelho
```

**Atalhos do Windows:** `INICIAR_CAMERA.bat` e `INICIAR_LANDMARKS.bat` executam os modos respectivos após a instalação. O modo `analise` é iniciado pelo terminal, como acima.

### Como interpretar o modo `analise`

- **`Mãos: 1 | Pontos: 21`:** uma mão detectada e o esqueleto desenhado.
- **`Escala palma`:** largura relativa usada para normalizar as coordenadas; não é uma medida em centímetros.
- **`Dist. polegar-indicador`:** distância relativa entre os landmarks 4 e 8; em geral, diminui quando as pontas se aproximam.
- **`Dist. indicador-mindinho`:** distância relativa entre os landmarks 8 e 20.
- **`Polegar: ESTENDIDO/RECOLHIDO`:** estimativa geométrica baseada em suas articulações.
- **`POL, IND, MED, ANE, MIN`:** dedos estimados como estendidos, **não** nomes de gestos reconhecidos.

As medidas e as estimativas podem sofrer variações por perspectiva, oclusão, iluminação e posição da mão. Um filtro temporal usa uma janela de cinco quadros para estabilizar a indicação de extensão.

## 5. Testes automatizados

O projeto usa testes `unittest` para verificar câmera simulada, integração, desenho dos landmarks, validação/normalização, características e extensão do polegar.

Execute na raiz:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Resultado da versão atual do código na verificação de desenvolvimento:**

```text
Ran 47 tests in ...s

OK
```

O número de segundos pode variar. Caso altere o código, teste novamente e verifique se continua com `OK`.

**Registro de validação:** uma versão inicial de 13 testes também foi executada no Windows da desenvolvedora, com `OK`; o conjunto expandido de 47 testes foi verificado no ambiente de desenvolvimento antes da publicação. A aprovação dos testes automatizados não elimina a necessidade de verificar a webcam real.

## 6. Estrutura dos arquivos

```text
ARC/
├── README.md                        # Instruções gerais (este documento)
├── requirements.txt                 # Dependências
├── .gitignore                       # Proteção de arquivos locais/pessoais
├── INICIAR_CAMERA.bat               # Atalho para o modo camera
├── INICIAR_LANDMARKS.bat            # Atalho para o modo maos
├── scripts/
│   ├── verificar_ambiente.py        # Diagnóstico do ambiente
│   └── baixar_modelo.py             # Download do modelo externo
├── src/
│   ├── main.py                      # Aplicação e argumentos da linha de comando
│   ├── config.py                    # Configurações e caminhos
│   ├── capture/camera.py            # Webcam
│   ├── tracking/hand_tracker.py     # MediaPipe Hand Landmarker
│   ├── ui/landmarks.py              # Esqueleto e indicadores do frame
│   ├── ui/analysis.py               # Painel de análise geométrica
│   └── processing/
│       ├── coordinates.py           # Normalização de landmarks
│       ├── features.py              # Medidas e estimativas de dedos
│       └── temporal.py              # Suavização da estimativa
├── models/
│   └── LEIA-ME.txt                  # O .task é baixado localmente
├── evidencias/
│   └── LEIA-ME.txt                  # Prints locais (ignorados no Git)
├── tests/                            # Testes automatizados
└── docs/
    ├── GUIA_DE_EXECUCAO.md          # Checklist prático resumido
    └── GUIA_PUBLICACAO_GITHUB.md    # Envio/atualização do repositório
```

## 7. Evidências e resultados

Nas verificações realizadas até agora:

- **D5:** Python 3.11.9; OpenCV 4.14.0.94; MediaPipe 1.2.2; NumPy 2.4.6; APIs verificadas e modelo oficial baixado.
- **D6:** webcam exibiu `CAPTURA OK`, com FPS em torno de 31,5 no registro apresentado; imagens foram salvas com `S`.
- **D7 e D8:** detecção de uma mão e sobreposição de **21 landmarks**, aproximadamente 31,6 FPS no registro apresentado.
- **D9 e D10:** vídeos de execução mostraram atualização de medidas geométricas e da estimativa de extensão dos dedos. Após ajustes, foram observados casos de mão aberta (`POL, IND, MED, ANE, MIN`), mão fechada (`nenhum`) e outras combinações. Isso valida os exemplos testados, **não todas as possíveis poses**.
- **Testes automatizados:** 13 testes aprovados no Windows em uma versão anterior; **47 testes aprovados** na versão atual durante verificação de desenvolvimento.

**Privacidade:** os prints originais podem mostrar o rosto e o ambiente da desenvolvedora. Para evitar a publicação acidental dessas imagens em repositórios públicos, o `.gitignore` impede o envio automático de imagens e vídeos em `evidencias/`. Não publique imagens de outras pessoas sem permissão; se desejar disponibilizar evidências, selecione e edite previamente versões apropriadas.

## 8. Solução de problemas

| Problema | Como resolver |
|:--|:--|
| `No suitable Python runtime found` | Use `py --list`; instale o Python 3.11 e abra novo terminal. |
| `python` errado ou bibliotecas ausentes | Use **sempre** `.\.venv\Scripts\python.exe` e reinstale com `-m pip install -r requirements.txt`. |
| `ModuleNotFoundError` | Verifique se a instalação terminou e se o ambiente virtual foi criado na pasta correta. |
| `Modelo nao encontrado` | Execute `scripts\baixar_modelo.py` ou salve manualmente `hand_landmarker.task` em `models/`. |
| Webcam não abre | Feche Meet/Zoom/Teams, permita o uso da câmera no Windows e tente `--camera 1`. |
| Janela não aparece ou fecha logo | Execute pelo terminal do VS Code para visualizar o erro; use o Windows com ambiente gráfico. |
| `Mãos: 0` em `camera` | Normal: este modo **não executa** a detecção. |
| `Mãos: 0` em `maos` / `analise` | Mostre a palma inteira, aumente a iluminação e diminua movimentos bruscos. |
| Estimativa dos dedos incorreta | Verifique se os 21 pontos acompanham a mão; teste outra orientação e evite oclusões; critérios ainda experimentais. |
| Avisos `W0000` do MediaPipe | Podem ser avisos internos; se a câmera funciona e há landmarks, não indicam necessariamente falha. |
| PowerShell bloqueia `Activate.ps1` | Não precisa ativar: use o caminho direto `.\.venv\Scripts\python.exe`. |

## 9. Limitações e próximos passos

**Limitações atuais:** rastreamento inicialmente de **uma mão**, análise heurística de extensão, medições relativas sem escala física e dependência da qualidade dos landmarks. Não há treinamento de modelo próprio, banco de dados, backend, controle de aplicações externas nem recursos 3D de interação espacial.

**Próximas atividades previstas:** definir um conjunto pequeno de gestos experimentais (Desafio 11), implementar regras de reconhecimento (Desafio 12), associar gestos reconhecidos a comandos demonstrativos (Desafio 13), realizar testes/ajustes (Desafio 14) e consolidar evidências/documentação (Desafio 15).

## 10. Referências

- [Google AI Edge — Hand Landmarker para Python](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python)
- [MediaPipe — Modelos Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV — VideoCapture](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)
- [Python 3.11 — Ambientes virtuais (`venv`)](https://docs.python.org/3.11/library/venv.html)

---

**A.R.C. — Adaptive Recognition & Control** · Desenvolvimento incremental de uma prova de conceito acadêmica em visão computacional.
