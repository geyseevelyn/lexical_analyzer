import ply.lex as lex

# Lista de tokens
tokens = [
    'CLASS_STEREOTYPE', 'RELATION_STEREOTYPE', 'KEYWORD', 'SPECIAL_SYMBOL', 'CLASS_NAME', 
    'RELATION_NAME','INSTANCE_NAME', 'NATIVE_DATATYPE', 'NEW_DATATYPE','META_ATTRIBUTE',
    'ENUM_NAME', 'ATTRIBUTE', 'CARDINALITY'
]

# Palavras reservadas
keywords = { 
    'specializes', 'genset', 'disjoint', 'complete', 'general', 'specifics', 'where', 
    'package', 'import', 'functional-complexes', 'relators', 'intrinsic-modes', 'extrinsic-modes', 
    'datatype', 'enum', 'type', 'instanceOf', 'categorizer', 'of', 'relation', 'inverseOf'
}

# Estereótipos de classe
class_stereotypes = { 
    'event', 'situation', 'process', 'category', 'mixin','phaseMixin', 'roleMixin', 
    'historicalRoleMixin', 'kind', 'collective','quantity', 'quality', 'mode', 'intrisicMode', 
    'extrinsicMode', 'subkind','phase', 'role', 'historicalRole', 'relator', 'class'
}

# Estruturas de dados
symbol_table = []
token_count = {token: 0 for token in tokens}
processed_tokens = [] 
error_tokens = []
last_keyword = None  # Armazena a última palavra-chave processada

# ---------- Estruturas para Análise Sintática ----------
# Modelo sintático extraído do fluxo de tokens
syntax_model = {
    'packages': {},           # { package: { 'classes': { className: { 'stereotype': str, 'specializes': [], 'attributes': [], 'relations': [] } } } }
    'types': {
        'datatypes': set(),   # ex.: CPFDataType
        'enums': set(),       # ex.: EyeColorEnum
    },
    'external_relations': []  # relações declaradas fora de blocos de classe
}

# Relatório de erros de ontologia com sugestões
ontology_errors = []  # itens: { 'mensagem': str, 'linha': int, 'posicao': int, 'sugestao': str }

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

# Função para adicionar erros (captura o lexema inválido completo e retorna o tamanho consumido)
def add_to_error_list(token):
    data = token.lexer.lexdata
    start = token.lexer.lexpos
    i = start
    n = len(data)
    # Delimitadores conhecidos (não consumir para não perder tokens válidos seguintes)
    delimiters = set('{}()[]:@,.*-<>')
    while i < n and (not data[i].isspace()) and (data[i] not in delimiters):
        i += 1
    invalid_lexeme = data[start:i] if i > start else data[start:start+1]
    error_tokens.append({
        'Token': 'ERRO',
        'Valor': invalid_lexeme,
        'Linha': token.lineno,
        'Posição': token.lexpos
    })
    return max(1, i - start)

# Expressões regulares para os tokens

# Atributos de Classes e DataTypes
def t_ATTRIBUTE(t):
    r'\b[a-z][a-zA-Z]*:'
    t.value = t.value[:-1]  
    add_to_symbol_table(t)
    return t

# Novos tipos de dados
def t_NEW_DATATYPE(t):
    r'\b[A-Za-z]+DataType\b'
    add_to_symbol_table(t)
    return t

# Enumerações
def t_ENUM_NAME(t):
    r'\b[A-Za-z]+Enum\b'
    add_to_symbol_table(t)
    return t

# Cardinalidade [n], [n..m], [n..*], [*]
def t_CARDINALITY(t):
    r'\[\s*(\*|\d+)\s*(?:\.\.\s*(\*|\d+))?\s*\]'
    # remove espaços internos
    content = t.value[1:-1].strip()
    if '..' in content:
        a, b = [p.strip() for p in content.split('..', 1)]
        t.value = f'[{a}..{b}]'
    else:
        t.value = f'[{content}]'
    add_to_symbol_table(t)
    return t

# Símbolos especiais restantes
# Observação: o caractere ":" também é usado em atributos, mas lá é consumido por t_ATTRIBUTE.
# Aqui tratamos apenas ocorrências de ':' que não façam parte de um atributo.
def t_SPECIAL_SYMBOL(t):
    r'(\{|\}|\(|\)|<>--|--<>|--|--<o>|<o>--|@|:|,|\.)'
    add_to_symbol_table(t)
    return t

