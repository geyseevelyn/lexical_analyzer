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