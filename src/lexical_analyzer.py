import ply.lex as lex

# Lista de tokens
tokens = [
    'KEYWORD', 'CLASS_ID', 'PROPERTY_ID', 'SPECIAL_SYMBOL', 
    'INDIVIDUAL_NAME', 'DATATYPE', 'CARDINALITY'
]

# Palavras reservadas
keywords = {
    'some', 'all', 'value', 'min', 'max', 'exactly', 'that',
    'not', 'and', 'or', 'only', 'Class:', 'EquivalentTo:', 
    'Individuals:', 'SubClassOf:', 'DisjointClasses:'
}

# Tipos de dados válidos
valid_datatypes = {
    "owl:rational", "owl:real", "rdf:langString", "rdf:PlainLiteral",
    "rdf:XMLLiteral", "rdfs:Literal", "xsd:anyURI", "xsd:base64Binary",
    "xsd:boolean", "xsd:byte", "xsd:dateTime", "xsd:dateTimeStamp",
    "xsd:decimal", "xsd:double", "xsd:float", "xsd:hexBinary", "xsd:int",
    "xsd:integer", "xsd:language", "xsd:long", "xsd:Name", "xsd:NCName",
    "xsd:negativeInteger", "xsd:NMTOKEN", "xsd:nonNegativeInteger",
    "xsd:nonPositiveInteger", "xsd:normalizedString", "xsd:positiveInteger",
    "xsd:short", "xsd:string", "xsd:token", "xsd:unsignedByte", "xsd:unsignedInt",
    "xsd:unsignedLong", "xsd:unsignedShort"
}

symbol_table = []
token_count = {token: 0 for token in tokens}
processed_tokens = [] 
error_tokens = []

# Expressões regulares para os tokens
def t_KEYWORD(t):
    r'\b(some|all|value|min|max|exactly|that|not|and|or|only)\b|Class:|EquivalentTo:|Individuals:|SubClassOf:|DisjointClasses:'
    if t.value in keywords:
        t.type = 'KEYWORD'
    #add_to_symbol_table(t)
    return t

def t_DATATYPE(t):
    r'(xsd|owl|rdf|rdfs):[a-zA-Z]+(?:[a-zA-Z0-9]*)?'
    if t.value in valid_datatypes:
        #add_to_symbol_table(t)
        return t

def t_INDIVIDUAL_NAME(t):
    r'[A-Z][a-z]*[a-zA-Z]*[0-9]+'
    #add_to_symbol_table(t)
    return t