# Palavras reservadas
def t_KEYWORD(t):
    r'\b(specializes|genset|disjoint|complete|general|specifics|where|package|import|functional-complexes|relators|intrinsic-modes|extrinsic-modes|datatype|enum|type|instanceOf|categorizer|of|relation|inverseOf)\b'
    global last_keyword
    if t.value in keywords:
        t.type = 'KEYWORD'
        last_keyword = t.value  # Armazena a palavra-chave processada
    add_to_symbol_table(t)
    return t

# Tipos de dados nativos: number, string, boolean, date, time, datetime
def t_NATIVE_DATATYPE(t):
    r'\b(number|string|boolean|date|time|datetime)\b'
    add_to_symbol_table(t)
    return t

# Meta-atributos: ordered, const, derived, subsets, redefines
def t_META_ATTRIBUTE(t):
    r'\b(ordered|const|derived|subsets|redefines)\b'
    add_to_symbol_table(t)
    return t

# Estereótipos de Classe
def t_CLASS_STEREOTYPE(t):
    r'\b(event|situation|process|category|mixin|phaseMixin|roleMixin|historicalRoleMixin|kind|collective|quantity|quality|mode|intrisicMode|extrinsicMode|subkind|phase|role|historicalRole|relator|class)\b'
    if t.value in class_stereotypes:
        t.type = 'CLASS_STEREOTYPE'
    add_to_symbol_table(t)
    return t

# Estereótipos de relações
def t_RELATION_STEREOTYPE(t):
    r'\b(material|derivation|comparative|mediation|characterization|externalDependence|subCollectionOf|subQualityOf|componentOf|instantiation|memberOf|termination|participational|participation|historicalDependence|creation|manifestation|bringsAbout|triggers|composition|aggregation|inherence|value|formal|constitution)\b'
    add_to_symbol_table(t)
    return t

# Nomes de Instâncias
def t_INSTANCE_NAME(t):
    r'\b[A-Za-z][A-Za-z_]*\d+\b'
    add_to_symbol_table(t)
    return t

# Convenção para nomes de relações
def t_RELATION_NAME(t):
    r'\b[a-z][a-zA-Z]*(?:_[a-zA-Z]+)*\b'
    add_to_symbol_table(t)
    return t

# Convenção para nomes de Classes (também usado para Packages e GenSets)
def t_CLASS_NAME(t):
    r'\b[A-Z][a-zA-Z]*(?:_[a-zA-Z][a-zA-Z]*)*\b'
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
    consumed = add_to_error_list(t)
    t.lexer.skip(consumed)

# Construção do Lexer
lexer = lex.lex()

# Função para processar o arquivo
def process_file(file_path):
    global symbol_table, token_count, processed_tokens, error_tokens, last_keyword, syntax_model, ontology_errors
    # Limpa completamente o contexto anterior
    symbol_table = []
    token_count = {token: 0 for token in tokens}
    processed_tokens = []
    error_tokens = []
    last_keyword = None  # Reseta a última palavra-chave
    syntax_model = {
        'packages': {},
        'types': {
            'datatypes': set(),
            'enums': set(),
        },
        'external_relations': []
    }
    ontology_errors = []

    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Reinicia contagem de linhas do lexer
            lexer.lineno = 1
            lexer.input(data)

            # Processa os tokens
            while lexer.token():
                pass  # Apenas preenche os dados na tabela e contador
        # Após o processamento léxico, executa uma análise sintática simplificada
        analyze_syntax()
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return False
    return True

# Função para exibir os tokens processados
def show_tokens():
    print("\n====================== Tokens Processados =======================\n")
    header = f"{'Token':<20} {'Valor':<28} {'Linha':<6} {'Posição':<5}"
    print(header)
    print("-" * len(header))

    for token in processed_tokens:
        print(f"{token.type:<20} {str(token.value):<30} {token.lineno:<6} {token.lexpos:<6}")

    if error_tokens:
        header = f"{'Token':<20} {'Valor':<28} {'Linha':<6} {'Posição':<5}"

        print("\n=========================== Erros ===============================\n")
        print(header)
        print("-" * len(header))
        for error in error_tokens:
            print(f"{error['Token']:<20} {error['Valor']:<30} {error['Linha']:<6} {error['Posição']:<5}")

