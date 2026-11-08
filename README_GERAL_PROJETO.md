# A.R.C. – Adaptive Recognition & Control
## Desafios 05 a 10 | Estágio Supervisionado

Implementação inicial da prova de conceito A.R.C. para **webcam → detecção e rastreamento da mão → 21 landmarks desenhados na imagem**. O projeto **ainda não reconhece gestos nem executa comandos**. Os Desafios 9 e 10 adicionam tratamento de coordenadas e características geométricas exploratórias para subsidiar o reconhecimento futuro.

## O que está incluído

| Desafio | Implementação correspondente | Resultado a verificar |
|---|---|---|
| D5 – Ambiente e dependências | `requirements.txt`, `scripts/verificar_ambiente.py`, módulos organizados | Python 3.11, OpenCV, MediaPipe e NumPy instalados |
| D6 – Captura da webcam | `src/capture/camera.py`, modo `camera` | Vídeo em tempo real e tratamento de falha da câmera |
| D7 – Detecção de mãos | `src/tracking/hand_tracker.py`, modelo oficial MediaPipe | Estado “mão detectada” quando uma mão estiver visível |
| D8 – Visualização dos landmarks | `src/ui/landmarks.py`, modo `maos` | 21 pontos e conexões acompanhando o movimento da mão |
| D9 – Tratamento das coordenadas | `src/processing/coordinates.py` | 21 pontos validados, posições relativas ao punho e normalização pela palma |
| D10 – Características gestuais | `src/processing/features.py`, `src/ui/analysis.py`, modo `analise` | Distâncias e avaliação exploratória de extensão dos dedos |

**Validação já realizada:** no Windows da estudante, os modos `camera` e `maos` foram executados com sucesso, produzindo capturas reais e rastreando 1 mão com 21 landmarks; também foram executados **13 testes automatizados** com resultado `OK`. A nova versão D9/D10 ainda precisa de validação prática na webcam da estudante.

## 1. Instalação no Windows (PowerShell / terminal do VS Code)

> **Onde executar:** no terminal integrado do **VS Code**, de preferência com o perfil **PowerShell**. Abra a pasta que contém `README.md`, `requirements.txt`, `src/` e `scripts/`. O nome da pasta pode ser diferente do nome original (por exemplo, `ARC-FIRST`); o importante é executar os comandos na raiz do projeto.

### 1.1. Verificar a versão do Python

```powershell
py --list
py -3.11 --version
```

O A.R.C. foi configurado para usar **Python 3.11 (64 bits)**. No computador em que este projeto está sendo testado, a versão instalada foi **Python 3.11.9**.

Se `py -3.11 --version` mostrar `No suitable Python runtime found`, instale o Python 3.11 e abra um novo terminal:

```powershell
winget install --id Python.Python.3.11 -e
```

A instalação do Python 3.11 **não exige remover outras versões** do Python. Confirme novamente com `py -3.11 --version`.

### 1.2. Criar o ambiente virtual e instalar as dependências

Execute os comandos a seguir, **um por vez**:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se a instalação terminar com `Successfully installed`, a instalação das dependências foi concluída. Este projeto usa `opencv-contrib-python` em vez de instalar `opencv-python` simultaneamente, evitando conflitos entre pacotes que fornecem `cv2`.

**Não é obrigatório ativar a `.venv`:** os comandos já utilizam diretamente o Python do ambiente virtual e evitam os bloqueios de execução de scripts do PowerShell.

### 1.3. Verificar as bibliotecas e as APIs principais

```powershell
.\.venv\Scripts\python.exe scripts\verificar_ambiente.py
```

O verificador deve apresentar `[OK]` para OpenCV, MediaPipe, NumPy e importação das APIs principais. Antes de baixar o modelo, é normal aparecer:

```text
[PENDENTE] Modelo de mao. Execute: python scripts/baixar_modelo.py
Dependencias OK. O modelo e exigido somente no modo maos.
```

Isso **não significa que as bibliotecas falharam**. O modelo `.task` é necessário apenas para detectar e rastrear mãos.

### 1.4. Baixar o modelo oficial Hand Landmarker

