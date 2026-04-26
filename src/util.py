def print_numero(f:float, soft:int=-1, hard:int=-1) -> str:
    f = float(f)
    numero_string = str(f).split(".")

    if soft > 0:
        return f"{numero_string[0]}.{numero_string[1].ljust(soft, "0")[:soft]}"
    if hard > 0:
        return f"{numero_string[0]}.{numero_string[1].ljust(hard, "0")}"[:hard]

    return ""

# Adiciona uma cor no padrão ansi em um string e reseta a cor no final
def embrulhar_cor(string:str, ansi_code:str):
    return f"{ansi_code}{string}\033[m"

def cortar_blocos(string, n):
    return [string[i:i+n] for i in range(0, len(string), n)]

class Data():
    data_bruta:str

    def __init__(self, data) -> None:
        self.data_bruta = data

    def separar(self):
        return self.data_bruta.split("T")

    def tempo(self):
        return self.separar()[1]

    def data(self):
        return self.separar()[0]

    def dia_mes_ano(self):
        return "/".join(self.data().split("-")[::-1])

    def dia_mes(self):
        return "/".join(self.data().split("-")[::-1][:2])
