from util import Data

def print_bimestres(data, escola):
    print(escola["NomeEscola"])
    bimestres_repetidos = []
    for i in range(1, 5):
        for bimestre in data:
            if (bimestre["NumeroBimestre"] != i) or (bimestre["NumeroBimestre"] in bimestres_repetidos):
                continue

            bimestres_repetidos.append(bimestre["NumeroBimestre"])

            data_inicio = Data(bimestre["DataInicio"])
            data_fim = Data(bimestre["DataFim"])

            print(f"{bimestre["NumeroBimestre"]}º Bimestre: {data_inicio.dia_mes()} - {data_fim.dia_mes()}")
