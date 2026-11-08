# GUIA PARA EVIDÊNCIAS – DESAFIOS 5 A 8

Não considere cada desafio realizado antes de executar seus testes no computador da estudante.

## D5 – Configuração do ambiente
**Objetivo:** ambiente Python 3.11, bibliotecas, pastas e dependências.
**Registrar:** captura do `py -3.11 --version`, tela do `verificar_ambiente.py` e pastas no VS Code.
**Texto de relatório sugerido:** “Foi configurado um ambiente virtual Python e instaladas as dependências do protótipo. A estrutura inicial foi organizada para separar a captura, o rastreamento e a apresentação visual. As versões instaladas estão registradas na evidência anexada.”

## D6 – Captura de vídeo
**Objetivo:** abrir webcam, capturar e exibir frames em tempo real.
**Registrar:** print do modo `camera`; opcionalmente vídeo curto movimentando a mão. Testar a tecla Q.
**Texto de relatório sugerido:** “Foi implementada a captura contínua por OpenCV com tratamento de falha de acesso à câmera e liberação de recursos. O teste demonstrou a exibição de frames capturados em tempo real.”

## D7 – Detecção de mãos
**Objetivo:** integrar MediaPipe Hand Landmarker em vídeo.
**Registrar:** print ou vídeo de `MAO DETECTADA` e depois `AGUARDANDO MAO`.
**Texto de relatório sugerido:** “Foi integrado o Hand Landmarker em modo VIDEO, com limite de uma mão e processamento local. Durante o teste, o estado de detecção foi exibido conforme a presença da mão no enquadramento.”

## D8 – Landmarks
**Objetivo:** representar os 21 pontos e suas conexões sobre a mão em movimento.
**Registrar:** imagem em `evidencias/arc_maos_*.png` criada com S e gravação de movimento, se disponível.
**Texto de relatório sugerido:** “Foram desenhados os pontos e as conexões da mão sobre os frames capturados, permitindo observar visualmente seu acompanhamento durante o movimento.”

## Observação
Os parágrafos acima são **modelos condicionais**. Só use o verbo no passado após o teste ter sido feito e comprovado.

| Desafio | Testado no PC? | Evidência | Problemas/ajustes |
|---|---|---|---|
| D5 | A preencher | A preencher | A preencher |
| D6 | A preencher | A preencher | A preencher |
| D7 | A preencher | A preencher | A preencher |
| D8 | A preencher | A preencher | A preencher |


## Evidências já fornecidas na conversa (execução real no PC)
- **D5:** `bibliotecasInstaladas.png` e `landmarksInstalado.png` mostram verificação OK e download do modelo.
- **D6:** `arc_camera_20261108_004518.png` e `arc_camera_20261108_004522.png` aparecem em `evidencias/`; janela mostrou CAPTURA OK e ~31,5 FPS.
- **D7/D8:** `arc_maos_20261108_004749.png` mostra 1 mão e 21 landmarks, aproximadamente 31,6 FPS.
- **Testes D5–D8:** `testesOk.png` mostra `Ran 13 tests ... OK`.

## D9 e D10: evidências ainda pendentes do computador
Abrir `--modo analise`; mostrar pelo menos duas posições da mão e registrar a distância polegar–indicador mudando. Registrar um print `arc_analise_*.png` com tecla S e um print dos novos testes automatizados. Os resultados de testes simulados não substituem a validação real com webcam.


## Correção D10 — Novo teste de estabilidade

Registrar 3 ou 4 prints reais de `--modo analise`: palma aberta, dedos recolhidos, só indicador estendido e pinça polegar–indicador. Documentar as estimativas no painel, diferenças observadas e, se houver, classificações incorretas. Não declarar a correção validada antes dos prints/testes na webcam da estudante.


## Atualização de evidências — polegar (Desafio 10)

- Teste 1: mão aberta e lista `POL, IND, MED, ANE, MIN` (ou anote divergências).
- Teste 2: polegar recolhido, com a linha `Polegar: RECOLHIDO`.
- Teste 3: sinal de positivo (só polegar), com `Polegar: ESTENDIDO` e `POL`.
- Teste 4: apenas indicador, para verificar que a estimativa de polegar não gera falso positivo.
- Salve capturas com **S** dentro de `evidencias/`. Anote qualquer divergência entre pose real e painel.
- A correção do polegar ainda não foi validada com a webcam real. Os testes simulados confirmam apenas os cenários sintéticos.