Para o **modo de detecção de mãos** será necessário baixar o pacote `hand_landmarker.task` uma vez. Ele não está incluso no ZIP. Com conexão à internet:

```powershell
.\.venv\Scripts\python.exe scripts\baixar_modelo.py
```

Link oficial utilizado pelo script:

https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

Se ocorrer erro de download, abra o link no navegador, salve o arquivo com o nome **`hand_landmarker.task`** na pasta `models` e execute novamente o verificador de ambiente.

**Confirmar o download:**

```powershell
.\.venv\Scripts\python.exe scripts\verificar_ambiente.py
```

Com o modelo presente, deve aparecer uma linha semelhante a `[OK] Modelo localizado: hand_landmarker.task (...)`.

### 1.5. Registro real da configuração inicial (Desafio 5)

Os prints do terminal do VS Code fornecidos durante a configuração confirmam o seguinte **neste computador**:

| Item | Situação observada |
|---|---|
| Python | **3.11.9** instalado; versões 3.13 e 3.14 também estavam disponíveis |
| Ambiente virtual | `.venv` criada e utilizada pelos comandos do projeto |
| `opencv-contrib-python` | **4.14.0.94** — `[OK]` no verificador |
| `mediapipe` | **1.2.2** — `[OK]` no verificador |
| `numpy` | **2.4.6** — `[OK]` no verificador |
| APIs principais | `[OK] Importacao e APIs principais verificadas.` |
| Modelo `hand_landmarker.task` | **Baixado e salvo em `models/`**, com tamanho de **7.891.105 bytes** |

**Atualização:** além da configuração, foram realizados posteriormente os testes de webcam, detecção e landmarks; as imagens reais encontram-se na pasta `evidencias/` da estudante (não incluídas neste pacote). A verificação inicial deste item deve ser considerada em conjunto com essas evidências posteriores.

## 2. Executar os desafios

### D6 – Apenas captura da webcam (não precisa do arquivo `.task`)

Feche programas que possam estar usando a câmera, como Teams, Meet ou Zoom. No **terminal do VS Code**, execute:

```powershell
.\.venv\Scripts\python.exe src\main.py --modo camera
```

Resultado esperado: janela **`A.R.C. | Visao Computacional`** com a imagem ao vivo da webcam, sem pontos desenhados. Mova a mão diante da câmera para verificar a atualização do vídeo. Pressione **S** para registrar a imagem em `evidencias/`; pressione **Q** para fechar a janela de forma segura.

Se a webcam não abrir, confira as permissões do Windows e teste `--camera 1` em vez do índice padrão 0:

```powershell
.\.venv\Scripts\python.exe src\main.py --modo camera --camera 1
```

### D7 + D8 – Detectar a mão e desenhar landmarks

```powershell
.\.venv\Scripts\python.exe src\main.py --modo maos
```

Resultado esperado: ao mostrar uma mão diante da webcam, surge o indicador **`MAO DETECTADA`** e aparecem pontos e linhas sobre a mão. Ao retirar a mão, o estado muda para **`AGUARDANDO MAO`**. Não existe reconhecimento de gesto nesta versão.

- `Q` ou `Esc` – sair e liberar a webcam.
- `S` – salvar uma captura real na pasta `evidencias/`.
- Se tiver outra câmera, acrescente `--camera 1`.
- Para não espelhar o vídeo, acrescente `--sem-espelho`.

### Comandos adicionais

