import numpy as np
import pandas as pd
from tabulate import tabulate

import util
from config import config

# TODO
# GERENCIAR MULTIPLAS ESCOLAS

# Essa lista mapeia os bimestres para tipoFechamentoId
bimestre_para_fechamento = [5, 6, 7, 8, 10]


# Retorna todos os registros referentes a um bimestre
def obter_bimestre(df, bimestre):
    # tipoFechamentoId é o bimestre que uma linha na tabela representa
    resultado = df[df["tipoFechamentoId"] == bimestre_para_fechamento[bimestre]]

    return resultado


# Obtém o desempenho de uma disciplina em todos os bimestres + CF
def obter_desempenho_disciplina(escola: pd.DataFrame, disciplina: str):
    desempenho = escola[escola["nomeDisciplina"] == disciplina]
    desempenho = desempenho[desempenho["tipoFechamentoId"] != bimestre_para_fechamento[4]]
    desempenho = desempenho[["notaAtribuida", "nivelNota", "porcentagemFrequencia", "tipoFechamentoId"]]

    desempenho_cf = escola[escola["nomeDisciplina"] == disciplina]
    desempenho_cf = desempenho_cf[desempenho_cf["tipoFechamentoId"] == bimestre_para_fechamento[4]]
    desempenho_cf = desempenho_cf[["notaAtribuidaMediaFinal", "nivelNotaMediaFinal", "porcentagemFrequencia", "tipoFechamentoId"]]

    desempenho_cf = desempenho_cf.rename(columns={
        "notaAtribuidaMediaFinal": "notaAtribuida",
        "nivelNotaMediaFinal": "nivelNota"
    })

    concat = pd.concat([desempenho, desempenho_cf], ignore_index=True)
    concat = concat.sort_values(by="tipoFechamentoId", ascending=True)

    return concat


# Tenta descobrir o número de bimestres completos
def obter_bimestres_concluidos(escola: pd.DataFrame):
    fechamentos = pd.unique(escola["tipoFechamentoId"])

    bimestres_completos = 0

    for fechamento in fechamentos:
        bimestres_completos += 1

    return bimestres_completos


# Mapeia uma cor a um nível de nota
# note que nivelNota é um valor provido pela própria API,
# logo essa função não utiliza a configuração de nota mínima
def cor_nivel_nota(nivel_nota):
    if nivel_nota == 3:
        return "\033[1;32m"
    if nivel_nota == 2:
        return "\033[1;33m"
    if nivel_nota == 1:
        return "\033[1;31m"

    return "\033[0;37m"


# Mapeia valores de frequencia (0 a 100) para cores
# O mapeamente de cores depende exclusivamente da
# configuração de presença mínima
def cor_frequencia(frequencia):
    minima = config["aluno"]["frequencia_minima"]

    if frequencia >= minima:
        return "\033[1;32m"
    if frequencia < minima:
        return "\033[1;31m"

    return "\033[0;37m"


