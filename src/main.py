import json
import argparse
import pickle

import api

from modulos.tarefa_sp import tarefasp
from modulos.tarefa_sp import print_tarefasp

from modulos.boletim import boletim
from modulos.boletim import print_boletim

import util

caminho_para_auths_padrao = "./auths.json"

def valores_separados_por_virgula(value):
    return [x.strip().lower() for x in value.split(",")]

def modulo_tarefas(args:argparse.Namespace):
    print("Listando salas...")
    salas = tarefasp.obter_salas(auth)

    alvos_de_pub = tarefasp.obter_alvos_de_publicacao(salas)

    print("Listando disciplinas/categorias")
    categorias = tarefasp.obter_categorias(auth, alvos_de_pub)

    print("Listando tarefas...")
    tarefas_completas = tarefasp.obter_tarefas_completas(auth, args.req_tarefas)[::-1]
    tarefas_incompletas = tarefasp.obter_tarefas_incompletas(auth, alvos_de_pub, args.req_tarefas, "true")[::-1]
    tarefas_expiradas = tarefasp.obter_tarefas_incompletas(auth, alvos_de_pub, args.req_tarefas, "false")[::-1]

    print("Abrindo tarefas...")
    for tarefa in tarefas_completas:
        tarefa.abrir(auth)

    print_tarefasp.print_tarefasp(auth, args.exibir, tarefas_completas, tarefas_incompletas, tarefas_expiradas, categorias)

def modulo_boletim(args:argparse.Namespace):
    print("Obtendo boletim...")
    boletim_json = api.get_full_bulletin(auth, args.ano, 0)["data"]

    print_boletim.print_boletim(args, boletim_json)

parser = argparse.ArgumentParser(
    prog="Sala do Futuro",
    description="ferramenta que acessa automaticamente a plataforma Sala do Futuro, coleta os dados do aluno e os transforma em informações claras e úteis sobre o desempenho escolar."
)

parser.add_argument("-a", "--auths",
    default=caminho_para_auths_padrao, required=False,
    help="Caminho para o arquivo de logins (auths.json)"
)

parser.add_argument("auth",
    help="Um nome de um aluno configurado em auths.json. (caso --auths não seja especificado)"
)

subparsers = parser.add_subparsers(required=True)

tarefas_parser = subparsers.add_parser("tarefas", help="Coleta informações do TarefaSP")
tarefas_parser.set_defaults(func=modulo_tarefas)

tarefas_parser.add_argument("-e", "--exibir", required=True, type=valores_separados_por_virgula, 
    help="Lista de opções separadas por uma vírgula. Opções: completas,incompletas,expiradas,provas,media"
)

tarefas_parser.add_argument("-n", "--requisitar-tarefas", default=100, dest="req_tarefas", type=int, 
    help="O número de tarefas a serem requisitadas da Sala do Futuro. Não altere esse valor sem compreender o código, caso contrário algumas tarefas podem não aparecer."
)

boletim_parser = subparsers.add_parser("boletim", help="Coleta informações do boletim")
boletim_parser.set_defaults(func=modulo_boletim)
boletim_parser.add_argument("ano")

args = parser.parse_args()

auths = {}
with open(args.auths, "r") as f:
    auths = json.load(f)

if not (args.auth in auths.keys()):
    util.print_erro(f"O aluno {args.auth} não existe em auths.json.")
    exit(1)

print("Autenticando...")
auth = api.Auth(*auths[args.auth])

args.func(args)