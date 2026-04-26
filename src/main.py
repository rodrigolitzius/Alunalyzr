import argparse
import json
from sys import stderr

import pandas as pd
from requests_cache.session import CachedSession

from api import Api
from mod import boletim
from mod import info
from mod import bimestres
from mod import disciplinas
from mod import tarefasp

from config import config

# TODO Handle IsSuccess = False case for all modules

class CachedSessionForcarRefresh(CachedSession):
    def request(self, *args, **kwargs):
        kwargs["force_refresh"] = True
        return super().request(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs["force_refresh"] = True
        return super().post(*args, **kwargs)

def modulo_boletim(args):
    boletim_json = api.get_boletim_completo(args.ano)

    if boletim_json["data"] == []:
        print("Boletim vazio", file=stderr)
        return

    # Sim, "Success" está escrito errado...
    if not boletim_json["isSucess"]:
        print(f'Erro ao obter boletim: "{boletim_json["message"]}"', file=stderr)
        return

    df = pd.DataFrame(boletim_json["data"])

    boletim.print_boletim(df)

def modulo_info_pessoal(args):
    info_json = api.obter_aluno_por_codigo()

    if not info_json["isSuccess"]:
        print("ObterAlunoPorCodigo falhou:", info_json["message"])
        return

    info.print_info_pessoal(info_json["data"])

def modulo_bimestres(args):
    turmas = obter_turmas()

    for escola_id in pd.unique(turmas["CodigoEscola"]):
        bimestres_json = api.listar_bimestres(escola_id)["data"]

        bimestres.print_bimestres(bimestres_json, turmas[turmas["CodigoEscola"] == escola_id].iloc[0])

def modulo_disciplinas(args):
    disciplinas.print_disciplinas(pd.DataFrame(api.listar_disciplina_por_aluno()["data"]))

def obter_turmas():
    df = pd.DataFrame(api.listar_turmas_por_aluno()["data"])
    return df

def modulo_tarefasp(args):
    publication_targets = obter_publication_targets(obter_usuario())
    categorias = api.categories(publication_targets)
    expiradas_e_pendentes = pd.DataFrame(api.todo(publication_targets, answer_status=["draft", "pending"]))
    completas = pd.DataFrame(api.answer(publication_targets))

    tarefasp.print_tarefasp(expiradas_e_pendentes, completas, categorias)

def obter_usuario():
    return api.user()

def obter_publication_targets(user):
    lista = []
    for room in user["rooms"]:
        lista.append(room["name"])
        for group_cat in room["group_categories"]:
            lista.append(group_cat["id"])

    return lista

def resposta_hook(r):
    print(r.url)

with open("./usuarios.json", "r") as file:
    usuarios = json.load(file)

parser = argparse.ArgumentParser(
    prog="sdf", description="Coleta dados da Sala do Futuro"
)
parser.add_argument(
    "aluno",
    help="O nome do aluno, como especificado em usuarios.json",
    choices=usuarios.keys(),
)
parser.add_argument(
    "-c",
    "--cached",
    help="Prefere o cache se disponível",
    action="store_true",
    dest="cache",
)

parser.add_argument(
    "-f",
    "--offline",
    help="utiliza apenas o cache. Pode causar erros se os dados armazenados forem inválidos",
    action="store_true",
    dest="offline",
)

subparsers = parser.add_subparsers()

boletim_parser = subparsers.add_parser("boletim", help="Mostra o boletim do aluno")
boletim_parser.set_defaults(func=modulo_boletim)
boletim_parser.add_argument("ano")

info_pessoal_parser = subparsers.add_parser("info", help="Mostra informações pessoais do aluno")
info_pessoal_parser.set_defaults(func=modulo_info_pessoal)

disciplinas_parser = subparsers.add_parser("bimestres")
disciplinas_parser.set_defaults(func=modulo_bimestres)

disciplinas_parser = subparsers.add_parser("disciplinas")
disciplinas_parser.set_defaults(func=modulo_disciplinas)

tarefasp_parser = subparsers.add_parser("tarefasp")
tarefasp_parser.set_defaults(func=modulo_tarefasp)

args = parser.parse_args()

if (args.cache) or (args.offline):
    sessao_classe = CachedSession
else:
    sessao_classe = CachedSessionForcarRefresh

sessao = sessao_classe(
    "http_cache",
    backend="sqlite",
    allowable_methods=("GET", "POST"),
)

sessao.settings.read_only = args.offline
sessao.settings.only_if_cached = args.offline

sessao.headers.update({"User-Agent": config["avancado"]["user_agent"]})

api = Api(sessao)
api.autenticar(*usuarios[args.aluno])

args.func(args)