def print_boletim(boletim_df: pd.DataFrame):
    boletim_df = boletim_df[["nomeEscola", "nomeDisciplina", "notaAtribuida", "notaAtribuidaMediaFinal", "nivelNota", "nivelNotaMediaFinal", "porcentagemFrequencia", "tipoFechamentoId"]]
    # Substituindo os valores NaN na tabela por None
    boletim_df = boletim_df.replace({np.nan: None})
    # Filtra o dataframe para que tal contenha APENAS fechamentoIds entre 1 e 4 + CF
    boletim_df = boletim_df[
        boletim_df["tipoFechamentoId"].isin([bimestre_para_fechamento[x] for x in range(0, 5)])
    ]

    _escolas = pd.unique(boletim_df["nomeEscola"])
    disciplinas = pd.unique(boletim_df["nomeDisciplina"])
    bimestres_concluidos = obter_bimestres_concluidos(boletim_df)

    bimestres = []
    for bimestre_numero in range(0, 5):
        bimestres.append(obter_bimestre(boletim_df, bimestre_numero))

    # Tabela para printar no terminal
    tabela = []

    # Construindo a tabela
    for i, disciplina in enumerate(disciplinas):
        # Limitando o nome da disciplina
        if len(disciplina) > 20:
            nome_disciplina = disciplina.title()[0:20]
            nome_disciplina += "..."
        else:
            nome_disciplina = disciplina.title()

        tabela.append([nome_disciplina])

        desempenho_disciplina = obter_desempenho_disciplina(boletim_df, disciplina)

        frequencias = list(desempenho_disciplina["porcentagemFrequencia"])
        notas = list(desempenho_disciplina["notaAtribuida"])
        niveis_notas = list(desempenho_disciplina["nivelNota"])

        for bimestre in range(0, bimestres_concluidos):
            conselho_final = bimestre == 4

            try:
                nota = notas[bimestre]
            except IndexError:
                nota = None

            try:
                nivel_nota = niveis_notas[bimestre]
            except IndexError:
                nivel_nota = None

            desempenho_str = util.embrulhar_cor(
                string=str(float(notas[bimestre]) if nota is not None else "-.--"),
                ansi_code=str(cor_nivel_nota(nivel_nota)),
            )

            tabela[i].append(desempenho_str)

            # A frequência não existe no CF. A única forma de
            frequencias_invalidas = None in frequencias[0:4]

            try:
                frequencia = frequencias[bimestre]
            except IndexError:
                frequencia = None
                frequencias_invalidas = True

            if conselho_final and (not frequencias_invalidas):
                # Apenas calcula a frequência pro CF se todas as frequencias anteriores forem válidas
                desempenho_frequencia = float(
                    sum(frequencias[0:4]) / len(frequencias[0:4])
                )
            elif frequencia is None:
                # Não printe essa frequencia caso ela seja None
                # Qualquer frequencia válida vai passar sem executar esse elif
                desempenho_frequencia = "-.--"
            else:
                # Por fim, se a frequencia for valida, ela passa por aqui
                desempenho_frequencia = float(frequencia)

            desempenho_str = util.embrulhar_cor(
                f"{desempenho_frequencia}%",
                cor_frequencia(desempenho_frequencia)
                if isinstance(desempenho_frequencia, float)
                else "",
            )

            tabela[i].append(desempenho_str)

        # Caso o aluno tenha um bimestre incompleto, calcule as mínimas de notas e frequencias
        if bimestres_concluidos < 4:
            for j, nota in enumerate(notas):
                if nota is not None:
                    continue
                notas[j] = config["aluno"]["nota_minima"]

            for j, frequencia in enumerate(frequencias):
                if frequencia is not None:
                    continue
                frequencias[j] = config["aluno"]["frequencia_minima"]

            nota_minima = ((config["aluno"]["nota_minima"] * 4) - sum(notas)) / (4 - bimestres_concluidos)
            frequencia_minima = ((config["aluno"]["frequencia_minima"] * 4) - sum(frequencias)) / (4 - bimestres_concluidos)

            if nota_minima <= 0:
                nota_cor = "\033[0;34m"
            else:
                nota_cor = "\033[0;35m"

            if frequencia_minima < config["aluno"]["frequencia_minima"]:
                frequencia_cor = "\033[0;34m"
            else:
                frequencia_cor = "\033[0;35m"

            tabela[i].append(util.embrulhar_cor(
                str(nota_minima if nota_minima > 0 else float(0)), nota_cor
            ))

            tabela[i].append(util.embrulhar_cor(
                f"{float(frequencia_minima) if frequencia_minima > 0 else float(0)}%",
                frequencia_cor,
            ))

    # Criando os nomes das colunas
    headers = ["DISCIPLINA"]
    for bimestre in range(0, bimestres_concluidos):
        if bimestre == 4:
            headers.append("CF")
        else:
            headers.append(f"{bimestre + 1}B")
        headers.append("%")

    if bimestres_concluidos < 4:
        headers.append("Nota")
        headers.append("Freq")

    print(tabulate(tabela, headers=headers, floatfmt=".2f"))
