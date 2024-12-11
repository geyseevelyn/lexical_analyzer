# Analisador Léxico

Este projeto implementa um **analisador léxico** para a linguagem [*OWL2*](https://www.w3.org/TR/owl2-overview/) no formato [*Manchester Syntax*](https://www.w3.org/TR/owl2-manchester-syntax/), utilizando Python e a biblioteca PLY. O objetivo é identificar e categorizar os *tokens* presentes em uma ontologia descrita neste formato, produzindo uma tabela de símbolos como saída.

---

## 📋 Tabela de Conteúdos
<!--ts-->
   * [Sobre o Projeto](#-sobre-o-projeto)
   * [Como Usar](#-como-usar)
   * [Funcionalidades](#-funcionalidades)
   * [Descrição do Tokens](#-descrição-dos-tokens)
   * [Exemplos](#-exemplos)
   * [Autores](#-autores)
   * [Licença](#-licença)
<!--te-->

---

## 📖 Sobre o Projeto

A linguagem **OWL2** é amplamente usada para criar ontologias e descrever relações semânticas na Web. O formato **Manchester Syntax** foi projetado para ser legível por humanos, permitindo descrever conceitos em lógica descritiva. Este **analisador léxico** é capaz de processar trechos de ontologias nesse formato e identificar elementos como palavras reservadas, identificadores de classe e propriedades, símbolos especiais, nomes de indivíduos, tipos de dados e cardinalidades.

---

## ⚙ Como Usar

### Pré-requisitos 

- [Python](https://www.python.org/downloads/)
- [Biblioteca PLY](https://www.dabeaz.com/ply/) (Python Lex-Yacc)

### Passo a Passo

1. Clone o repositório ou baixe o arquivo ZIP:

   ```bash
   git clone https://github.com/geyseevelyn/lexical_analyzer.git
   ```

2. Acesse a pasta do repositório:

   ```bash
   cd lexical_analyzer
   ```

3. Instale a biblioteca PLY:

   ```bash
   pip install ply
   ```

4. Mude para a pasta `src`:

   ```bash
   cd src
   ```

5. Execute o código:

   ```bash
   python lexical_analyzer.py
   ```

6. Insira o nome do arquivo de teste (deve estar na pasta `src`):

   ```bash
   input.txt
   ```

7. Escolha as opções do menu interativo para:

   - Visualizar tokens processados;
   - Exibir a tabela de símbolos;
   - Consultar a contagem de tokens.

---

## ✨ Funcionalidades

- Identificação de **palavras reservadas**, **classes**, **propriedades** e **indivíduos**, **tipos de dados**, **símbolos especiais** e **cardinalidades**.

- Geração de **tabela de símbolos**.

- Registro de **erros léxicos** encontrados no código.
 
- **Menu interativo** com exibição de dados processados.

---

## 🔤 Descrição dos Tokens

### 1. Palavras Reservadas
Tokens que representam palavras-chave da linguagem:

- `some`, `all`, `value`, `min`, `max`, `exactly`, `that`
- `not`, `and`, `or`, `only`
- `Class:`, `EquivalentTo:`, `Individuals:`, `SubClassOf:`, `DisjointClasses:`

### 2. Identificadores de Classes
Nomes que representam classes na ontologia:

- Começam com letra maiúscula, p.ex.: `Pizza`.
- Nomes compostos concatenados e com iniciais maiúsculas, p.ex.: `VegetarianPizza`.
- Nomes compostos separados por underline, p.ex.: `Margherita_Pizza`..

### 3. Identificadores de Propriedades
Nomes que representam propriedades das classes:

- Começam com "has", seguidos de uma string simples ou composta, p.ex.: `hasTopping`, `hasBase`.
- Começam com "is", seguidos de qualquer coisa, e terminam com `Of`, p.ex.: `isToppingOf`, `isBaseOf`.
- Outros nomes geralmente começam com letra minúscula, p.ex.: `ssn`, `numberOfPizzasPurchased`.

### 4. Nomes de Indivíduos
Identificam instâncias específicas de classes:

- Começam com uma letra maiúscula, seguida de qualquer combinação de letras minúsculas e terminando com um número. Exemplo: `Customer1`, `Pizza1`, `Waiter2`.

### 5. Tipos de Dados
Representam tipos suportados pela linguagem OWL, RDF, RDFs ou XML Schema:

- Exemplo: `xsd:integer`, `xsd:string`, `owl:real`.

### 6. Símbolos Especiais
Incluem caracteres utilizados para estruturar expressões:

- `[`, `]`, `{`, `}`, `(`, `)`, `<`, `>`, `=`,`,`.

### 7. Cardinalidades
Especificam restrições numéricas para relações ou propriedades:

- Exemplo: min `3`, exactly `2`.

---

## 💻 Exemplos

### Entrada

```
Class: VegetarianPizza
EquivalentTo:
    Pizza
    and (hasTopping only
    (CheeseTopping or VegetableTopping))
```

### Saída Esperada

- Tokens Processados

|**Token**            | **Valor**               | **Linha** | **Posição** |
|-----------------------|-------------------------|-----------|-------------|
| KEYWORD              | Class:                 | 1         | 0           |
| CLASS_ID             | VegetarianPizza        | 1         | 7           |
| KEYWORD              | EquivalentTo:          | 2         | 23          |
| CLASS_ID             | Pizza                  | 3         | 41          |
| KEYWORD              | and                    | 4         | 51          |
| SPECIAL_SYMBOL       | (                      | 4         | 55          |
| PROPERTY_ID          | hasTopping             | 4         | 56          |
| KEYWORD              | only                   | 4         | 67          |
| SPECIAL_SYMBOL       | (                      | 5         | 76          |
| CLASS_ID             | CheeseTopping          | 5         | 77          |
| KEYWORD              | or                     | 5         | 91          |
| CLASS_ID             | VegetableTopping       | 5         | 94          |
| SPECIAL_SYMBOL       | )                      | 5         | 110         |
| SPECIAL_SYMBOL       | )                      | 5         | 111         |

<br>

- Tabela de Símbolos

| **Token**            | **Valor**              |
|-----------------------|------------------------|
| KEYWORD              | Class:                |
| CLASS_ID             | VegetarianPizza       |
| KEYWORD              | EquivalentTo:         |
| CLASS_ID             | Pizza                 |
| KEYWORD              | and                   |
| SPECIAL_SYMBOL       | (                     |
| PROPERTY_ID          | hasTopping            |
| KEYWORD              | only                  |
| CLASS_ID             | CheeseTopping         |
| KEYWORD              | or                    |
| CLASS_ID             | VegetableTopping      |
| SPECIAL_SYMBOL       | )                     |

<br>

- Contagem de Tokens

| **Token**            | **Quantidade**        |
|-----------------------|-----------------------|
| KEYWORD              | 5                     |
| CLASS_ID             | 4                     |
| PROPERTY_ID          | 1                     |
| SPECIAL_SYMBOL       | 4                     |

---

## 👨‍💻 Autores

- [Geyse Evelyn](https://github.com/geyseevelyn)
- [Fabrício D'angellis](https://github.com/FabricioDangellis)

---

## 📜 Licença
Este projeto está sob a licença [MIT](./LICENSE).

---

<div align="center">
    <a href="https://github.com/geyseevelyn/lexical_analyzer?tab=readme-ov-file#analisador-l%C3%A9xico">Voltar ao topo</a>
</div>
 
