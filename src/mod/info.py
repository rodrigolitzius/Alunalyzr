import util

def print_info_pessoal(info):
    data_nasc = util.Data(info["DataNascimento"])
    print(f"Aluno: {info["NomeAluno"].title()}")
    print(f"Data Nasc: {data_nasc.dia_mes_ano()}")
    print(f"RA: {info["Ra"]}-{info["DigRa"].strip()} {info["UfRa"]}")

    print(f"Mãe: {info["NomeMae"].title()}")
    print(f"Pai: {info["NomePai"].title()}")

    print(f"Endereço: {info["Logradouro"].title()}, {info["Numero"]} ({info["Bairro"].title()}, {info["Cidade"].title()}, {info["Uf"]}) (CEP: {info["Cep"]})")
    print(f"CPF: {info["Cpf"]}")
