import requests as rq

import util

DEFAULT_USER_AGENT = "User Agent"

class Auth:
    login: str
    password: str

    name: str # Nome do aluno

    nick: str # Uma combinação do RA e dígito
    student_code: int

    token1: str # Token dado por LoginCompletoToken
    token2: str # Dado por Token

    def __init__(self, login, password) -> None:
        self.login = login
        self.password = password

        self._login_completo_token()
        self._token()

    def _login_completo_token(self):
        request = APIEndpoint(
            url="https://sedintegracoes.educacao.sp.gov.br/credenciais/api/LoginCompletoToken",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",

                # Aparentemente essa chave é igual pra todo mundo...
                "Ocp-Apim-Subscription-Key": "2b03c1db3884488795f79c37c069381a"
            },

            json={
                "user": self.login,
                "senha": self.password
            }
        )
        
        response = request.post()

        self.nick = response["DadosUsuario"]["NM_NICK"]
        self.student_code = response["DadosUsuario"]["CD_USUARIO"]

        self.token1 = response["token"]
        self.name = response["DadosUsuario"]["NAME"]

    def _token(self):
        request = APIEndpoint(
            url=f"https://edusp-api.ip.tv/registration/edusp/token",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.5",
                "content-type": "application/json",
                "x-api-platform": "webclient",
                "x-api-realm": "edusp",
                "Priority": "u=4"
            },

            json={
                "token": self.token1
            }
        )

        response = request.post()

        self.token2 = response["auth_token"]

    @property
    def region(self):
        return self.login[-2:]

class APIEndpoint:
    url: str
    headers: dict
    json: dict

    expected_sc: list

    def __init__(self, url:str, headers:dict, json:dict={}, expected_sc:list=[200], user_agent:str=f"{DEFAULT_USER_AGENT}") -> None:
        self.url = url
        self.headers = {
            "User-Agent": user_agent,
            **headers
        }
        self.json = json

        self.expected_sc = expected_sc

    def post(self) -> dict:
        response = rq.post(
            url=self.url,
            headers=self.headers,
            json=self.json
        )

        self.check_response(response)

        return response.json()

    def get(self) -> dict:
        response = rq.get(
            url=self.url,
            headers=self.headers,
            json=self.json
        )

        self.check_response(response)

        return response.json()

    def check_response(self, response:rq.Response):
        if not (response.status_code in self.expected_sc):
            util.print_erro(f"Código de status inexperado: {response.status_code}.", False)
            util.print_erro(f"URL: {self.url}")

def lista_para_parametros(nome_parametro:str, parametros:list):
    string = ""

    for parametro in parametros:
        string += f"{nome_parametro}={parametro}&"

    return string[:len(string)-1]

def get_completed_tasks(auth:Auth, limit:int, fields:list):
    endpoint = APIEndpoint(
        url=f"https://edusp-api.ip.tv/tms/answer?nick={auth.nick}-{auth.region}&limit={str(limit)}&offset=0&status=submitted&status=finished&{lista_para_parametros("fields", fields)}",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "x-api-key": auth.token2
        }
    )

    return endpoint.get()

def get_disciplines(auth:Auth, ano:int):
    endpoint = APIEndpoint(
        url=f"https://sedintegracoes.educacao.sp.gov.br/apihubintegracoes/api/v2/Disciplina/ListarDisciplinaPorAluno?codigoAluno={auth.student_code}",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Ocp-Apim-Subscription-Key": "5936fddda3484fe1aa4436df1bd76dab"
        }
    )

    return endpoint.get()

def get_rooms(auth:Auth):
    endpoint = APIEndpoint(
        url=f"https://edusp-api.ip.tv/room/user?list_all=true&with_cards=true",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "x-api-key": auth.token2,
        }
    )

    return endpoint.get()

def get_incomplete_tasks(auth:Auth, publication_targets:str, filter_expired:str, limit:int):
    expired_only = "true"

    if filter_expired == "true":
        expired_only = "false"

    endpoint = APIEndpoint(
        url = f"https://edusp-api.ip.tv/tms/task/todo?expired_only={expired_only}&limit={str(limit)}&offset=0&filter_expired={filter_expired}&{publication_targets}",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "x-api-key": auth.token2,
        }
    )

    return endpoint.get()

def get_full_task_data(auth:Auth, task_id, other_id):
    endpoint = APIEndpoint(
        url=f"https://edusp-api.ip.tv/tms/task/{task_id}/answer/{other_id}?with_task=true&with_genre=true&with_questions=true&with_assessed_skills=true",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "x-api-key": auth.token2,
        }
    )

    return endpoint.get()

def get_categories(auth:Auth, publication_targets:str):
    endpoint = APIEndpoint(
        url=f"https://edusp-api.ip.tv/tms/task/targets/categories?expired_only=false&filter_expired=false&{publication_targets}",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "x-api-key": auth.token2
        }
    )

    return endpoint.get()

def get_bulletin(auth:Auth, ano, bimestre):
    print(auth.student_code)
    endpoint = APIEndpoint(
        # O código de usuário (auth.student_code) usado nas requisições não tem o número final por algum motivo...
        url=f"https://sedintegracoes.educacao.sp.gov.br/apiboletim/api/Frequencia/ConsultaFrequenciaBimestre?codigoAluno={int(auth.student_code/10)}&anoLetivo={ano}&bimestre={bimestre}&somenteAtivo=0",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Ocp-Apim-Subscription-Key": "a84380a41b144e0fa3d86cbc25027fe6",
        }
    )

    return endpoint.get()

def get_full_bulletin(auth:Auth, ano:int, codigo_turma:int):
    endpoint = APIEndpoint(
        url=f"https://sedintegracoes.educacao.sp.gov.br/apiboletim/api/Boletim/GetBoletimCompleto?codigoAluno={int(auth.student_code/10)}&anoLetivo={ano}&codigoTurma={codigo_turma}",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Ocp-Apim-Subscription-Key": "a84380a41b144e0fa3d86cbc25027fe6",
        }
    )

    return endpoint.get()

def get_last_missed_days(auth:Auth, ano:int):
    endpoint = APIEndpoint(
        url=f"https://sedintegracoes.educacao.sp.gov.br/apiboletim/api/Frequencia/GetAlunoUltimosDiasFalta?codigoAluno={int(auth.student_code/10)}&anoLetivo={ano}",
        headers={
            "Ocp-Apim-Subscription-Key": "a84380a41b144e0fa3d86cbc25027fe6",
        },
    )

    return endpoint.get()