import ply.lex as lex

# Lista de tokens
tokens = [
    'CLASS_STEREOTYPE', 'RELATION_STEREOTYPE', 'KEYWORDS', 'SPECIAL_SYMBOL', 'CLASS_NAME', 
    'RELATION_NAME','INSTANCE_NAME', 'NATIVE_DATATYPE', 'NEW_DATATYPE','META_ATTRIBUTE'
]

# Estereótipos de classe
class_stereotypes = { 
    'event', 'situation', 'process', 'category', 'mixin','phaseMixin', 'roleMixin', 
    'historicalRoleMixin', 'kind', 'collective','quantity', 'quality', 'mode', 'intrisicMode', 
    'extrinsicMode', 'subkind','phase', 'role', 'historicalRole', 'relator', 'class'
}

symbol_table = []
token_count = {token: 0 for token in tokens}
processed_tokens = [] 
error_tokens = []

# Adiciona o token à tabela de símbolos e atualiza o contador
def add_to_symbol_table(token):
    if any(entry['Valor'] == token.value for entry in symbol_table):
        token_count[token.type] += 1
        processed_tokens.append(token)
        return  # Não adiciona duplicatas
    symbol_table.append({
        'Token': token.type,
        'Valor': token.value
    })
    token_count[token.type] += 1
    processed_tokens.append(token)

# Função para adicionar erros
def add_to_error_list(token):
    error_tokens.append({
        'Token': 'ERRO',
        'Valor': token.value[0],
        'Linha': token.lineno,
        'Posição': token.lexpos
    })

# Expressões regulares para os tokens
def t_CLASS_STEREOTYPE(t):
    r'\b(event|situation|process|category|mixin|phaseMixin|roleMixin|historicalRoleMixin|kind|collective|quantity|quality|mode|intrisicMode|extrinsicMode|subkind|phase|role|historicalRole|relator|class)\b'
    if t.value in class_stereotypes:
        t.type = 'CLASS_STEREOTYPE'
    add_to_symbol_table(t)
    return t

# Atualizar contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    add_to_error_list(t)
    t.lexer.skip(1)

# Construção do lexer
lexer = lex.lex()

# Função para processar o arquivo
def process_file(file_path):
    global symbol_table, token_count, processed_tokens
    symbol_table = []  
    token_count = {token: 0 for token in tokens}  
    processed_tokens = []  

    try:
        with open(file_path, 'r') as file:
            data = file.read()
            lexer.input(data)

            # Processa os tokens
            while lexer.token():
                pass  # Apenas preenche os dados na tabela e contador
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return False
    return True

# Função para exibir os tokens processados
def show_tokens():
    print("\n====================== Tokens Processados ======================\n")
    header = f"{'Token':<25} {'Valor':<23} {'Linha':<6} {'Posição':<5}"
    print(header)
    print("-" * len(header))

    for token in processed_tokens:
        print(f"{token.type:<25} {str(token.value):<25} {token.lineno:<6} {token.lexpos:<5}")

    if error_tokens:
        print("\n=========================== Erros ===========================\n")
        for error in error_tokens:
            print(f"{error['Token']:<25} {error['Valor']:<25} {error['Linha']:<6} {error['Posição']:<5}")

# Função para exibir a tabela de símbolos
def show_symbol_table():
    print("\n================= Tabela de Símbolos =================\n")
    print(f"{'Token':<25} {'Valor':<30}")
    print("-" * 55)
    for entry in symbol_table:
        print(f"{entry['Token']:<25} {entry['Valor']:<30}")

# Função para exibir a contagem de tokens
def show_token_count():
    print("\n======= Contagem de Tokens =======\n")
    print(f"{'Token':<20} {'Quantidade':<10}")
    print("-" * 35)
    for token, count in token_count.items():
        print(f"{token:<25} {count:<10}")

# Menu interativo
def menu():
    while True:
        print("\n====== MENU DE OPÇÕES ======")
        print("1. Exibir Tokens Processados")
        print("2. Exibir Tabela de Símbolos")
        print("3. Exibir Contagem de Tokens")
        print("4. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            show_tokens()
        elif choice == '2':
            show_symbol_table()
        elif choice == '3':
            show_token_count()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Caminho do arquivo de entrada
file_path = input("Digite o caminho do arquivo: ")
if process_file(file_path):
    menu()
