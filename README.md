# Alunalyzr
Alunalyzr é uma ferramenta que acessa automaticamente a plataforma Sala do Futuro, coleta os dados do aluno e os transforma em informações claras e úteis sobre o desempenho escolar.

# Módulos
Esse programa é dividido em módulos. Cada módulo coleta diferentes dados da Sala do Futuro. Veja mais detalhes no final desse documento

> ***Nota!*** Esse readme não contém imagens do Alunalyzr para proteger minha privacidade, já que muitos dos reportes contém dados sensíveis.

# Como utilizar
A primeira coisa que deve fazer é instalar o python na sua máquina. Após isso, clone esse repositório:

```
git clone "https://github.com/rodrigolitzius/Alunalyzr"
```

entre na pasta do projeto:

```
cd Alunalyzr
```

instale as dependências do projeto:

```
pip install -r requirements.txt
```

## usuarios.json
Este programa acessa a Sala do Futuro fazendo login em uma conta de um aluno e coletando dados pessoas, mas para isso, o programa precisa saber as credenciais do aluno. 

Logo, é necessário um arquivo chamado usuarios.json que armazena essas informações. Crie o arquivo na pasta do projeto, depois preencha-o desta forma:

```
"Nome": ["Login (RA+Dígito+UF)", "Senha"]
```
> ***Nome*** pode ser qualquer texto, não necessariamente o nome do aluno, porém evite espaços.

substitua o texto abaixo pela suas credencias (Ou a de uma amigo) e cole no arquivo. Segue um exemplo:

```
{
    "Joaquim": ["00001234567891sp", "Senha321"]
}
```
> ***Dica:*** Você pode adicionar quantos alunos você quiser nessa lista!

Com isso feito, podemos executar o programa!

## Executando
ainda na pasta onde você clonou o repositório, digite este comando:

```
python ./src/main.py <nome> <módulo> <opções>
```

| Valor | significado |
| -- | -- |
| nome | Esse é o nome que você escreveu no usuarios.js |
| modulo | Esse é o nome módulo que deseja utilizar. Veja a lista de módulos abaixo |
| opções | Alguns módulos requerem argumentos adicionais. é aqui onde você deve colocá-las |

### Lista de módulos
Atualmente existem esses módulos

#### ***boletim***
Exibe o boletim do ano especificado 
(Pelos meus testes, boletins anteriores a 2024 estão indisponíveis)

#### ***info***
Exibe informações confidenciais do aluno. 

***CUIDADO AO UTILIZAR***

#### ***bimestres***
Exibe os bimestres com data de início e término. A API da sala do futuro é terrível, então é possível que a lista de bimestres apareça repetida. Só ignore isso, não é culpa minha kkkk

#### ***disciplinas***
Exibe as disciplinas que o aluno tem na grada curricular. Novamente, a API é estranha, e o nome de algumas disciplinas pode estar incompleto

#### ***tarefasp***
Esse módulo está em desenvolvimento ainda, mas atualmente ele coleta os nomes das tarefas completas, pendentes e expiradas. algum dia ess módulo voltará a sua former glory!
