import api
from enum import Enum

class TarefaStatus(Enum):
    incompleta = 0
    completa = 1

class Sala:
    identificador:int
    nome:str
    topico:str
    operadores:list
    ids_de_categoria:list

    # Eu não tenho a menor ideia do que seja isso...
    categorias_de_grupo:list

    def __init__(self, sala:dict) -> None:
        self.identificador = sala["id"]
        self.nome = sala["name"]
        self.topico = sala["topic"]
        self.operadores = sala["oper"]
        self.ids_de_categoria = sala["category_ids"]
        self.categorias_de_grupo = sala["group_categories"]

class TarefaCartao:
    tem_resposta:bool
    tipo:str
    pontuacao_maxima:float|None
    pontuacao_recebida:float|None
    secao:int
    declaracao:str

    def __init__(self, tipo:str, pontuacao_maxima:float|None, pontuacao_recebida:float|None, secao:int, declaracao:str, tem_resposta:bool) -> None:
        self.tipo = tipo
        self.pontuacao_maxima = pontuacao_maxima
        self.pontuacao_recebida = pontuacao_recebida
        self.secao = secao
        self.declaracao = declaracao
        self.tem_resposta = tem_resposta

class TarefaSecao:
    identificador:int
    declaracao:str

    def __init__(self, identificador:int, declaracao:str) -> None:
        self.identificador = identificador
        self.declaracao = declaracao

class Tarefa:
    status:Enum
    identificador:int
    titulo:str
    autor:str
    expiracao:str
    e_prova:bool

    # De quais categorias essa tarefa faz parte. (Exemplo: Matemática, português, química, prova paulista...)
    ids_de_categoria:list

    # Esses valores podem não estar inicializados
    _identificador_resposta:int # Diferente de identificador
    _pontuacao_recebida:float
    _pontuacao_maxima:float
    _duracao:float
    _cartoes:list

    def __init__(self, status, tarefa) -> None:
        self.status = status
        self._cartoes = []

        # Esse valor tem que ser calculado manualmente
        self._pontuacao_maxima = -1

        # Esses valores não existem para tarefas incompletas
        self._pontuacao_recebida = -1
        self._identificador_resposta = -1
        self._duracao = -1

        # NOTA: id e task_id são diferentes
        # ["task_id"] existe caso a tarefa esteja completa e se refere ao id da tarefa em si
        # ["id"] existe tanto em tarefas completas quando em incompletas. Para tarefas completas,
        #   se refere ao id da resposta da tarefa. Já para incompletas ele se refere ao id da tarefa em si
        if status == TarefaStatus.completa:
            # Quando uma tarefa completa é requisitada, alguns valores têm 'task' como prefixo
            self.identificador = tarefa["task_id"]
            self.titulo = tarefa["task_title"]
            self.autor = tarefa["task_author"]
            self.expiracao = tarefa["task_expire_at"]
            self.ids_de_categoria = tarefa["task_category_ids"]
            self.e_prova = tarefa["task_is_exam"]

            self._duracao = float(tarefa["duration"])
            self._pontuacao_recebida = tarefa["result_score"]
            self._identificador_resposta = tarefa["id"]

        elif status == TarefaStatus.incompleta:
            self.identificador = tarefa["id"]
            self.titulo = tarefa["title"]
            self.autor = tarefa["author"]
            self.expiracao = tarefa["expire_at"]
            self.ids_de_categoria = tarefa["category_ids"]
            self.e_prova = tarefa["is_exam"]

    # Para acessar algumas informações da tarefa, é necessário abri-la
    def abrir(self, auth:api.Auth):
        # Não abra uma terefa sem ela estar respondida, caso contrário ela pode ser anulada
        if self.status != TarefaStatus.completa:
            return False

        # Esse valor também indica se a tarefa já foi respondida
        try: self.identificador_resposta
        except AttributeError: return False

        tarefa_completa = api.get_full_task_data(auth, self.identificador, self.identificador_resposta)

        respostas = tarefa_completa["answers"].values()
        questoes = tarefa_completa["task"]["questions"]

        self._pontuacao_maxima = get_pontuacao_maxima(tarefa_completa["task"]["questions"])

        # A API retorna duas listas: Uma com as questões da tarefa e outra com as respostas do aluno.
        # Por conveniência esse código juntas essas duas listas em uma só, para que todos os dados estejam no mesmo local
        for questao in questoes:
            # Nem todos os cartões são perguntas, e consequentemente não têm uma resposta,
            # por isso é necessario verificar cartao.tem_resposta
            resposta_da_questao = {}

            for resposta in respostas:
                if resposta["question_id"] == questao["id"]:
                    resposta_da_questao = resposta
                    break

            self._cartoes.append(
                TarefaCartao(
                    questao["type"], questao["score"], resposta_da_questao.get("score", None),
                    questao["section"], questao["statement"], resposta_da_questao != {}
                )
            )

    # Retorna se a tarefa tem uma ou mais seções
    def tem_secoes(self):
        for cartao in self.cartoes:
            if cartao.tipo == "section":
                return True

        return False

    @property
    def cartoes(self):
        if len(self._cartoes) > 0:
            return self._cartoes
        else:
            raise AttributeError("Esse valor ainda não vou inicializado.")

    @property
    def identificador_resposta(self):
        if self._identificador_resposta > 0:
            return self._identificador_resposta
        else:
            raise AttributeError("Esse valor ainda não vou inicializado.")

    @property
    def pontuacao_maxima(self):
        if self._pontuacao_maxima >= 0:
            return self._pontuacao_maxima
        else:
            raise AttributeError("Esse valor ainda não vou inicializado.")

    @property
    def pontuacao_recebida(self):
        if self._pontuacao_recebida >= 0:
            return self._pontuacao_recebida
        else:
            raise AttributeError("Esse valor ainda não vou inicializado.")

    @property
    def duracao(self):
        if self._duracao >= 0:
            return self._duracao
        else:
            raise AttributeError("Esse valor ainda não vou inicializado.")

