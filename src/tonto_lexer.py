import ply.lex as lex

# Lista de tokens (constante)
tokens = [
    # Terminais Regex
    'ID', 'INT', 'STRING',

    # Keywords (mapeadas a partir do ID)
    'GLOBAL', 'PACKAGE', 'IMPORT', 'AS', 'CLASS', 'EVENT', 'SITUATION',
    'CATEGORY', 'MIXIN', 'PHASEMIXIN', 'ROLEMIXIN', 'HISTORICALROLEMIXIN',
    'KIND', 'COLLECTIVE', 'QUANTITY', 'QUALITY', 'MODE', 'INTRINSICMODE',
    'EXTRINSICMODE', 'RELATOR', 'TYPE', 'POWERTYPE', 'SUBKIND', 'PHASE',
    'ROLE', 'HISTORICALROLE', 'INSTANCEOF', 'SPECIALIZES', 'OF', 'OBJECTS',
    'COLLECTIVES', 'QUANTITIES', 'RELATORS', 'QUALITIES', 'EVENTS', 'SITUATIONS',
    'TYPES', 'MATERIAL', 'DERIVATION', 'COMPARATIVE', 'MEDIATION',
    'CHARACTERIZATION', 'EXTERNALDEPENDENCE', 'COMPONENTOF', 'MEMBEROF',
    'SUBCOLLECTIONOF', 'SUBQUANTITYOF', 'INSTANTIATION', 'TERMINATION',
    'PARTICIPATIONAL', 'PARTICIPATION', 'HISTORICALDEPENDENCE', 'CREATION',
    'MANIFESTATION', 'BRINGABOUT', 'TRIGGERS', 'COMPOSITION', 'AGGREGATION_KW',
    'INHERENCE', 'VALUE', 'FORMAL', 'INVERSEOF', 'RELATION', 'ORDERED',
    'CONST', 'DERIVED', 'SUBSETS', 'REDEFINES', 'DISJOINT', 'COMPLETE',
    'GENSET', 'GENERAL', 'CATEGORIZER', 'SPECIFICS', 'WHERE', 'DATATYPE', 'ENUM',

    # Keywords Especiais (multi-palavra ou hífen)
    'FUNCTIONAL_COMPLEXES', 'INTRINSIC_MODES', 'EXTRINSIC_MODES', 'ABSTRACT_INDIVIDUALS',

    # Símbolos
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'COMMA', 'DOT', 'COLON', 'AT', 'STAR',

    # Símbolos multi-caractere
    'ARROW', 'AGGREGATION_OP', 'DOTDOT'
]

# Palavras reservadas (constante)
keywords = {
    'global': 'GLOBAL', 'package': 'PACKAGE', 'import': 'IMPORT', 'as': 'AS',
    'class': 'CLASS', 'event': 'EVENT', 'situation': 'SITUATION', 'category': 'CATEGORY',
    'mixin': 'MIXIN', 'phaseMixin': 'PHASEMIXIN', 'roleMixin': 'ROLEMIXIN',
    'historicalRoleMixin': 'HISTORICALROLEMIXIN', 'kind': 'KIND', 'collective': 'COLLECTIVE',
    'quantity': 'QUANTITY', 'quality': 'QUALITY', 'mode': 'MODE',
    'intrinsicMode': 'INTRINSICMODE', 'extrinsicMode': 'EXTRINSICMODE', 'relator': 'RELATOR',
    'type': 'TYPE', 'powertype': 'POWERTYPE', 'subkind': 'SUBKIND', 'phase': 'PHASE',
    'role': 'ROLE', 'historicalRole': 'HISTORICALROLE', 'instanceOf': 'INSTANCEOF',
    'specializes': 'SPECIALIZES', 'of': 'OF', 'objects': 'OBJECTS',
    'collectives': 'COLLECTIVES', 'quantities': 'QUANTITIES', 'relators': 'RELATORS',
    'qualities': 'QUALITIES', 'events': 'EVENTS', 'situations': 'SITUATIONS',
    'types': 'TYPES', 'material': 'MATERIAL', 'derivation': 'DERIVATION',
    'comparative': 'COMPARATIVE', 'mediation': 'MEDIATION', 'characterization': 'CHARACTERIZATION',
    'externalDependence': 'EXTERNALDEPENDENCE', 'componentOf': 'COMPONENTOF',
    'memberOf': 'MEMBEROF', 'subCollectionOf': 'SUBCOLLECTIONOF',
    'subQuantityOf': 'SUBQUANTITYOF', 'instantiation': 'INSTANTIATION',
    'termination': 'TERMINATION', 'participational': 'PARTICIPATIONAL',
    'participation': 'PARTICIPATION', 'historicalDependence': 'HISTORICALDEPENDENCE',
    'creation': 'CREATION', 'manifestation': 'MANIFESTATION', 'bringsAbout': 'BRINGABOUT',
    'triggers': 'TRIGGERS', 'composition': 'COMPOSITION', 'aggregation': 'AGGREGATION_KW',
    'inherence': 'INHERENCE', 'value': 'VALUE', 'formal': 'FORMAL',
    'inverseOf': 'INVERSEOF', 'relation': 'RELATION', 'ordered': 'ORDERED',
    'const': 'CONST', 'derived': 'DERIVED', 'subsets': 'SUBSETS',
    'redefines': 'REDEFINES', 'disjoint': 'DISJOINT', 'complete': 'COMPLETE',
    'genset': 'GENSET', 'general': 'GENERAL', 'categorizer': 'CATEGORIZER',
    'specifics': 'SPECIFICS', 'where': 'WHERE', 'datatype': 'DATATYPE', 'enum': 'ENUM'
}


