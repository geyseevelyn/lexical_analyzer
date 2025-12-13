
# Analisador Léxico para a Linguagem TONTO

Este projeto implementa um **analisador léxico** para a linguagem [*TONTO*](https://matheuslenke.github.io/tonto-docs/docs/intro), utilizando **Python** e a biblioteca **PLY (Python Lex-Yacc)**. O objetivo é reconhecer e classificar os elementos dessa linguagem, produzindo uma tabela de símbolos e uma contagem de *tokens* como saída.

---

## 📋 Tabela de Conteúdos
<!--ts-->
   * [A Linguagem TONTO](#-a-linguagem-tonto)
   * [Sobre o Projeto](#-sobre-o-projeto)
   * [Tecnologias Utilizadas](#-tecnologias-utilizadas)
   * [Estrutura de Pastas](#-estrutura-de-pastas)
   * [Funcionalidades](#-funcionalidades)
   * [Especificação dos Tokens](#-especificação-dos-tokens)
   * [Como Usar](#-como-usar)
   * [Exemplos](#-exemplos)
   * [Autores](#%E2%80%8D-autores)
   * [Licença](#-licença)
<!--te-->

---

## 🧩 A Linguagem TONTO

A **TONTO** (*Textual Ontology Language*) é uma linguagem textual para modelagem de ontologias, desenvolvida por **Matheus Lenke Coutinho**. Criada com o objetivo de superar limitações das linguagens de modelagem puramente visuais, ela permite a **edição**, **validação** e **versionamento** de ontologias por meio de **código textual** e também a **conversão** para outros para outros formatos como:

- *OntoUML*
- *gUFO (OWL)*
- *JSON*

Também possui extensão para o *VSCode*, permitindo criar módulos `.tonto`, gerenciar dependências com o *Tonto Package Manager* e gerar modelos interoperáveis com o *Protégé* e o *Visual Paradigm*.

💡 Para mais informações sobre a lingaugem, consulte a [documentação oficial](https://matheuslenke.github.io/tonto-docs/docs/intro), a [monografia completa](https://matheuslenke.github.io/tonto-docs/pdf/Tonto.pdf) e o [repositório oficial no GitHub](https://github.com/matheuslenke/Tonto).

---

## 📖 Sobre o Projeto

O **Analisador Léxico para a Linguagem TONTO** foi desenvolvido como parte de um estudo prático sobre a construção de compiladores e ferramentas de análise léxica. O projeto tem como objetivo o reconhecimento e categorização dos seguintes elementos da linguagem:

- **Palavras reservadas**;
- **Estereótipos de classe**;
- **Estereótipos de relações**;
- **Nomes de classes**;
- **Nomes de relações**;
- **Nomes de instâncias**;
- **Tipos de dados nativos**;
- **Novos tipos de dados**; 
- **Meta-atributos**;
- **Símbolos especiais**.

Além desses elementos previamente especificados na descrição do trabalho, o analisador léxico reconhece:

- **Atributos**;
- **Cardinalidades**.

O resultado consiste em **relatórios detalhados** sobre os *tokens* encontrados, permitindo uma base sólida para análise sintática ou semântica posterior.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**;
- **PLY** (Python Lex-Yacc)
- **TONTO** (Extensão do *VS Code*, *Tonto CLI* e *Tonto Package Manager*).

---

## 📂 Estrutura de Pastas

```shell
lexical_analyzer/
├── docs/                      
│   └── tonto_tokens_details.md   # Documentação dos tokens reconhecidos
├── src/                        
│   ├── examples/                 # Arquivos TONTO de entrada para testes
│   ├── lexer.py                  # Implementação do analisador léxico e funções de processamento/relatório
│   └── main.py                   # Ponto de entrada para executar o lexer nos arquivos de exemplo
├── .gitignore                    # Arquivo para ignorar pastas e arquivos gerados (padrão Git)
├── LICENSE                       # Informações sobre a licença de uso do código.
└── README.md                     # Documentação principal do projeto.

```

---

## ✨ Funcionalidades

- **Reconhecimento de Tokens:** reconhece e categoriza os *tokens* válidos da linguagem **TONTO** (citados na seção [Sobre o Projeto](#-sobre-o-projeto));

- **Geração de Tabela de Símbolos:** organiza e exibe todos os *tokens* identificados;

- **Contador de *Tokens*:** gera uma tabela de síntese com contagens de categorias léxicas;

- **Registro de Erros Léxicos:** detecta e lista *tokens* inválidos encontrados durante o processamento;

- **Menu Interativo:** permite a navegação e visualização de resultados.

---

## 🔤 Especificação dos *Tokens*

A **especificação detalhada** dos *tokens* da linguagem **TONTO** reconhecidos e categorizados pelo analisador léxico pode ser encontrada nesse [documento](docs/tonto_tokens_details.md).

---

## 🚀 Como Usar

### Pré-requisitos 

- [Python 3.10+](https://www.python.org/downloads/)
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)

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

## 💻 Exemplos

### Entrada

```
package CarOwnership 

kind Organization
subkind CarAgency specializes Organization
kind Car

relator CarOwnership {
    @mediation
    -- involvesOwner -- [1] CarAgency

    @mediation
    -- involvesProperty -- [1] Car
}
```
### Saída Esperada

- **Tokens Processados** (*Opção 1* do menu):

  <details>
  <summary>Clique para expandir</summary>

  | **Token**           | **Valor**        | **Linha** | **Posição** |
  | ------------------- | ---------------- | --------- | ----------- |
  | KEYWORD             | package          | 1         | 0           |
  | CLASS_NAME          | CarOwnership     | 1         | 8           |
  | CLASS_STEREOTYPE    | kind             | 3         | 23          |
  | CLASS_NAME          | Organization     | 3         | 28          |
  | CLASS_STEREOTYPE    | subkind          | 4         | 41          |
  | CLASS_NAME          | CarAgency        | 4         | 49          |
  | KEYWORD             | specializes      | 4         | 59          |
  | CLASS_NAME          | Organization     | 4         | 71          |
  | CLASS_STEREOTYPE    | kind             | 5         | 84          |
  | CLASS_NAME          | Car              | 5         | 89          |
  | CLASS_STEREOTYPE    | relator          | 7         | 94          |
  | CLASS_NAME          | CarOwnership     | 7         | 102         |
  | SPECIAL_SYMBOL      | {                | 7         | 115         |
  | SPECIAL_SYMBOL      | @                | 8         | 121         |
  | RELATION_STEREOTYPE | mediation        | 8         | 122         |
  | SPECIAL_SYMBOL      | --               | 9         | 136         |
  | RELATION_NAME       | involvesOwner    | 9         | 139         |
  | SPECIAL_SYMBOL      | --               | 9         | 153         |
  | CARDINALITY         | [1]              | 9         | 156         |
  | CLASS_NAME          | CarAgency        | 9         | 160         |
  | SPECIAL_SYMBOL      | @                | 11        | 175         |
  | RELATION_STEREOTYPE | mediation        | 11        | 176         |
  | SPECIAL_SYMBOL      | --               | 12        | 190         |
  | RELATION_NAME       | involvesProperty | 12        | 193         |
  | SPECIAL_SYMBOL      | --               | 12        | 210         |
  | CARDINALITY         | [1]              | 12        | 213         |
  | CLASS_NAME          | Car              | 12        | 217         |
  | SPECIAL_SYMBOL      | }                | 13        | 221         |

  </details>

- **Tabela de Símbolos** (*Opção 2* do menu):

  <details>
  <summary>Clique para expandir</summary>

  | **Token**            | **Valor**        |
  | -------------------  | ---------------- |
  | KEYWORD              | package          |
  | CLASS_NAME           | CarOwnership     |
  | CLASS_STEREOTYPE     | kind             |
  | CLASS_NAME           | Organization     |
  | CLASS_STEREOTYPE     | subkind          |
  | CLASS_NAME           | CarAgency        |
  | KEYWORD              | specializes      |
  | CLASS_NAME           | Car              |
  | CLASS_STEREOTYPE     | relator          |
  | SPECIAL_SYMBOL       | {                |
  | SPECIAL_SYMBOL       | @                |
  | RELATION_STEREOTYPE  | mediation        |
  | SPECIAL_SYMBOL       | --               |
  | RELATION_NAME        | involvesOwner    |
  | CARDINALITY          | [1]              |
  | RELATION_NAME        | involvesProperty |
  | SPECIAL_SYMBOL       | }                |

  </details> 

- **Contagem de Tokens** (*Opção 3* do menu):

  <details>
  <summary>Clique para expandir</summary>

  | **Token**           | **Quantidade** |
  | ------------------- | -------------- |
  | CLASS_STEREOTYPE    | 4              |
  | RELATION_STEREOTYPE | 2              |
  | KEYWORD             | 2              |
  | SPECIAL_SYMBOL      | 8              |
  | CLASS_NAME          | 8              |
  | RELATION_NAME       | 2              |
  | INSTANCE_NAME       | 0              |
  | NATIVE_DATATYPE     | 0              |
  | NEW_DATATYPE        | 0              |
  | META_ATTRIBUTE      | 0              |
  | ATTRIBUTE           | 0              |
  | CARDINALITY         | 2              |

  </details>

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