class Categoria:
    identificador:int
    nome:str

    def __init__(self, identificador, nome) -> None:
        self.identificador = identificador

        # Por algum motivo o nome de algumas disciplinas são seguido por um número.
        # Exemplo: "Matemática - 1302"
        # Esse código remove esses números
        if "-" in nome:
            self.nome = nome.split("-")[0].strip()
        else:
            self.nome = nome

# Retorna o número de total de pontos em uma lista de questões
def get_pontuacao_maxima(questoes):
        # Nota: "Questões" não são necessariamente perguntas. Elas podem ser imagens que fazem parte da pergunta ou algum outro
        # elemento da tarefa
        maxima = 0

        for questao in questoes:
            if not questao["score"]:
                # Se não há uma pontuação atribuida, isso não é uma pergunta
                continue
            
            maxima += questao["score"]

        return maxima

# Retorna uma lista de classes Sala
def obter_salas(auth:api.Auth):
    salas = []
    salas_json = api.get_rooms(auth)["rooms"]

    for sala in salas_json:
        salas.append(Sala(sala))

    return salas

# Geralmente cada disciplina ou tarefa especial tem uma "categoria" atribuída
# Essa função retorna essas categorias
def obter_categorias(auth:api.Auth, alvos_de_pub):
    categorias = []
    categorias_json = api.get_categories(auth, alvos_de_publicacao_para_string(alvos_de_pub))

    for categoria_json in categorias_json:
        categorias.append(Categoria(categoria_json["id"], categoria_json["name"]))

    return categorias

# Retorna uma lista de classes Tarefa com as tarefas incompletas
def obter_tarefas_incompletas(auth:api.Auth, alvos_de_pub:list, limite:int, filtrar_expiradas:str):
    tarefas = []
    tarefas_json = api.get_incomplete_tasks(auth, alvos_de_publicacao_para_string(alvos_de_pub), filtrar_expiradas, limite)

    for tarefa_json in tarefas_json:
        tarefas.append(Tarefa(TarefaStatus.incompleta, tarefa_json))

    return tarefas

# Retorna uma lista de classes Tarefa com as tarefas completas
def obter_tarefas_completas(auth:api.Auth, limite:int):
    tarefas = []

    # Quais informações sobre a tarefa pedir a API
    parametros = [
        "id", "task_id", "status", "delivered_at", "result_score", "duration",
        "task.title", "task.author", "task.is_exam", "task.category_ids", "task.expire_at"
    ]

    tarefas_json = api.get_completed_tasks(auth, limite, parametros)

    for tarefa_json in tarefas_json:
        tarefas.append(Tarefa(TarefaStatus.completa, tarefa_json))

    return tarefas

def calcular_nota_tarefa(tarefa):
    return (tarefa.pontuacao_recebida/tarefa.pontuacao_maxima)*10

# coleta alvos de publicação. Esses parâmetros são usados, por exemplo, para requisitar as tarefas do tarefa SP
def obter_alvos_de_publicacao(salas:list):
    alvos = []

    # Alvos de pub. incluem:
    # Nome da sala
    for sala in salas:
        alvos.append(sala.nome)

    # IDs de categoria
    for sala in salas:
        for id_de_categoria in sala.ids_de_categoria:
            alvos.append(id_de_categoria)

    # IDs de categoria de grupos
    for sala in salas:
        for categoria_grupo in sala.categorias_de_grupo:
            alvos.append(categoria_grupo["id"])

    # NOTA: Alguns alvos podem estar repetidos
    return alvos

def alvos_de_publicacao_para_string(alvos:list):
    string = ""
    for alvo in alvos:
        string += f"publication_target={alvo}&"

    string = string[:len(string)-1]

    return string

# Retorna um dicionário no formato {TarefaSecao: [<Todos os cartões dentro dessa seção>]}
def cartoes_por_secao(tarefa:Tarefa):
    secoes = {}

    for cartao in tarefa.cartoes:
        if cartao.tipo == "section":
            secoes[TarefaSecao(cartao.secao, cartao.declaracao)] = []

    for cartao in tarefa.cartoes:
        for secao in secoes:
            if secao.identificador == cartao.secao:
                secoes[secao].append(cartao)
    
    return secoes

# Retorna em quais categorias uma tarefa está
def categorias_da_tarefa(tarefa:Tarefa, categorias):
    categorias_tarefa = []

    for categoria in categorias:
        if categoria.identificador in tarefa.ids_de_categoria:
            categorias_tarefa.append(categoria)

    return categorias_tarefa