class TontoLexer:
    """
    Classe que encapsula o analisador léxico para a gramática Tonto.
    Gerencia seu próprio estado (tabelas, contadores) e segue os padrões do PLY.
    """

    def __init__(self):
        # Listas de tokens e keywords
        self.tokens = tokens
        self.keywords = keywords

        # Estado encapsulado
        self.symbol_table = []
        self.token_count = {token: 0 for token in self.tokens}
        self.processed_tokens = []
        self.error_tokens = []

        # Construção do lexer
        self.lexer = lex.lex(module=self)

    def _reset_state(self):
        """ Limpa o estado interno para reprocessar um arquivo. """
        self.symbol_table = []
        self.token_count = {token: 0 for token in self.tokens}
        self.processed_tokens = []
        self.error_tokens = []
        if hasattr(self, 'lexer'):
            self.lexer.lineno = 1

    # Terminais Ocultos (Ignorados)
    t_ignore = ' \t'  # WS
    t_ignore_ML_COMMENT = r'\/\*[\s\S]*?\*\/'
    t_ignore_SL_COMMENT = r'\/\/[^^\n\r]*'

    # Símbolos simples (definidos como strings)
    t_AGGREGATION_OP = r'<>--'
    t_ARROW = r'--'
    t_DOTDOT = r'\.\.'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_DOT = r'\.'
    t_COLON = r':'
    t_AT = r'@'
    t_STAR = r'\*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Keywords Especiais (multi-palavra) — prioridade antes de t_ID
    def t_FUNCTIONAL_COMPLEXES(self, t):
        r'functional\s+complexes'
        return t

    def t_ABSTRACT_INDIVIDUALS(self, t):
        r'abstract\s+individuals'
        return t

    def t_INTRINSIC_MODES(self, t):
        r'intrinsic-modes'
        return t

    def t_EXTRINSIC_MODES(self, t):
        r'extrinsic-modes'
        return t

    # Regra para ID e Keywords
    def t_ID(self, t):
        r'[_a-zA-Z][\w_]*'
        t.type = self.keywords.get(t.value, 'ID')
        return t

    # Terminais (Literals)
    def t_STRING(self, t):
        r'"[^"]*"|\'[^\']*\''
        t.value = t.value[1:-1]
        return t

    def t_INT(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    # Tratamento de erros
    def t_error(self, t):
        self.error_tokens.append({
            'Token': 'ERRO',
            'Valor': t.value[0],
            'Linha': t.lineno,
            'Posição': t.lexpos
        })
        t.lexer.skip(1)

    # Processamento
    def process(self, data: str):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self._add_to_symbol_table(tok)

    def _add_to_symbol_table(self, token):
        if token.type in self.token_count:
            self.token_count[token.type] += 1
        self.processed_tokens.append(token)
        if not any(entry['Valor'] == token.value and entry['Token'] == token.type for entry in self.symbol_table):
            self.symbol_table.append({'Token': token.type, 'Valor': token.value})

    # Métodos utilitários de saída (mantidos aqui para compatibilidade)
    def show_tokens(self):
        print("\n====================== Tokens Processados ======================\n")
        header = f"{'Token':<25} {'Valor':<30} {'Linha':<6} {'Posição':<5}"
        print(header)
        print("-" * (25 + 30 + 6 + 5 + 3))
        for token in self.processed_tokens:
            valor_str = str(token.value)
            if len(valor_str) > 28:
                valor_str = valor_str[:25] + '...'
            print(f"{token.type:<25} {valor_str:<30} {token.lineno:<6} {token.lexpos:<5}")
        if self.error_tokens:
            print("\n=========================== Erros ===========================\n")
            err_header = f"{'Token':<25} {'Valor':<30} {'Linha':<6} {'Posição':<5}"
            print(err_header)
            print("-" * (25 + 30 + 6 + 5 + 3))
            for error in self.error_tokens:
                print(f"{error['Token']:<25} {error['Valor']:<30} {error['Linha']:<6} {error['Posição']:<5}")

    def show_symbol_table(self):
        print("\n================= Tabela de Símbolos (Entradas Únicas) =================\n")
        print(f"{'Token':<25} {'Valor':<30}")
        print("-" * 55)
        for entry in self.symbol_table:
            valor_str = str(entry['Valor'])
            if len(valor_str) > 28:
                valor_str = valor_str[:25] + '...'
            print(f"{entry['Token']:<25} {valor_str:<30}")

    def show_token_count(self):
        print("\n======= Contagem de Tokens =======\n")
        print(f"{'Token':<30} {'Quantidade':<10}")
        print("-" * 40)
        total = 0
        for token in sorted(self.token_count.keys()):
            count = self.token_count[token]
            if count > 0:
                print(f"{token:<30} {count:<10}")
                total += count
        print("-" * 40)
        print(f"{'TOTAL':<30} {total:<10}")
