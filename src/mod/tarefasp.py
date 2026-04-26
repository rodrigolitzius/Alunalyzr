import pandas as pd
from colorama import Fore, Style
from util import embrulhar_cor, Data

def obter_nomes_categoria(ids_categoria:list[int], categorias:dict):
    nome_categorias = []

    for categoria in categorias:
        if categoria["id"] in ids_categoria:
            nome_categorias.append(categoria["name"])

    return nome_categorias

def nome_e_disciplina(titulo:str, nome_categorias:list):
    return embrulhar_cor(f"* {titulo}", Fore.YELLOW+Style.BRIGHT) + \
    " - " + \
    embrulhar_cor(f"{", ".join(nome_categorias)}", Fore.CYAN+Style.BRIGHT)

def print_tarefasp(exp_e_pend:pd.DataFrame, completas:pd.DataFrame, categorias:dict):
    if not exp_e_pend.empty:
        a_fazer = exp_e_pend[(exp_e_pend["answer_id"].isna()) & (~exp_e_pend["task_expired"])]
        expiradas = exp_e_pend[exp_e_pend["task_expired"]]
    else:
        a_fazer = pd.DataFrame()
        expiradas = pd.DataFrame()

    a_fazer_vazio = a_fazer.empty
    expiradas_vazio = expiradas.empty
    completas_vazio = completas.empty

    print(embrulhar_cor("COMPLETAS", Fore.GREEN+Style.BRIGHT))
    if not completas_vazio:
        for row in completas.iterrows():
            row = row[1]
            nome_categorias = obter_nomes_categoria(row["task_category_ids"], categorias)

            print(nome_e_disciplina(row["task_title"], nome_categorias))
            print(f" - Publicada por: {row["task_author"]}")

            if row["enable_display_answers"]:
                pass
            else:
                print(embrulhar_cor(" - O resultado não foi liberado", Fore.RED))

            print()

    if not a_fazer_vazio:
        print(embrulhar_cor("PENDENTES", Fore.YELLOW+Style.BRIGHT))
        for row in a_fazer.iterrows():
            row = row[1]
            nome_categorias = obter_nomes_categoria(row["category_ids"], categorias)

            print(nome_e_disciplina(row["title"], nome_categorias))
            print(f" - Publicada por: {row["author"]}")

            data_expiracao = Data(row["expire_at"])
            print(f" - Expira em: {data_expiracao.dia_mes_ano()} às {data_expiracao.tempo()[:-5]}")

            print()

    print(embrulhar_cor("EXPIRADAS", Fore.RED+Style.BRIGHT))
    if not expiradas_vazio:
        for row in expiradas.iterrows():
            row = row[1]
            nome_categorias = obter_nomes_categoria(row["category_ids"], categorias)

            print(nome_e_disciplina(row["title"], nome_categorias))
            print(f" - Publicada por: {row["author"]}")
            print()
