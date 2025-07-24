import json
from datetime import datetime, timedelta
from sys import stderr
import defaults

##### TODO: Traduzir esse arquivo por completo #####
# Esse código foi transplantado de uma versão antiga desse projeto, onde o código estava escrito em inglês

def print_json(data:dict|list):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def print_numero(f:float, soft:int=-1, hard:int=-1) -> str:
    f = float(f)
    numero_string = str(f).split(".")

    if soft > 0:
        return f"{numero_string[0]}.{numero_string[1].ljust(soft, "0")[:soft]}"
    if hard > 0:
        return f"{numero_string[0]}.{numero_string[1].ljust(hard, "0")}"[:hard]

    return ""

RESET_COLOR = "\033[m"
# Returns a color ANSI escape code
def color(style, fg, bg=""):
    colors = {
        "white":  97,
        "green":  32,
        "yellow": 33,
        "red":    31,
        "purple": 35,
        "cyan":   36,
    }

    styles = {
        "none": 0,
        "bold": 1
    }

    if not bg:
        return f"\033[{styles[style]};{colors[fg]}m"

    return f"\033[{styles[style]};{colors[fg]};{colors[fg]+10}m"

def get_longest_string(strings:list):
    longest_string_len = 0

    for string in strings:
        if len(string) > longest_string_len:
            longest_string_len = len(string)

    return longest_string_len

def relative_time(date_str:str, time_str:str):
    now = datetime.now()
    date = datetime.strptime(date_str, "%Y-%m-%d")
    time = timedelta(hours=int(time_str[:2]), minutes=int(time_str[3:5]), seconds=int(time_str[6:8]))

    delta = (date+time) - now

    days = delta.total_seconds() / 60 / 60 / 24
    hours = (days - int(days)) * 24
    minutes = (hours - int(hours)) * 60

    return f"{int(days)} dias, {int(hours)} horas e {int(minutes)} minutos"

def print_erro(erro:str, sair=True, codigo_saida=1):
    print(f"[ERRO] {erro}", file=stderr)

    if sair == True:
        exit(codigo_saida)

def truncate_string(string:str, n:int):
    if len(string) > n:
        return string[:n-3] + "..."
    else:
        return string

# retorna vermelho, ciano ou verde dependendo do quão bom é a pontuação em relação à mínima
def cor_da_pontuacao(pontuacao:float, estilo_cor:str="none"):
    if pontuacao < defaults.nota_minima:
        return color(estilo_cor, "red")

    if pontuacao >= (defaults.nota_minima+1):
        return color(estilo_cor, "green")

    if pontuacao >= (defaults.nota_minima):
        return color(estilo_cor, "cyan")

    return ""

# retorna vermelho, ciano ou verde dependendo do quão bom é a presença em relação à mínima
def cor_da_presenca(presenca:float, estilo_cor:str="none"):
    if presenca < defaults.presenca_minima:
        return color(estilo_cor, "red")

    if presenca >= (defaults.presenca_minima+10):
        return color(estilo_cor, "green")

    if presenca > (defaults.presenca_minima):
        return color(estilo_cor, "cyan")

    return ""