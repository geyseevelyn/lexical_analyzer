# Analisador Léxico para a linguagem TONTO

Este projeto implementa um **analisador léxico** para a linguagem [*TONTO*](https://matheuslenke.github.io/tonto-docs/docs/intro), utilizando **Python** e a biblioteca **PLY (Python Lex-Yacc)**. O objetivo é reconhecer e classificar os elementos dessa linguagem, produzindo uma tabela de símbolos e uma contagem de *tokens* como saída.

---

## 📋 Tabela de Conteúdos
<!--ts-->
   * [A Linguagem TONTO](#-a-linguagem-tonto)
   * [Sobre o Projeto](#-sobre-o-projeto)
   * [Tecnologias Utilizadas](#-tecnologias-utilizadas)
   * [Funcionalidades](#-funcionalidades)
   * [Especificação dos Tokens](#-especificação-dos-tokens-reconhecidos)
   * [Como Usar](#-como-usar)
   * [Autores](#-autores)
   * [Licença](#-licença)
<!--te-->

---

## 📖 A Linguagem TONTO

A **TONTO** (*Textual Ontology Language*) é uma linguagem textual para modelagem de ontologias, desenvolvida por **Matheus Lenke Coutinho**. Criada com o objetivo de superar limitações das linguagens de modelagem puramente visuais, ela permite a **edição**, **validação** e **versionamento** de ontologias por meio de **código textual** e também a **conversão** para outros para outros formatos como:

- *OntoUML*
- *gUFO (OWL)*
- *JSON*

També,m possui extensão para o **VSCode**, permitindo criar módulos `.tonto`, gerenciar dependências com o **Tonto Package Manager** e gerar modelos interoperáveis com o **Protégé** e o **Visual Paradigm**.

💡 Para mais informações sobre a lingaugem, consulte a [documentação oficial](https://matheuslenke.github.io/tonto-docs/docs/intro), a [monografia completa](https://matheuslenke.github.io/tonto-docs/pdf/Tonto.pdf) e o [repositório oficial no GitHub](https://github.com/matheuslenke/Tonto).

---

## 📖 Sobre o Projeto

O **Analisador Léxico para a linguagem TONTO** foi desenvolvido como parte de um estudo prático sobre a construção de compiladores e ferramentas de análise léxica. O projeto tem como objetivo o reconhecimento e categorização dos seguintes elementos da linguagem **TONTO**:

- **Palavras reservadas**;
- **Estereótipos de classe**;
- **Estereótipos de relações**;
- **Nomes de classes**;
- **Nomes de relações**;
- **Nomes de instâncias**;
- **Tipos de dados nativos**;
- **Novos tipos de dados**; 
- **Meta-atributos**;
- **Símbolos especias**.

Além desses elementos previamente especificados na descrição do trabalho, o analisador léxico **também reconhece**:

- **Nomes de pacotes**;
- ***Generalization sets (gensets)***;
- **Atributos**;
- **Enumerações**;
- **Cardinalidades**.

O resultado consiste em **relatórios detalhados** sobre os *tokens* encontrados, permitindo uma base sólida para **análise sintática** ou **semântica** posterior.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**;
- **PLY** (Python Lex-Yacc)
- **TONTO** (Extensão do *VS Code*, *Tonto CLI* e *Tonto Package Manager*).

---

## ✨ Funcionalidades

- **Reconhecimento de Tokens:** reconhece e categoriza os *tokens* válidos da linguagem **TONTO** (citados na seção [**Sobre o Projeto**](#-sobre-o-projeto));

- **Geração de Tabela de Símbolos:** organiza e exibe todos os *tokens* identificados;

- **Contador de *Tokens*:** gera uma tabela de síntese com contagens de categorias léxicas;

- **Registro de Erros Léxicos:** detecta e lista *tokens* inválidos encontrados durante o processamento;

- **Menu Interativo:** permite a navegação e visualização de resultados.

---

## 🔤 Especificação dos *Tokens*

A **especificação detalhada** dos *tokens* da linguagem **TONTO** reconhecidos e categorizados pelo analisador léxico pode ser encontrada nesse [documento](docs/tokens_tonto_details.md). 

---

## 🚀 Como Usar

### Pré-requisitos 

- [Python 3.10+](https://www.python.org/downloads/);
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/);
- [TONTO](https://matheuslenke.github.io/tonto-docs/docs/intro-installling)

### Instalação

1. Clone o repositório ou baixe o arquivo ZIP:

   ```bash
   git clone https://github.com/geyseevelyn/lexical_analyzer.git
   ```

2. Acesse a pasta do projeto:

   ```bash
   cd lexical_analyzer
   ```

3. Instale a dependência necessária (PLY):

   ```bash
   pip install ply
   ```

### Execução

1. Já na pasta do projeto, mude para a pasta `src`:

   ```bash
   cd src
   ```

2. Execute o código:

   ```bash
   python main.py
   ```

3. Na **menu interativo**, escolha uma opção:
   - **Opção 1**: Digitar o caminho completo do arquivo `.tonto` no seu computador.
   - **Opção 2**: Listar e escolher um arquivo `.tonto` da pasta `examples`).

4. Após selecionar o arquivo, o programa vai processar e abrir o menu principal com opções para:

   - Exibir os tokens processados
   - Exibir a tabela de símbolos
   - Exibir a contagem de tokens
   - Analisar outro arquivo
   - Sair

### Usando os exemplos prontos
- O projeto já inclui exemplos em `src\examples`. Você pode escolher a **Opção 2** quando o programa pedir e selecionar um arquivo da lista, por exemplo:
  - `CarExample\src\car.tonto`
  - `FoodAllergyExample\src\alergiaalimentar.tonto`
  - `TDAHExample\src\TDAH.tonto`

### Usando seu próprio arquivo
1. Tenha um arquivo com a extensão `.tonto` salvo no seu computador.
2. Execute o programa (`python src\main.py`).
3. Escolha a **Opção 1** e cole o caminho completo do arquivo, por exemplo:
   - `C:\Users\seu_usuario\Documents\meu_arquivo.tonto`

---

## 👨‍💻 Autores

- [Geyse Evelyn](https://github.com/geyseevelyn)
- [Ivanildo Junior](https://github.com/jrsilva95)

---

## 📜 Licença
Este projeto está sob a licença *MIT*. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

<div align="center">
    <a href="https://github.com/geyseevelyn/lexical_analyzer?tab=readme-ov-file#analisador-l%C3%A9xico-para-a-linguagem-tonto">Voltar ao topo</a>
</div>