# Função para exibir a tabela de símbolos
def show_symbol_table():
    print("\n================= Tabela de Símbolos =================\n")
    print(f"{'Token':<20} {'Valor':<30}")
    print("-" * 55)
    for entry in symbol_table:
        print(f"{entry['Token']:<20} {entry['Valor']:<30}")

# Função para exibir a contagem de tokens
def show_token_count():
    print("\n======= Contagem de Tokens =======\n")
    print(f"{'Token':<20} {'Quantidade':<10}")
    print("-" * 35)
    for token, count in token_count.items():
        print(f"{token:<25} {count:<10}")

# ===================== Análise Sintática (Simplificada) =====================

def _ensure_package(pkg_name):
    if pkg_name not in syntax_model['packages']:
        syntax_model['packages'][pkg_name] = {'classes': {}}

def _register_class(pkg, stereotype, class_name, line, pos):
    _ensure_package(pkg)
    classes = syntax_model['packages'][pkg]['classes']
    if class_name in classes:
        ontology_errors.append({
            'mensagem': f"Classe duplicada '{class_name}' no pacote '{pkg}'.",
            'linha': line,
            'posicao': pos,
            'sugestao': 'Renomeie a classe ou remova a duplicata.'
        })
    else:
        classes[class_name] = {
            'stereotype': stereotype,
            'specializes': [],
            'attributes': [],
            'relations': []
        }

def _add_attribute(pkg, cls, name, atype, line, pos):
    try:
        syntax_model['packages'][pkg]['classes'][cls]['attributes'].append({'name': name, 'type': atype})
    except KeyError:
        ontology_errors.append({
            'mensagem': f"Atributo '{name}' fora de um contexto de classe.",
            'linha': line,
            'posicao': pos,
            'sugestao': 'Declare atributos dentro de um bloco de classe.'
        })

def _add_relation(pkg, cls, data):
    try:
        syntax_model['packages'][pkg]['classes'][cls]['relations'].append(data)
    except KeyError:
        ontology_errors.append({
            'mensagem': f"Relação '{data.get('name','?')}' fora de um contexto de classe.",
            'linha': data.get('line', 0),
            'posicao': data.get('pos', 0),
            'sugestao': 'Declare relações dentro de blocos de classe ou use o construto relation no nível superior.'
        })

