import util
from math import fsum
import defaults

fechamento_id_para_bimestre = {
    5: 1,
    6: 2,
    7: 3,
    8: 4,
    10: 5 # o 5º bimestre é o conselho final
}

def ordenar_desempenhos(desempenhos:list, bimestres:int):
    ordenado = [None for _ in range(bimestres)]

    for desempenho in desempenhos:
        ordenado[fechamento_id_para_bimestre[desempenho.fechamento_id]-1] = desempenho

    return ordenado

class Disciplina:
    identificador:int
    nome:str

    def __init__(self, identificador:int, nome:str) -> None:
        self.identificador = identificador
        self.nome = nome

class Desempenho:
    fechamento_id:int
    nota:float|None
    presenca:float|None
    escola_identificador:int
    escola_nome:str

    def __init__(self, desempenho_dict:dict) -> None:
        self.fechamento_id = desempenho_dict["tipoFechamentoId"]
        self.nota = desempenho_dict["notaAtribuida"]
        self.escola_identificador = desempenho_dict["escolaId"]
        self.escola_nome = desempenho_dict["nomeEscola"]

        if self.nota is None:
            self.nota = desempenho_dict["notaAtribuidaMediaFinal"]

        self.presenca = None

        if desempenho_dict["quantidadeAulasRealizadas"] != 0:
            self.presenca = 1 - (desempenho_dict["numeroFaltas"]/desempenho_dict["quantidadeAulasRealizadas"])

class Escola:
    nome:str
    identificador:int

    def __init__(self, desempenho_dict) -> None:
        self.nome = desempenho_dict["nomeEscola"]
        self.identificador = desempenho_dict["escolaId"]
