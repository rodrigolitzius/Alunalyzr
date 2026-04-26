import pandas as pd
from util import embrulhar_cor

def print_disciplinas(data):
    turmas = data[["CodigoTurma", "IdentificadorTurma", "DescricaoTurma"]]

    print("* Os nomes podem estar incompletos")
    for turma in pd.unique(turmas["CodigoTurma"]):
        disciplinas = data[data["CodigoTurma"] == turma]

        nome_disciplina = turmas[turmas["CodigoTurma"] == turma].iloc[0]["DescricaoTurma"]

        print(embrulhar_cor(nome_disciplina, "\033[1m"))
        for disciplina in disciplinas["NomeDisciplina"]:
            print("-", disciplina.title())