def analyze_syntax():
    """
    Varre processed_tokens e constrói um modelo sintático mínimo da ontologia,
    além de coletar inconsistências comuns com sugestões de correção.
    """
    global syntax_model, ontology_errors

    if not processed_tokens:
        return

    # Estado
    current_package = None
    current_class = None
    current_class_pkg = None
    class_block_open = False  # true quando o último '{' abriu um bloco de classe
    brace_stack = []          # rastrear outros blocos
    last_rel_stereo = None

    connectors = {'--', '<>--', '--<>', '--<o>', '<o>--'}

    def class_exists(name):
        for p in syntax_model['packages'].values():
            if name in p['classes']:
                return True
        return False

    i = 0
    n = len(processed_tokens)
    while i < n:
        t = processed_tokens[i]

        # 1) Pacotes
        if t.type == 'KEYWORD' and t.value == 'package':
            if i + 1 < n and processed_tokens[i+1].type in ('CLASS_NAME',):
                pkg_name = processed_tokens[i+1].value
                current_package = pkg_name
                _ensure_package(pkg_name)
                i += 2
                continue
            else:
                ontology_errors.append({
                    'mensagem': "Declaração de pacote sem nome.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Use: package NomeDoPacote'
                })
                i += 1
                continue

        # 2) Declarações de tipos
        if t.type == 'KEYWORD' and t.value == 'datatype':
            if i + 1 < n and processed_tokens[i+1].type in ('NEW_DATATYPE', 'CLASS_NAME'):
                syntax_model['types']['datatypes'].add(processed_tokens[i+1].value)
                i += 2
                continue
            else:
                ontology_errors.append({
                    'mensagem': "Declaração de datatype sem nome.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Ex.: datatype CPFDataType'
                })
                i += 1
                continue

        if t.type == 'KEYWORD' and t.value == 'enum':
            if i + 1 < n and processed_tokens[i+1].type in ('ENUM_NAME', 'CLASS_NAME'):
                syntax_model['types']['enums'].add(processed_tokens[i+1].value)
                i += 2
                continue
            else:
                ontology_errors.append({
                    'mensagem': "Declaração de enum sem nome.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Ex.: enum EyeColorEnum { ... }'
                })
                i += 1
                continue

        # 3) Classes
        if t.type == 'CLASS_STEREOTYPE':
            if i + 1 < n and processed_tokens[i+1].type == 'CLASS_NAME':
                stereotype = t.value
                cls_name = processed_tokens[i+1].value
                pkg = current_package or 'global'
                _register_class(pkg, stereotype, cls_name, t.lineno, t.lexpos)
                current_class = cls_name
                current_class_pkg = pkg
                # especializações
                i += 2
                if i < n and processed_tokens[i].type == 'KEYWORD' and processed_tokens[i].value == 'specializes':
                    if i + 1 < n and processed_tokens[i+1].type == 'CLASS_NAME':
                        try:
                            syntax_model['packages'][pkg]['classes'][cls_name]['specializes'].append(processed_tokens[i+1].value)
                        except KeyError:
                            pass
                        i += 2
                    else:
                        ontology_errors.append({
                            'mensagem': f"'specializes' sem classe alvo após '{cls_name}'.",
                            'linha': processed_tokens[i].lineno,
                            'posicao': processed_tokens[i].lexpos,
                            'sugestao': 'Informe o nome da classe geral após specializes.'
                        })
                        i += 1
                # bloco opcional
                if i < n and processed_tokens[i].type == 'SPECIAL_SYMBOL' and processed_tokens[i].value == '{':
                    class_block_open = True
                    brace_stack.append('class')
                    i += 1
                continue
            else:
                ontology_errors.append({
                    'mensagem': "Estereótipo de classe sem nome da classe.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Use: kind/min/etc. NomeDaClasse'
                })
                i += 1
                continue

        # 4) Fechamento/abertura de blocos
        if t.type == 'SPECIAL_SYMBOL' and t.value == '{':
            brace_stack.append('block')
            i += 1
            continue
        if t.type == 'SPECIAL_SYMBOL' and t.value == '}':
            if brace_stack:
                top = brace_stack.pop()
                if top == 'class':
                    class_block_open = False
                    current_class = None
                    current_class_pkg = None
                    last_rel_stereo = None
            else:
                ontology_errors.append({
                    'mensagem': "Chave de fechamento '}' sem abertura correspondente.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Verifique os blocos e pareamentos de chaves.'
                })
            i += 1
            continue

        inside_class = class_block_open and current_class is not None

        # 5) Conteúdo de classe
        if inside_class:
            if t.type == 'ATTRIBUTE':
                # tipo opcional logo após
                atype = None
                if i + 1 < n and processed_tokens[i+1].type in ('NATIVE_DATATYPE', 'NEW_DATATYPE', 'CLASS_NAME', 'ENUM_NAME'):
                    atype = processed_tokens[i+1].value
                    i += 2
                else:
                    i += 1
                _add_attribute(current_class_pkg, current_class, t.value, atype, t.lineno, t.lexpos)
                continue

            if t.type == 'SPECIAL_SYMBOL' and t.value == '@':
                if i + 1 < n and processed_tokens[i+1].type == 'RELATION_STEREOTYPE':
                    last_rel_stereo = processed_tokens[i+1].value
                    i += 2
                    continue
                else:
                    ontology_errors.append({
                        'mensagem': "Meta-indicador '@' sem estereótipo de relação subsequente.",
                        'linha': t.lineno,
                        'posicao': t.lexpos,
                        'sugestao': 'Use: @mediation, @characterization, etc.'
                    })
                    i += 1
                    continue

            if t.type == 'SPECIAL_SYMBOL' and t.value in connectors:
                # padrão: connector RELATION_NAME connector? CARDINALITY? CLASS_NAME
                j = i
                connector1 = processed_tokens[j].value
                j += 1
                if j >= n or processed_tokens[j].type != 'RELATION_NAME':
                    ontology_errors.append({
                        'mensagem': f"Conector de relação '{connector1}' sem nome de relação.",
                        'linha': t.lineno,
                        'posicao': t.lexpos,
                        'sugestao': 'Informe o nome da relação após o conector.'
                    })
                    i += 1
                    continue
                rname = processed_tokens[j].value
                rline = processed_tokens[j].lineno
                rpos = processed_tokens[j].lexpos
                j += 1
                connector2 = None
                if j < n and processed_tokens[j].type == 'SPECIAL_SYMBOL' and processed_tokens[j].value in connectors:
                    connector2 = processed_tokens[j].value
                    j += 1
                card = None
                if j < n and processed_tokens[j].type == 'CARDINALITY':
                    card = processed_tokens[j].value
                    j += 1
                if j < n and processed_tokens[j].type == 'CLASS_NAME':
                    target = processed_tokens[j].value
                    _add_relation(current_class_pkg, current_class, {
                        'name': rname,
                        'stereotype': last_rel_stereo,
                        'connector': f"{connector1}{' ' + connector2 if connector2 else ''}",
                        'cardinality': card,
                        'target': target,
                        'line': rline,
                        'pos': rpos
                    })
                    j += 1
                    i = j
                    continue
                else:
                    ontology_errors.append({
                        'mensagem': f"Relação '{rname}' sem classe alvo.",
                        'linha': rline,
                        'posicao': rpos,
                        'sugestao': 'Informe o nome da classe alvo após a cardinalidade (se houver).'
                    })
                    i = j
                    continue

        # 6) Relações externas via palavra-chave 'relation'
        if t.type == 'KEYWORD' and t.value == 'relation':
            j = i + 1
            if j >= n or processed_tokens[j].type != 'RELATION_NAME':
                ontology_errors.append({
                    'mensagem': "'relation' sem nome da relação.",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Use: relation nomeRelacao ...'
                })
                i += 1
                continue
            rel_name = processed_tokens[j].value
            rel_line = processed_tokens[j].lineno
            rel_pos = processed_tokens[j].lexpos
            j += 1
            rel_st = None
            rel_card = None
            rel_from = None
            rel_to = None
            # varre alguns tokens à frente para tentar capturar classes
            scan = 0
            while j < n and scan < 12 and (processed_tokens[j].type not in ('CLASS_STEREOTYPE', 'KEYWORD') or processed_tokens[j].value == 'inverseOf'):
                tt = processed_tokens[j]
                if tt.type == 'RELATION_STEREOTYPE' and not rel_st:
                    rel_st = tt.value
                elif tt.type == 'CARDINALITY' and not rel_card:
                    rel_card = tt.value
                elif tt.type == 'CLASS_NAME':
                    if rel_from is None:
                        rel_from = tt.value
                    elif rel_to is None:
                        rel_to = tt.value
                    else:
                        break
                j += 1
                scan += 1
            if rel_from and rel_to:
                syntax_model['external_relations'].append({
                    'name': rel_name,
                    'stereotype': rel_st,
                    'from': rel_from,
                    'to': rel_to,
                    'cardinality': rel_card,
                    'line': rel_line,
                    'pos': rel_pos
                })
                i = j
                continue
            else:
                ontology_errors.append({
                    'mensagem': f"Declaração de relação '{rel_name}' incompleta.",
                    'linha': rel_line,
                    'posicao': rel_pos,
                    'sugestao': 'Informe pelo menos as classes de origem e destino.'
                })
                i = j
                continue

        # 7) Atributos fora de classe
        if t.type == 'ATTRIBUTE' and not inside_class:
            ontology_errors.append({
                'mensagem': f"Atributo '{t.value}' declarado fora de classe.",
                'linha': t.lineno,
                'posicao': t.lexpos,
                'sugestao': 'Mova o atributo para dentro de um bloco de classe.'
            })
            i += 1
            continue

        i += 1

    # Finais: chaves não fechadas
    if brace_stack:
        ontology_errors.append({
            'mensagem': 'Há blocos não fechados (chaves abertas).',
            'linha': 0,
            'posicao': 0,
            'sugestao': 'Feche todos os blocos com }.'
        })

    # Verificação de referências a classes não definidas
    defined_classes = set()
    for pkg_data in syntax_model['packages'].values():
        defined_classes.update(pkg_data['classes'].keys())
    # relações de classes
    for pkg, pdata in syntax_model['packages'].items():
        for cname, cdata in pdata['classes'].items():
            for r in cdata['relations']:
                tgt = r.get('target')
                if tgt and tgt not in defined_classes:
                    ontology_errors.append({
                        'mensagem': f"Relação '{r.get('name')}' referencia classe não definida '{tgt}'.",
                        'linha': r.get('line', 0),
                        'posicao': r.get('pos', 0),
                        'sugestao': 'Declare a classe alvo ou corrija o nome referenciado.'
                    })
    # relações externas
    for r in syntax_model['external_relations']:
        for endp in ('from', 'to'):
            val = r.get(endp)
            if val and val not in defined_classes:
                ontology_errors.append({
                    'mensagem': f"Relação externa '{r.get('name')}' referencia classe não definida '{val}'.",
                    'linha': r.get('line', 0),
                    'posicao': r.get('pos', 0),
                    'sugestao': 'Declare a classe envolvida ou corrija o nome.'
                })


