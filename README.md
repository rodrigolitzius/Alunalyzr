# Alunalyzr
Alunalyzr é uma ferramenta que acessa automaticamente a plataforma Sala do Futuro, coleta os dados do aluno e os transforma em informações claras e úteis sobre o desempenho escolar.

# Módulos
Esse programa é dividido em módulos. Cada módulo coleta diferentes dados da Sala do Futuro. Por enquanto existem apenas 2 módulos. Veja mais detalhes abaixo:

> ***Nota!*** Esse readme não contém imagens do Alunalyzr para proteger minha privacidade, já que muitos dos reportes contém dados sensíveis.

## Tarefa SP
Esse módulo coleta informações sobre as tarefas do TarefaSP, como:

### Tarefas completas
Exibe todas as tarefas que vocẽ completou, e inclui informações como a sua nota (de 0 à 10) e o tempo que você levou para conclui-la.

Algumas tarefas possuem seções que separam as questões. Por exemplo, a prova paulista contém questões de várias disciplinas, e as separa por seções. Este módulo é capaz de calcular as notas de cada uma dessas seções individualmente

### Tarefas Incompletas
Exibe todas as tarefas incompletas e o tempo restante que você tem pra concluí-las

### Tarefas expiradas
Exibe a porcentagem de tarefas que vocẽ perdeu

### Média das matérias
Separa todas as tarefas por disciplina, e exibe a média de notas para todas as disciplinas (Muito difícil explicar)

> (As matérias que estiverem na cor branca não têm nenhuma tarefa)

As médias não incluem seções de tarefas por que eu não achei nenhuma forma de relacionar uma seção a uma matéria. Acho que nem é possível :(

## Boletim
> ***Atenção!*** Esse módulo ainda está em desenvolvimento e já existem bugs confirmados.

Mostra as suas notas e frequências para cada bimestre/fechamento de notas

# Como utilizar
A primeira coisa que deve fazer é instalar o python na sua máquina. Quando fizer isso, instale a biblioteca requests (Utilizada para se comunicar com a Sala do Futuro)

Instale o requests utilizando o pip

```
pip install requests
```

Após isso, clone esse repositório:

```
git clone "https://github.com/rodrigolitzius/Alunalyzr"
```

## auths.json
Este programa acessa a Sala do Futuro fazendo login em uma conta de um aluno e coletando dados pessoas, mas para isso, o programa precisa saber as credenciais do aluno. 

Logo, existe um arquivo chamado auths.json que armazena essas informações. Você deve escrevê-lo dessa forma:

```
"Nome": ["Login (RA+Dígito+UF)", "Senha"]
```
> ***Nome*** pode ser qualquer texto, não necessariamente o nome do aluno, porém evite espaços.

substitua o texto abaixo pela suas credencias (Ou a de uma amigo) e cole no arquivo

```
{
    "Joaquim": ["00001234567891sp", "Senha321"]
}
```
> ***Dica:*** Você pode adicionar quantos alunos você quiser nessa lista!

Com isso feito, podemos executar o programa!

## Executando
entre a pasta onde você clonou o repositório e digite o comando do módulo em que você quer ver.

| Valor | significado |
| -- | -- |
| nome | Esse é o nome que você escreveu no auths.js |

### Módulo TarefaSP

```
python ./main.py <nome> tarefas -e <opções>
```

| Valor | significado |
| -- | -- |
| opções | aqui você pode escolher exibir qualquer uma dessas categorias: ***completas, incompletas, expiradas, provas, media.*** Você também pode especificar multiplas categorias. Por exemplo: ***provas,media*** irá exibir suas provas e médias, e ***completas,provas,media*** exibirá tarefas completas, provas e suas médias. |

### Módulo Boletim
```
python ./main.py <nome> boletim <ano>
```

| Valor | significado |
| -- | -- |
| ano | Qual o ano do boletim que deseja ver. Pelos meus testes boletins de anos anteriores à 2024 não estão disponíveis na plataforma. |