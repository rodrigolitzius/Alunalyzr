import util
import defaults
from math import fsum
from . import boletim as boletim_util

def print_boletim(args, boletim):
    disciplinas = {}

    disciplinas_vistas = []
    for disciplina_dict in boletim:
        disciplina_classe = boletim_util.Disciplina(disciplina_dict["disciplinaId"], disciplina_dict["nomeDisciplina"])

        if not (disciplina_dict["disciplinaId"] in disciplinas_vistas):
            disciplinas[disciplina_classe] = []
            disciplinas_vistas.append(disciplina_dict["disciplinaId"])

        for disciplina in disciplinas:
            if disciplina.identificador == disciplina_dict["disciplinaId"]:
                disciplinas[disciplina].append(boletim_util.Desempenho(disciplina_dict))

    desempenhos_disponiveis = len(list(disciplinas.values())[0])

    for disciplina in disciplinas:
        disciplinas[disciplina] = boletim_util.ordenar_desempenhos(disciplinas[disciplina], desempenhos_disponiveis)

    colunas = ["DISCIPLINA", "1° BIMESTRE", "2° BIMESTRE", "3º BIMESTRE", "4º BIMESTRE", "CONSELHO FINAL"]
    espacamento = 23

    boletim_incompleto = False
    if desempenhos_disponiveis < 4:
        colunas = colunas[0:desempenhos_disponiveis+1]
        colunas.append("MÍNIMAS")
        boletim_incompleto = True

    print()

    for string in [x.ljust(espacamento) for x in colunas]:
        print(string, end="")
    print()

    for disciplina in disciplinas:
        desempenhos = disciplinas[disciplina]

        print(util.color("bold", "yellow") + util.truncate_string(disciplina.nome.title(), espacamento-3).ljust(espacamento), end="")

        for desempenho in desempenhos:
            if (desempenho is None): continue

            nota = desempenho.nota
            nota_str = str(float(nota)).ljust(4, "0")

            if desempenho.presenca is None: 
                presenca = 100
                presenca_str = "----"
            else:
                presenca = desempenho.presenca*100
                presenca_str = f"{round(presenca)}%"

            print(util.cor_da_pontuacao(desempenho.nota, "bold") + f"{nota_str}  " + util.cor_da_presenca(presenca, "bold") + f"{presenca_str}".ljust(espacamento-6) + util.RESET_COLOR, end="")

            if boletim_incompleto:
                notas = [x.nota for x in desempenhos if not (x is None)]
                presencas = [x.presenca for x in desempenhos if not (x is None)]

                nota_minima = ((defaults.nota_minima*4) - fsum(notas))/(4-desempenhos_disponiveis)
                nota_minima_str = str(util.print_numero(nota_minima, hard=4))
                presenca_minima = (((defaults.presenca_minima/100)*4) - fsum(presencas))/(4-desempenhos_disponiveis)

                print(f"{nota_minima_str}  {round(presenca_minima*100)}%", end="")
        print()

##### Parte de uma refatoração em progresso. Ignore. Esse código ainda pode ser substituido por completo #####
# def print_boletim(args, boletim_dict):
#     boletim = {}

#     escolas_vistas = []
#     for desempenho_dict in boletim_dict:
#         if not (desempenho_dict["escolaId"] in escolas_vistas):
#             boletim[boletim_util.Escola(desempenho_dict)] = {}
#             escolas_vistas.append(desempenho_dict["escolaId"])

#     fechamentos_vistos = []
#     for escola in boletim:
#         for desempenho_dict in boletim_dict:
#             # Esse fechamento já foi adicionado ao boletim
#             if desempenho_dict["tipoFechamentoId"] in fechamentos_vistos:
#                 continue

#             # Adiciona esse fechamento ao boletim
#             if desempenho_dict["escolaId"] == escola.identificador:
#                 boletim[escola][desempenho_dict["tipoFechamentoId"]] = {}
#                 fechamentos_vistos.append(desempenho_dict["tipoFechamentoId"])

#         # Resetando os fechamentos já adicionados antes de ir pra próxima escola
#         fechamentos_vistos = []

#     disciplinas_vistas = []
#     for escola in boletim:
#         for fechamento in boletim[escola]:
#             for desempenho_dict in boletim_dict:
#                 # Essa disciplina já foi adicionado ao fechamento
#                 if desempenho_dict["disciplinaId"] in disciplinas_vistas:
#                     continue

#                 # Adiciona essa disciplina ao fechamento
#                 if desempenho_dict["tipoFechamentoId"] == fechamento:
#                     boletim[escola][fechamento][boletim_util.Disciplina(desempenho_dict["disciplinaId"], desempenho_dict["nomeDisciplina"])] = []
#                     disciplinas_vistas.append(desempenho_dict["disciplinaId"])

#             disciplinas_vistas = []

#     for escola in boletim:
#         print(escola.nome)

#         for fechamento in boletim[escola]:
#             print(f"  {boletim_util.fechamento_id_para_bimestre[fechamento]}")

#             for disciplina in boletim[escola][fechamento]:
#                 print(f"    {disciplina.nome}")