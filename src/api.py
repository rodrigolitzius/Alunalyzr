import requests as rq

class Request:
    session = None
    def __init__(self, session) -> None:
        self.session = session

    def post(self, *args, **kwargs):
        resposta = self.session.post(*args, **kwargs)
        self.checar_resposta(resposta)
        return resposta

    def get(self, *args, **kwargs):
        resposta = self.session.get(*args, **kwargs)
        self.checar_resposta(resposta)
        return resposta

    def checar_resposta(self, resposta):
        resposta.raise_for_status()

class Auth:
    nome:str
    apelido:str
    cd_usuario:int
    token:str
    token2:str

    def __init__(self, usuario, senha, sessao):
        resposta = sessao.post(url="https://sedintegracoes.educacao.sp.gov.br/saladofuturobffapi/credenciais/api/LoginCompletoToken",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": "d701a2043aa24d7ebb37e9adf60d043b",
            },

            json={
                "user": usuario,
                "senha": senha
            }
        )

        resposta = resposta.json()

        self.nome = resposta["DadosUsuario"]["NAME"]
        self.cd_usuario = int(resposta["DadosUsuario"]["CD_USUARIO"])
        self.token = resposta["token"]

        resposta = sessao.post(url="https://edusp-api.ip.tv/registration/edusp/token",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "x-api-platform": "webclient",
                "x-api-realm": "edusp",
            },

            json={
                "token": self.token
            }
        ).json()

        self.token2 = resposta["auth_token"]
        self.apelido = resposta["nick"]

    @property
    def cd_usuario_curto(self):
        # Por algum motivo alguns endpoints só funcionam com cd_usuarios sem o último dígito
        return str(self.cd_usuario//10)

class Api:
    auth = None
    sessao = None
    handler = None

    def __init__(self, sessao=rq.Session()) -> None:
        self.sessao = sessao
        self.handler = Request(self.sessao)

    def autenticar(self, usuario, senha):
        self.auth = Auth(usuario, senha, self.handler)

    def get_boletim_completo(self, ano):
        resposta = self.handler.get(url=f"https://sedintegracoes.educacao.sp.gov.br/apiboletim/api/Boletim/GetBoletimCompleto?codigoAluno={self.auth.cd_usuario_curto}&anoLetivo={ano}&codigoTurma=0",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "ocp-apim-subscription-key": "a84380a41b144e0fa3d86cbc25027fe6",
            }
        )

        return resposta.json()

    def obter_aluno_por_codigo(self):
        resposta = self.handler.get(f"https://sedintegracoes.educacao.sp.gov.br/saladofuturobffapi/api/Aluno/ObterAlunoPorCodigo?codigoAluno={self.auth.cd_usuario_curto}",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": "d701a2043aa24d7ebb37e9adf60d043b",
                "Authorization": f"Bearer {self.auth.token}"
            }
        )

        return resposta.json()

    def listar_turmas_por_aluno(self):
        resposta = self.handler.get(f"https://sedintegracoes.educacao.sp.gov.br/apihubintegracoes/api/v2/Turma/ListarTurmasPorAluno?codigoAluno={self.auth.cd_usuario_curto}",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Ocp-Apim-Subscription-Key": "5936fddda3484fe1aa4436df1bd76dab",
            }
        )

        return resposta.json()

    def listar_bimestres(self, escola_id):
        resposta = self.handler.get(f"https://sedintegracoes.educacao.sp.gov.br/apihubintegracoes/api/v2/Bimestre/ListarBimestres?escolaId={escola_id}",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Ocp-Apim-Subscription-Key": "5936fddda3484fe1aa4436df1bd76dab"
            }
        )

        return resposta.json()

    def listar_disciplina_por_aluno(self):
        resposta = self.handler.get(f"https://sedintegracoes.educacao.sp.gov.br/apihubintegracoes/api/v2/Disciplina/ListarDisciplinaPorAluno?codigoAluno={self.auth.cd_usuario_curto}",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Ocp-Apim-Subscription-Key": "5936fddda3484fe1aa4436df1bd76dab"
            }
        )

        return resposta.json()

    def todo(self, publication_targets, answer_status=[], expired_only=False, limit=100, filter_expired=False, is_exam=False, is_essay=False):
        publication_targets_str = ""
        for pub_target in publication_targets:
            publication_targets_str += f"&publication_target={pub_target}"

        answer_statuses_str = ""
        for status in answer_status:
            answer_statuses_str += f"&answer_statuses={status}"

        resposta = self.handler.get(f"https://edusp-api.ip.tv/tms/task/todo?expired_only={expired_only}&limit={limit}&offset=0&filter_expired={filter_expired}&is_exam={is_exam}&with_answer=true&is_essay={is_essay}&with_apply_moment=true&{publication_targets_str}&{answer_statuses_str}",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "x-api-key": self.auth.token2,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "Priority": "u=4"
            },
        )

        return resposta.json()

    def user(self):
        resposta = self.handler.get("https://edusp-api.ip.tv/room/user?list_all=true&with_cards=true",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "x-api-key": f"{self.auth.token2}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "Priority": "u=4"
            }
        )

        return resposta.json()

    def categories(self, publication_targets):
        resposta = self.handler.get("https://edusp-api.ip.tv/tms/task/targets/categories",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "x-api-key": f"{self.auth.token2}"
            },

            params={
                "expired_only": False,
                "filter_expired": False,
                "publication_target": publication_targets
            }
        )

        return resposta.json()

    def answer(self, publication_targets:list):
        resposta = self.handler.get("https://edusp-api.ip.tv/tms/answer",
            headers = {
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "x-api-key": f"{self.auth.token2}",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site"
            },

            params={
                "nick": self.auth.apelido,
                "publication_target": publication_targets,
                "status": ["finished", "submitted"],
                # Curiosidade: Não dá pra passar um único field, se não o server retorna 400 e reclama que os fields devem ser um array. bruuuhhhhh
                "fields": ["task.title", "task.category_ids", "task.author", "task.allow_check_answer"]
            }
        )

        return resposta.json()
