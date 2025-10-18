# lexical_analyzer

Um analisador léxico simples para arquivos .tonto. Ele lê o conteúdo de um arquivo, identifica tokens (como identificadores, inteiros e cadeias de texto) e mantém uma tabela de símbolos e uma contagem de tokens. O projeto usa a biblioteca PLY (Python Lex-Yacc) para construir o lexer e oferece um menu interativo no terminal para visualizar os resultados.

## Requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação
1. Abra o Terminal (PowerShell no Windows).
2. Vá até a pasta do projeto:
   - Exemplo:
     - `cd C:\Users\seu_usuario\PycharmProjects\lexical_analyzer`
3. (Opcional) Crie e ative um ambiente virtual:
   - Criar: `python -m venv .venv`
   - Ativar: `.venv\Scripts\Activate`
4. Instale a dependência necessária (PLY):
   - `pip install ply`

## Como executar
1. No Terminal (dentro da pasta do projeto), execute:
   - `python src\main.py`
2. Na tela inicial, escolha uma opção:
   - Opção 1: Digitar o caminho completo de um arquivo `.tonto` no seu computador.
   - Opção 2: Escolher um arquivo de exemplo que já vem no projeto.
3. Após escolher o arquivo, o programa vai processar e abrir um menu com opções para:
   - Exibir os tokens processados
   - Exibir a tabela de símbolos
   - Exibir a contagem de tokens
   - Processar outro arquivo
   - Sair

## Usando os exemplos prontos
- O projeto já inclui exemplos em `src\examples`. Você pode escolher a Opção 2 quando o programa pedir e selecionar um arquivo da lista, por exemplo:
  - `CarExample\src\car.tonto`
  - `FoodAllergyExample\src\alergiaalimentar.tonto`
  - `TDAHExample\src\TDAH.tonto`

## Usando seu próprio arquivo
1. Tenha um arquivo com a extensão `.tonto` salvo no seu computador.
2. Execute o programa (`python src\main.py`).
3. Escolha a opção 1 e cole o caminho completo do arquivo, por exemplo:
   - `C:\Users\seu_usuario\Documents\meu_arquivo.tonto`

## Dicas e solução de problemas
- Erro “ModuleNotFoundError: No module named 'ply'”:
  - Execute `pip install ply` e tente novamente.
- Se o comando `python` abrir a Microsoft Store ou não funcionar:
  - Tente `py` no lugar de `python` (ex.: `py src\main.py`).
- Se estiver usando ambiente virtual e o comando não for reconhecido:
  - Ative o ambiente com `.venv\Scripts\Activate` antes de rodar os comandos.

## Licença
Consulte o arquivo LICENSE para mais detalhes.