def show_syntax_summary():
    print("\n================= Síntese da Análise Sintática =================\n")
    # Pacotes
    pkgs = list(syntax_model['packages'].keys())
    print(f"Pacotes ({len(pkgs)}): {', '.join(pkgs) if pkgs else 'nenhum'}\n")

    # Classes por pacote
    for pkg, pdata in syntax_model['packages'].items():
        print(f"Pacote: {pkg}")
        classes = pdata['classes']
        if not classes:
            print("  (sem classes)")
        for cname, cdata in classes.items():
            spec = (f" specializes {', '.join(cdata['specializes'])}" if cdata['specializes'] else '')
            print(f"  - {cdata['stereotype']} {cname}{spec}")
            # Atributos
            if cdata['attributes']:
                print("    atributos:")
                for a in cdata['attributes']:
                    tdesc = f": {a['type']}" if a.get('type') else ''
                    print(f"      - {a['name']}{tdesc}")
            # Relações
            if cdata['relations']:
                print("    relações:")
                for r in cdata['relations']:
                    st = f"@{r['stereotype']} " if r.get('stereotype') else ''
                    cd = f" {r['cardinality']}" if r.get('cardinality') else ''
                    conn = r.get('connector') or ''
                    print(f"      - {st}{r['name']} {conn} {r['target']}{cd}")
        print()

    # Tipos
    dts = sorted(list(syntax_model['types']['datatypes']))
    ens = sorted(list(syntax_model['types']['enums']))
    print(f"Tipos de dados declarados ({len(dts)}): {', '.join(dts) if dts else 'nenhum'}")
    print(f"Enums declarados ({len(ens)}): {', '.join(ens) if ens else 'nenhum'}\n")

    # Relações externas
    exts = syntax_model['external_relations']
    print(f"Relações externas ({len(exts)}):")
    if not exts:
        print("  (nenhuma)")
    for r in exts:
        st = f"@{r['stereotype']} " if r.get('stereotype') else ''
        cd = f" {r['cardinality']}" if r.get('cardinality') else ''
        print(f"  - {st}{r['name']}: {r.get('from','?')} -> {r.get('to','?')}{cd}")


def show_ontology_errors():
    print("\n==================== Relatório de Erros da Ontologia ====================\n")
    if not ontology_errors and not error_tokens:
        print("Nenhum erro encontrado.")
        return
    # Erros sintáticos/semânticos
    if ontology_errors:
        print("Erros e sugestões:")
        for e in ontology_errors:
            print(f"- Linha {e.get('linha',0)}, pos {e.get('posicao',0)}: {e['mensagem']}")
            if e.get('sugestao'):
                print(f"  Sugestão: {e['sugestao']}")
    # Erros léxicos já coletados
    if error_tokens:
        print("\nErros léxicos:")
        for err in error_tokens:
            print(f"- Linha {err['Linha']}, pos {err['Posição']}: lexema inválido '{err['Valor']}'")