from util import Data

def print_bimestres(data, escola):
    print(escola["NomeEscola"])
    for i in range(1, 5):
        for bimestre in data:
            if bimestre["NumeroBimestre"] != i:
                continue

            data_inicio = Data(bimestre["DataInicio"])
            data_fim = Data(bimestre["DataFim"])

            print(f"{bimestre["NumeroBimestre"]}º Bimestre:\nInicia: {data_inicio.dia_mes()} termina: {data_fim.dia_mes()}")
