"""
Módulo responsável pela análise sintática e relatório de erros de ontologia.
Mantém o mesmo comportamento que antes existia dentro de lexer.py, porém
separado para melhor organização do código.
"""

# Estado interno da análise sintática
syntax_model = {
    'packages': {},
    'types': {
        'datatypes': set(),
        'enums': set(),
    },
    'external_relations': []
}

ontology_errors = []  # itens: { 'mensagem': str, 'linha': int, 'posicao': int, 'sugestao': str }


def reset_syntax_state():
    """Reinicia o estado da análise sintática/semântica."""
    global syntax_model, ontology_errors
    syntax_model = {
        'packages': {},
        'types': {
            'datatypes': set(),
            'enums': set(),
        },
        'external_relations': []
    }
    ontology_errors = []


# ===================== Funções auxiliares =====================
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


# ===================== Análise Sintática (Simplificada) =====================
def analyze_syntax(processed_tokens):
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
                    'mensagem': 'Estereótipo de classe sem nome da classe.',
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Informe o nome da classe após o estereótipo.'
                })
                i += 1
                continue

        # 4) Controle de chaves
        if t.type == 'SPECIAL_SYMBOL' and t.value == '{':
            brace_stack.append('{')
            i += 1
            continue
        if t.type == 'SPECIAL_SYMBOL' and t.value == '}':
            if brace_stack:
                popped = brace_stack.pop()
                if popped == 'class':
                    class_block_open = False
                    current_class = None
                    current_class_pkg = None
            else:
                ontology_errors.append({
                    'mensagem': 'Chave de fechamento sem abertura correspondente.',
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Verifique a estrutura de blocos.'
                })
            i += 1
            continue

        # Checagem de contexto de classe
        inside_class = class_block_open and (current_class is not None)

        # 5) Atributos (dentro de classe)
        if t.type == 'ATTRIBUTE' and inside_class:
            # Atributo: nome ':' tipo? (tipo pode ser NATIVE_DATATYPE, NEW_DATATYPE ou CLASS_NAME)
            name = t.value
            atype = None
            j = i + 1
            if j < n:
                nxt = processed_tokens[j]
                if nxt.type in ('NATIVE_DATATYPE', 'NEW_DATATYPE', 'CLASS_NAME'):
                    atype = nxt.value
                    j += 1
            _add_attribute(current_class_pkg or 'global', current_class, name, atype, t.lineno, t.lexpos)
            i = j
            continue

        # 6) Relações
        if t.type == 'KEYWORD' and t.value == 'relation':
            # Estrutura geral: relation NomeRel -- Alvo [card] dentro de classe, ou relation A -- B [card] no topo
            j = i + 1
            rel_name = None
            rel_stereo = last_rel_stereo
            last_rel_stereo = None
            # nome opcional
            if j < n and processed_tokens[j].type in ('RELATION_NAME', 'CLASS_NAME'):
                rel_name = processed_tokens[j].value
                j += 1
            # conector
            if j < n and processed_tokens[j].type == 'SPECIAL_SYMBOL' and processed_tokens[j].value in connectors:
                connector = processed_tokens[j].value
                j += 1
            else:
                ontology_errors.append({
                    'mensagem': "Relação sem conector ('--', '<>--', etc.).",
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Use um conector entre as classes na declaração da relação.'
                })
                i = j
                continue

            # alvo
            target = None
            if j < n and processed_tokens[j].type == 'CLASS_NAME':
                target = processed_tokens[j].value
                j += 1
            elif j < n and processed_tokens[j].type in ('RELATION_NAME', 'INSTANCE_NAME'):
                target = processed_tokens[j].value
                j += 1
            else:
                ontology_errors.append({
                    'mensagem': 'Relação sem classe/entidade alvo.',
                    'linha': t.lineno,
                    'posicao': t.lexpos,
                    'sugestao': 'Informe a classe alvo da relação.'
                })
                i = j
                continue

            # cardinalidade opcional
            cardinality = None
            if j < n and processed_tokens[j].type == 'CARDINALITY':
                cardinality = processed_tokens[j].value
                j += 1

            if inside_class and current_class:
                _add_relation(current_class_pkg or 'global', current_class, {
                    'name': rel_name or 'relation',
                    'stereotype': rel_stereo,
                    'target': target,
                    'cardinality': cardinality,
                    'connector': connector,
                    'line': t.lineno,
                    'pos': t.lexpos,
                })
            else:
                # relação externa
                syntax_model['external_relations'].append({
                    'name': rel_name or 'relation',
                    'stereotype': rel_stereo,
                    'from': None,
                    'to': target,
                    'cardinality': cardinality,
                    'connector': connector,
                    'line': t.lineno,
                    'pos': t.lexpos,
                })

            i = j
            continue

        # 6.1) Estereótipo de relação precedendo a palavra-chave relation
        if t.type == 'RELATION_STEREOTYPE':
            last_rel_stereo = t.value
            i += 1
            continue

        # 6.2) Relação no formato NomeRel -- Classe alvo (sem keyword) dentro de classe
        if inside_class and t.type in ('RELATION_NAME', 'CLASS_NAME'):
            # Verifica se a sequência é: nomeRel operador alvo [card]
            j = i + 1
            name_or_target = t.value
            if j < n and processed_tokens[j].type == 'SPECIAL_SYMBOL' and processed_tokens[j].value in connectors:
                connector = processed_tokens[j].value
                j += 1
                # alvo
                if j < n and processed_tokens[j].type in ('CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME'):
                    target = processed_tokens[j].value
                    j += 1
                    # cardinalidade
                    cardinality = None
                    if j < n and processed_tokens[j].type == 'CARDINALITY':
                        cardinality = processed_tokens[j].value
                        j += 1
                    _add_relation(current_class_pkg or 'global', current_class, {
                        'name': name_or_target,
                        'stereotype': last_rel_stereo,
                        'target': target,
                        'cardinality': cardinality,
                        'connector': connector,
                        'line': t.lineno,
                        'pos': t.lexpos,
                    })
                    last_rel_stereo = None
                    i = j
                    continue
            # caso não forme relação, segue fluxo normal

        # 6.3) Construto de relação externa completa: relation A -- B [card]
        if t.type == 'KEYWORD' and t.value == 'relation':
            # Esse bloco já foi tratado acima, mantido para clareza
            pass

        # 6.4) Declaração de classes em conjunto (genset) e especializações
        if t.type == 'KEYWORD' and t.value == 'genset':
            # Ex.: genset General { specifics A, B, C }
            # Simplificação: apenas valida a presença de nomes
            j = i + 1
            if j < n and processed_tokens[j].type in ('CLASS_NAME',):
                # nome do conjunto
                j += 1
            # Procura bloco specifics
            # Aqui não estruturamos no modelo, apenas reconhecemos tokens
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


def show_ontology_errors(lexical_errors=None):
    print("\n==================== Relatório de Erros da Ontologia ====================\n")
    if not ontology_errors and not lexical_errors:
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
    if lexical_errors:
        print("\nErros léxicos:")
        for err in lexical_errors:
            print(f"- Linha {err['Linha']}, pos {err['Posição']}: lexema inválido '{err['Valor']}'")
