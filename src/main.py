from tonto_lexer import TontoLexer
import sys
import os

def read_file(file_path):
    """ Tenta ler um arquivo e retorna seu conteúdo. """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"ERRO: Arquivo {file_path} não encontrado.")
        return None
    except Exception as e:
        print(f"ERRO: Erro ao processar o arquivo: {e}")
        return None


def gather_example_files():
    """Retorna uma lista de tuplas (rel_path, full_path) dos arquivos .tonto em src\\examples."""
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    files = []
    for root, _dirs, filenames in os.walk(examples_dir):
        for name in filenames:
            if name.lower().endswith(".tonto"):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, examples_dir)
                files.append((rel, full))
    files.sort(key=lambda x: x[0].lower())
    return files


def prompt_select_file():
    """Permite ao usuário escolher um arquivo manualmente ou selecionar um exemplo."""
    while True:
        print("\n===== Seleção de Arquivo =====")
        print("1. Digitar caminho completo")
        print("2. Escolher entre arquivos de exemplo (src\\examples)")
        choice = input("Escolha uma opção (1/2): ").strip()

        if choice == '1':
            path = input("Digite o caminho do arquivo: ").strip()
            return path
        elif choice == '2':
            examples = gather_example_files()
            if not examples:
                print("Nenhum arquivo de exemplo (.tonto) encontrado em src\\examples. Voltando.")
                continue
            print("\nArquivos de exemplo disponíveis:")
            for idx, (rel, _full) in enumerate(examples, start=1):
                print(f"{idx}. {rel}")
            sel = input("Escolha um número da lista (ou Enter para voltar): ").strip()
            if not sel:
                continue
            if sel.isdigit():
                idx = int(sel)
                if 1 <= idx <= len(examples):
                    return examples[idx - 1][1]
            print("Seleção inválida. Tente novamente.")
        else:
            print("Opção inválida. Tente novamente.")


def menu(lexer_instance: TontoLexer):
    """
    Executa o menu interativo, operando sobre a instância
    do lexer fornecida.
    """
    while True:
        print("\n====== MENU DE OPÇÕES (Analisador Tonto) ======")
        print("1. Exibir Tokens Processados")
        print("2. Exibir Tabela de Símbolos")
        print("3. Exibir Contagem de Tokens")
        print("4. Processar outro Arquivo")
        print("5. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            lexer_instance.show_tokens()
        elif choice == '2':
            lexer_instance.show_symbol_table()
        elif choice == '3':
            lexer_instance.show_token_count()
        elif choice == '4':
            file_path = prompt_select_file()
            data = read_file(file_path)
            if data is not None:
                # Limpa o estado antigo e processa o novo
                lexer_instance._reset_state()
                lexer_instance.process(data)
                print(f"Arquivo '{file_path}' processado com sucesso.")
        elif choice == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# --- 6. Execução Principal ---

if __name__ == "__main__":
    file_path = prompt_select_file()
    data = read_file(file_path)

    if data is not None:
        # 1. Cria a instância do lexer
        my_lexer = TontoLexer()

        # 2. Processa os dados iniciais
        my_lexer.process(data)
        print(f"Arquivo '{file_path}' processado com sucesso.")

        # 3. Inicia o menu, passando a instância do lexer
        menu(my_lexer)
    else:
        print("Nenhum arquivo processado. Encerrando.")
        sys.exit(1)