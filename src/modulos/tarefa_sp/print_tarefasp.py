import api
import util
from . import tarefasp

def print_tarefa_completa_info(tarefa:tarefasp.Tarefa, categorias:list):
    limite_nome_da_secao = 30

    categorias_tarefa = tarefasp.categorias_da_tarefa(tarefa, categorias)

    print(f"{util.color("bold", "yellow")}{tarefa.titulo.strip()}{util.color("bold", "cyan")} - {"/".join([x.nome for x in categorias_tarefa])}" + util.RESET_COLOR)
    print(f" - Publicada por: {tarefa.autor}")

    tempo_str = "segundos"
    duracao = tarefa.duracao

    if tarefa.duracao >= 60:
        tempo_str = "minutos"
        duracao = tarefa.duracao/60

    if tarefa.duracao >= 3600:
        tempo_str = "horas"
        duracao = tarefa.duracao/3600

    print(f" - Completa em {round(duracao, 2)} {tempo_str}.")

    if tarefa.tem_secoes():
        print(util.color("bold", "yellow") + f" * SEÇÕES" + util.RESET_COLOR)
        secoes = tarefasp.cartoes_por_secao(tarefa)

        nomes_das_secoes = []
        for secao in secoes:
            nome_da_secao = secao.declaracao.strip()
            # Algumas seções têm uma declaração em HTML ou têm nomes desnecessariamente longos
            nome_da_secao = util.truncate_string(nome_da_secao, limite_nome_da_secao)

            nomes_das_secoes.append(nome_da_secao)
        maior_nome_secao = util.get_longest_string(nomes_das_secoes)

        for i, secao in enumerate(secoes):

            pontuacao_maxima = 0
            pontuacao_recebida = 0

            for cartao in secoes[secao]:
                # Verifica se o cartão é uma pergunta e tem uma resposta atribuída
                if not cartao.tem_resposta:
                    continue

                pontuacao_maxima += cartao.pontuacao_maxima
                pontuacao_recebida += cartao.pontuacao_recebida

            nota_secao = (pontuacao_recebida/pontuacao_maxima)*10

            nota_perdida = ((pontuacao_maxima-pontuacao_recebida)/tarefa.pontuacao_maxima)*100

            print(util.cor_da_pontuacao(nota_secao) + f"  - {nomes_das_secoes[i].ljust(maior_nome_secao)}  -  {f"{util.print_numero(nota_secao, hard=4)}"}. {f"{pontuacao_recebida} pontos de {pontuacao_maxima}.".ljust(19)} (-{round(nota_perdida)}%)")

    nota = tarefasp.calcular_nota_tarefa(tarefa)

    print(util.cor_da_pontuacao(nota) + f" - Nota geral: {util.print_numero(nota, hard=4)}. {tarefa.pontuacao_recebida} pontos de {tarefa.pontuacao_maxima}" + util.RESET_COLOR)
    print()

def print_tarefa_incompleta_info(tarefa:tarefasp.Tarefa, categorias:list):
    categorias_tarefa = tarefasp.categorias_da_tarefa(tarefa, categorias)

    print(f"{util.color("bold", "yellow")}{tarefa.titulo.strip()}{util.color("bold", "cyan")} - {"/".join([x.nome for x in categorias_tarefa])}" + util.RESET_COLOR)
    print(f" - Publicada por: {tarefa.autor}")

    data_expiracao = tarefa.expiracao.split("T")[0]
    horario_expiracao = tarefa.expiracao.split("T")[1][:-1]

    print(f" - Expira em: {util.relative_time(data_expiracao, horario_expiracao)}")

    print()

def print_tarefas_expiradas(tarefas_completas:list[tarefasp.Tarefa], tarefas_incompletas:list[tarefasp.Tarefa], tarefas_expiradas:list[tarefasp.Tarefa]):
    print(util.color("bold", "red") + "==== TAREFAS EXPIRADAS ====" + util.RESET_COLOR)
    print(f" - Você tem {len(tarefas_expiradas)} tarefas expiradas.")
    porcentagem_expiradas = (len(tarefas_expiradas)/(len(tarefas_completas) + len(tarefas_incompletas) + len(tarefas_expiradas)))*100
    print(f" - Isso é {util.print_numero(porcentagem_expiradas, hard=4)}% de todas as tarefas publicadas.")
    print()

def print_media(tarefas_completas:list[tarefasp.Tarefa], categorias:list):
    # Media de nota em todas as tarefas dessa categoria
    print(util.color("bold", "cyan") + "=== MÉDIAS ===" + util.RESET_COLOR)
    print(" * Não inclui seções de tarefas!\n")
    for categoria in categorias:
        media_total = 0

        soma_notas = 0
        nr_de_tarefas = 0

        # Calcula a nota de cada tarefa dentro de uma categoria para adicionar a média
        for tarefa in tarefas_completas:
            if categoria.identificador in tarefa.ids_de_categoria:
                soma_notas += tarefasp.calcular_nota_tarefa(tarefa)
                nr_de_tarefas += 1

        longest_name = util.get_longest_string([x.nome for x in categorias])

        # Nem todas as categorias têm tarefas 
        if nr_de_tarefas > 0:
            nota = soma_notas/nr_de_tarefas
            print(util.cor_da_pontuacao(nota), end="")
            print(f" - {categoria.nome.ljust(longest_name)}  {util.print_numero(nota, hard=4)}")
            print(util.RESET_COLOR, end="")
        else:
            print(f" - {categoria.nome.ljust(longest_name)}  -.--")

def print_tarefasp(auth:api.Auth, exibir:list, tarefas_completas:list[tarefasp.Tarefa], tarefas_incompletas:list[tarefasp.Tarefa], tarefas_expiradas:list[tarefasp.Tarefa], categorias:list):
    print(util.color("bold", "yellow") + f"==== TarefaSP de {auth.name} ====" + util.RESET_COLOR)

    # Estou iterando cada elemento para que a ordem que sejam printados seja a mesma do que o usuário escreveu no terminal
    for tipo in exibir:
        if tipo == "completas":
            print(util.color("bold", "green") + "==== TAREFAS COMPLETAS ====" + util.RESET_COLOR)
            for tarefa in tarefas_completas:
                print_tarefa_completa_info(tarefa, categorias)

        if tipo == "incompletas":
            print(util.color("bold", "yellow") + "==== TAREFAS INCOMPLETAS ====" + util.RESET_COLOR)
            for tarefa in tarefas_incompletas:
                print_tarefa_incompleta_info(tarefa, categorias)

        if tipo == "expiradas":
            print_tarefas_expiradas(tarefas_completas, tarefas_incompletas, tarefas_expiradas)

        if tipo == "provas":
            print(util.color("bold", "purple") + "==== PROVAS ====" + util.RESET_COLOR)
            for tarefa in [tarefa for tarefa in tarefas_completas if tarefa.e_prova]:
                print_tarefa_completa_info(tarefa, categorias)
            print()

        if tipo == "media":
            print_media(tarefas_completas, categorias)