```powershell
.\.venv\Scripts\python.exe src\main.py --help
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 3. Checklist de testes manuais e evidências

Só marque após executar no seu computador:

- [x] **D5:** `py -3.11 --version` confirmou Python 3.11.9 (print apresentado).
- [x] **D5:** `scripts/verificar_ambiente.py` confirmou OpenCV, MediaPipe, NumPy e APIs principais (print apresentado).
- [x] **D5:** VS Code mostrou `src`, `capture`, `tracking`, `ui` e `scripts` (print apresentado).
- [x] **D5:** `scripts/baixar_modelo.py` salvou o arquivo `models/hand_landmarker.task` (print apresentado).
- [x] **D6:** modo `camera` abre a webcam e acompanha movimentos em vídeo (captura `arc_camera_20261108_004518.png`).
- [x] **D6:** `Q` fecha a aplicação e libera a câmera (terminal retornou ao prompt).
- [x] **D7:** modo `maos` detectou 1 mão (não houve ainda evidência separada do estado sem mão).
- [x] **D8:** foram exibidos 21 pontos e conexões sobre a mão na captura real. O acompanhamento durante movimento pode ser registrado em vídeo, se necessário.
- [x] **D8:** `S` salvou `arc_maos_20261108_004749.png` em `evidencias/`.
- [x] **Testes D5–D8:** 13 testes concluídos com `OK` (print `testesOk.png`). Os testes D9–D10 no PC ainda estão pendentes.

**Não apresente a figura ilustrativa de landmarks como evidência de funcionamento.** A evidência deve ser um print ou vídeo da sua aplicação executando com a sua webcam.

## 4. Estrutura do projeto

```text
ARC_Desafios_05_a_08/
├── src/
│   ├── main.py                      # Integra e executa os módulos
│   ├── config.py                    # Configurações iniciais
│   ├── capture/
│   │   └── camera.py                # D6 – Webcam e frames
│   ├── tracking/
│   │   └── hand_tracker.py          # D7 – MediaPipe Hand Landmarker
│   └── ui/
│       └── landmarks.py             # D8 – Pontos, linhas e status
├── scripts/
│   ├── verificar_ambiente.py        # D5 – Verificação técnica
│   └── baixar_modelo.py            # Baixar modelo oficial
├── models/                         # Colocar hand_landmarker.task aqui
├── tests/                          # Testes automatizados sem webcam
├── evidencias/                     # Capturas reais tiradas pelo aluno
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Justificativas técnicas

- **OpenCV (pacote `opencv-contrib-python`):** capta os frames da webcam, apresenta a janela e desenha os elementos sobre o vídeo.
- **MediaPipe Hand Landmarker:** detecta e acompanha a mão, fornecendo 21 landmarks em coordenadas normalizadas. Usa o modo `VIDEO`, que reaproveita informações entre frames para rastreamento.
- **NumPy:** oferece arrays para processamento de imagens e dados numéricos, integrando OpenCV e MediaPipe.
- **Uma mão:** mantém o escopo inicial pequeno e alinhado ao planejamento do estágio.
- **Estrutura modular:** captura, rastreamento e apresentação visual têm responsabilidades distintas, coerentes com a arquitetura preliminar aprovada.
- **Processamento local:** o vídeo da webcam não é enviado a um backend do A.R.C. O download inicial do modelo exige internet; a captura e a inferência são locais. Consulte a política do MediaPipe sobre métricas de uso da biblioteca.

## 6. Problemas comuns

**`py` não é reconhecido:** no Windows, instale o Python Launcher junto do Python 3.11, ou use o caminho para `python.exe` instalado.

**Nenhuma janela aparece:** execute a partir do Windows/VS Code (não em notebook na nuvem). Confira permissões de câmera em *Configurações → Privacidade e segurança → Câmera*.

**Webcam indisponível:** feche Teams, Zoom, navegador e outros apps que possam estar utilizando a câmera. Experimente `--camera 1`.

**Erro `Modelo nao encontrado`:** rode `scripts/baixar_modelo.py` ou coloque o `.task` em `models/`.

**Erro em `mediapipe` ou na versão:** verifique `scripts/verificar_ambiente.py`, reinstale as dependências na `.venv` e confirme que o terminal está usando `\.venv\Scripts\python.exe`.

**Detecção instável:** melhore a iluminação, mostre a mão inteira no quadro, evite movimentos bruscos e fundos muito semelhantes à pele. Essas variáveis serão avaliadas nas próximas etapas.

## 7. Referências técnicas

- [Google AI Edge – Hand Landmarker (Python)](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python)
- [Google AI Edge – Visão geral e modelo](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV – VideoCapture](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)
- [Python – venv](https://docs.python.org/3.11/library/venv.html)

## 8. Como usar os atalhos do Windows

Depois de instalar o ambiente, abra `INICIAR_CAMERA.bat` para testar o Desafio 6, ou `INICIAR_LANDMARKS.bat` para executar os Desafios 7 e 8. São atalhos para os comandos listados anteriormente.


## 9. Continuação — Desafios 9 e 10 (código implementado, evidências práticas registradas)

**Situação do acompanhamento:** vídeos do modo `analise` já foram enviados e analisados. Neles, a atualização das distâncias e o rastreamento estavam funcionando, com casos de falha na estimativa de extensão. A correção específica do polegar descrita na seção 11 **ainda não foi testada na webcam real**.

### Funcionalidades adicionadas

- **D9 — coordenadas:** valida as 21 posições `x, y, z`, rejeita NaN e infinitos, define o punho (ponto 0) como origem e normaliza as distâncias usando a largura da palma (pontos 5 e 17). Em posições extremas, utiliza o segmento 0–9 como alternativa. As medidas são **relativas**, não representam centímetros reais.
- **D10 — características:** calcula distâncias relativas como polegar–indicador (4–8), indicador–mindinho (8–20), ângulos de articulações e uma **estimativa heurística** de dedos estendidos. Essas medidas não são uma classificação de gestos. A perspectiva, iluminação, oclusão e orientação da mão podem influenciar os valores.
- **Modo `analise`:** une captura, rastreamento, landmarks e painel de características. Os modos anteriores continuam disponíveis.

### Executar no terminal do VS Code

Com a `.venv` e o modelo `models/hand_landmarker.task` já configurados:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\main.py --modo analise
```

Posicione **uma mão aberta** diante da webcam, observe a mudança dos indicadores e aproxime o polegar do indicador para ver a distância relativa diminuir. Pressione **S** para salvar a captura em `evidencias/` e **Q** para fechar. Anote os valores e compare pelo menos duas poses (aberta e polegar–indicador próximos).

**Evidências previstas:** `evidencias/arc_analise_*.png` com o painel visível; captura do terminal mostrando a saída final dos testes; descrição da variação observada das distâncias. Se a webcam não abrir, teste `--camera 1` e confira se outro aplicativo está usando o dispositivo.

**Checklist com base nas evidências recebidas:**

- [ ] Executar no seu computador os **47 testes** da versão com polegar e registrar o resultado. Os 47 testes passaram no ambiente de preparação.
- [x] Modo `analise` abriu com uma mão detectada e 21 landmarks (vídeos enviados).
- [x] Painel mostrou distâncias e indicadores em execução na webcam (vídeos enviados).
- [x] A distância polegar–indicador variou nas poses mostradas (vídeos enviados).
- [ ] Registrar novas capturas `arc_analise_*.png` com o polegar atualizado usando S.

### Como aplicar esta atualização à sua pasta `ARC-FIRST`

Se já configurou a `.venv` no VS Code, **não substitua a pasta inteira**. Copie os arquivos `src/` e `tests/` desta atualização para as pastas correspondentes do seu projeto. Substitua o `README.md` pelo desta versão. **Não exclua** `.venv`, `models/hand_landmarker.task` ou a pasta `evidencias/` com os seus prints. Não é necessária uma nova instalação das dependências.


## 10. Correção da estimativa de dedos estendidos (Desafio 10)

A primeira versão avaliava um ângulo `MCP–PIP–TIP` em 2D e comparava a distância da ponta ao punho, com limiar de 160°. Isso gerava falsos negativos em certas poses. A correção passa a avaliar **duas articulações de cada dedo** (`MCP–PIP–DIP` e `PIP–DIP–TIP`), usando `x, y, z` estimados pelo MediaPipe, e a projeção da ponta na direção do dedo. Também aplica um **filtro temporal de cinco quadros** para reduzir oscilações momentâneas.

**Escopo da versão anterior:** indicador, médio, anelar e mindinho. O polegar foi incluído na correção seguinte (seção 11), com regra específica. Os limiares são experimentais e poderão exigir calibração. Mesmo com essa correção, o resultado é uma **estimativa**, NÃO um reconhecedor de gestos pronto. Oclusões, mãos de lado, mudanças de profundidade e erros de landmarks podem afetar a leitura.

### Como instalar a correção no projeto que já funciona

Copie as pastas `src` e `tests` do ZIP de atualização para a raiz de seu `ARC-FIRST`, mesclando e substituindo apenas os arquivos com mesmo nome. Substitua também este `README.md`. **Não remova** `.venv/`, `models/hand_landmarker.task` nem `evidencias/`. Não é necessário reinstalar bibliotecas.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\main.py --modo analise
```

### Teste manual recomendado (webcam real)

1. Mostre a palma aberta, com os cinco dedos separados: após a inclusão do polegar (seção 11), esperamos `POL, IND, MED, ANE, MIN`, sujeito às limitações da estimativa. Pressione **S**.
2. Feche os quatro dedos: a lista deve diminuir ou indicar `nenhum`. Pressione **S**.
3. Estenda somente o indicador: idealmente aparece `IND`, mas a posição e o ângulo da mão afetam o resultado. Pressione **S**.
4. Aproxime polegar do indicador: a medida relativa `Dist. polegar-indicador` deve **diminuir**. Pressione **S**.
5. Vire suavemente a mão e observe se o indicador oscila menos. O filtro apresenta atraso intencional de poucos frames.
6. Pressione **Q** para sair. Compare os prints e anote quaisquer classificações incorretas.

**Se houver erros de classificação, não altere os limiares aleatoriamente:** envie os prints de pelo menos duas poses e podemos calibrar os critérios usando evidências.

### Situação dos testes

- Desafios 5–8: já validados com a webcam da estudante.
- Primeira versão de D9/D10: vídeo real recebido, com atualização coerente das distâncias e oscilação na estimativa de dedos.
- Correção D10 para os quatro dedos: vídeo real recebido; houve melhora clara, com limitações observadas em determinadas poses.
- Correção para incluir o polegar: **47 testes automatizados** passaram no ambiente de preparação; **teste com webcam da estudante pendente**.


## 11. Atualização — polegar na estimativa de extensão (D10)

A regra anterior incluía somente indicador, médio, anelar e mindinho. Esta atualização acrescenta o **polegar** com sua própria geometria: pontos **1 (CMC), 2 (MCP), 3 (IP), 4 (TIP)**. Calcula os ângulos `CMC–MCP–IP` e `MCP–IP–TIP` e duas medidas relativas à palma. Não reutiliza os limites geométricos dos demais dedos. O suavizador já existente filtra o resultado do polegar também.

O painel exibe **`Polegar: ESTENDIDO`** ou **`Polegar: RECOLHIDO`** e inclui **`POL`** quando o polegar está estimado como estendido. As medidas são relativas, não centímetros. **Isto é uma heurística**, não reconhecimento de gesto; em posições com o polegar sobreposto à palma ou em forte perspectiva, podem ocorrer falsos positivos/negativos.

### Aplicação na pasta do projeto em Windows

Feche o A.R.C. usando `Q`. Faça uma cópia da pasta `ARC-FIRST`. Extraia o ZIP de atualização e copie `src`, `tests` e `README.md` para dentro de `ARC-FIRST`, permitindo mesclar pastas e substituir os arquivos existentes. Não remova `.venv`, `models/hand_landmarker.task` nem suas imagens em `evidencias/`. Não é necessário reinstalar as bibliotecas.

### Testes automatizados

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Teste real da webcam

```powershell
.\.venv\Scripts\python.exe src\main.py --modo analise
```

1. **Mão aberta:** espere `POL, IND, MED, ANE, MIN` (a ordem pode variar por ajustes futuros).
2. **Punho fechado, com polegar recolhido:** espere `Polegar: RECOLHIDO` e redução da lista.
3. **Somente polegar levantado (positivo):** espere `Polegar: ESTENDIDO` e `POL` na lista.
4. **Somente indicador levantado:** espere `IND`, sem `POL` se o polegar estiver dobrado.
5. **Mova o polegar lateralmente:** observe se o estado muda conforme abre/fecha; o filtro temporal precisa de alguns quadros para estabilizar.

Use **S** para salvar imagens na pasta `evidencias/` e **Q** para encerrar. Registre casos em que a classificação não corresponda à posição real, para calibrarmos a heurística com sua webcam.

**Status:** os testes automatizados executados no ambiente de desenvolvimento verificam regras sintéticas. Os testes com a webcam real nesta nova versão ainda estão **pendentes**; não registre como concluídos antes da execução no seu computador.
