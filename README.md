# AP4 — Serviço Remoto com gRPC

Projeto desenvolvido para a **Atividade Prática 4 da disciplina de Sistemas Distribuídos**.

A atividade implementa um serviço remoto utilizando **gRPC + Protocol Buffers**, com cliente e servidor desenvolvidos em Python.

---

# 1. Objetivo

O objetivo da atividade é desenvolver e demonstrar um serviço remoto utilizando gRPC, contemplando:

* definição de contrato utilizando `.proto`;
* geração automática dos códigos do gRPC;
* implementação de cliente e servidor em Python;
* três operações RPC;
* validação de dados;
* tratamento de erros utilizando códigos de status gRPC;
* utilização de deadlines/timeouts;
* tratamento de servidor indisponível;
* execução de chamadas concorrentes;
* evolução compatível do contrato `.proto`;
* comparação entre gRPC, REST e MQTT.

O projeto foi desenvolvido de forma simples e reproduzível, utilizando Python e podendo ser executado em computadores Windows, inclusive nos computadores do laboratório da faculdade.

---

# 2. Tecnologias utilizadas

* Python 3.13
* gRPC
* Protocol Buffers (Protobuf)
* `grpcio`
* `grpcio-tools`
* PowerShell
* Visual Studio Code

---

# 3. Estrutura do projeto

```text
AP4-gRPC-Felipe/
│
├── processador.proto
├── processador_pb2.py
├── processador_pb2_grpc.py
├── servidor.py
├── cliente.py
├── testes.py
├── gerar_stubs.bat
├── requirements.txt
├── .gitignore
├── README.md
│
└── evolucao/
    ├── v1/
    │   └── processador_v1.proto
    └── v2/
        └── processador_v2.proto
```

### Descrição dos principais arquivos

| Arquivo                   | Função                                     |
| ------------------------- | ------------------------------------------ |
| `processador.proto`       | Define o contrato do serviço gRPC          |
| `processador_pb2.py`      | Código gerado para as mensagens Protobuf   |
| `processador_pb2_grpc.py` | Código gerado para cliente e servidor gRPC |
| `servidor.py`             | Implementação do servidor                  |
| `cliente.py`              | Cliente que realiza as chamadas RPC        |
| `testes.py`               | Teste de chamadas concorrentes             |
| `gerar_stubs.bat`         | Automatiza a geração dos arquivos gRPC     |
| `requirements.txt`        | Lista as dependências Python               |
| `evolucao/v1`             | Primeira versão do contrato                |
| `evolucao/v2`             | Segunda versão do contrato                 |
| `README.md`               | Documentação do projeto                    |

Os arquivos `processador_pb2.py` e `processador_pb2_grpc.py` são **gerados automaticamente** a partir do arquivo `.proto` e não devem ser editados manualmente.

---

# 4. Pré-requisitos

Para executar o projeto é necessário ter:

1. Python instalado;
2. Visual Studio Code ou outro editor;
3. PowerShell ou terminal;
4. acesso à pasta do projeto.

Para verificar a instalação do Python:

```powershell
python --version
```

Exemplo utilizado durante o desenvolvimento:

```text
Python 3.13.11
```

---

# 5. Criando o ambiente virtual

Dentro da pasta do projeto:

```powershell
python -m venv .venv
```

Isso cria o ambiente virtual:

```text
.venv/
```

## Ativação opcional

No PowerShell, a ativação pode ser feita com:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução de scripts, pode ser utilizada temporariamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando ativado, o terminal apresenta algo semelhante a:

```text
(.venv) PS D:\...\AP4-gRPC-Felipe>
```

## Forma recomendada neste projeto

A ativação do ambiente virtual **não é obrigatória**.

Para evitar problemas de política de execução do PowerShell, os programas podem ser executados diretamente utilizando o Python existente dentro do `.venv`:

```powershell
.\.venv\Scripts\python.exe servidor.py
```

```powershell
.\.venv\Scripts\python.exe cliente.py
```

```powershell
.\.venv\Scripts\python.exe testes.py
```

Essa foi a forma utilizada com sucesso durante os testes do projeto.

---

# 6. Instalação das dependências

Com o ambiente virtual criado, instalar as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

Depois:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O arquivo `requirements.txt` contém:

```text
grpcio
grpcio-tools
```

Também é possível instalar diretamente:

```powershell
.\.venv\Scripts\python.exe -m pip install grpcio grpcio-tools
```

---

# 7. Definição do contrato com Protocol Buffers

O contrato principal do projeto está em:

```text
processador.proto
```

O arquivo `.proto` define:

* o serviço;
* os métodos RPC;
* as mensagens utilizadas;
* os tipos dos dados;
* os campos das mensagens.

A ideia é que cliente e servidor compartilhem um contrato bem definido.

A estrutura geral pode ser representada por:

```text
             processador.proto
                    |
                    v
              protoc / grpcio
                    |
          +---------+---------+
          |                   |
          v                   v
 processador_pb2.py   processador_pb2_grpc.py
          |                   |
          +---------+---------+
                    |
              Cliente/Servidor
```

---

# 8. Gerando os arquivos do gRPC

Os arquivos Python podem ser gerados utilizando:

```powershell
.\.venv\Scripts\python.exe -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

Após a execução devem existir:

```text
processador_pb2.py
processador_pb2_grpc.py
```

Também existe o arquivo:

```text
gerar_stubs.bat
```

No PowerShell, ele pode ser executado com:

```powershell
.\gerar_stubs.bat
```

Os arquivos gerados não precisam ser escritos manualmente.

O `.proto` é a fonte do contrato e o `protoc` gera os códigos necessários.

---

# 9. Como funciona a comunicação

A comunicação do projeto pode ser representada da seguinte forma:

```text
+----------------+
|    CLIENTE     |
+----------------+
        |
        | chamada RPC
        v
+----------------+
|      gRPC      |
+----------------+
        |
        | Protobuf
        v
+----------------+
|    SERVIDOR    |
+----------------+
        |
        +--------------------------+
        |            |             |
        v            v             v
 Registrar       Consultar      Calcular
 Veículo         Veículo         Média
```

O cliente não executa diretamente as funções do servidor.

Ele utiliza um **stub**, gerado automaticamente a partir do contrato `.proto`.

---

# 10. Operações RPC implementadas

O serviço possui três operações principais.

## 10.1 RegistrarVeiculo

Responsável por cadastrar um veículo no servidor.

São utilizados dados como:

```text
Placa
Modelo
Setor
Velocidade
```

Exemplo:

```text
Placa: ABC1D23
Modelo: Volvo FH
Setor: Transporte
Velocidade: 65.5 km/h
```

Quando o cadastro é realizado corretamente, o servidor retorna uma resposta de sucesso.

---

## 10.2 ConsultarVeiculo

Recebe uma placa e procura o veículo cadastrado.

Quando o veículo existe:

```text
Veículo encontrado
```

Quando não existe:

```text
NOT_FOUND
```

---

## 10.3 CalcularMediaVelocidade

Recebe uma lista de velocidades e calcula a média.

Exemplo:

```text
10
20
30
```

Resultado:

```text
20 km/h
```

O método também possui o campo:

```text
delay_ms
```

Esse campo permite simular um processamento demorado para demonstrar o funcionamento de deadlines.

---

# 11. Tratamento de erros gRPC

O projeto utiliza diferentes códigos de status gRPC.

## 11.1 INVALID_ARGUMENT

É utilizado quando os dados enviados pelo cliente são inválidos.

Exemplos:

* placa vazia;
* velocidade negativa;
* lista de velocidades vazia;
* setor vazio.

Exemplo de resultado:

```text
StatusCode.INVALID_ARGUMENT
```

---

## 11.2 ALREADY_EXISTS

É utilizado quando o cliente tenta cadastrar um veículo cuja placa já está cadastrada.

Exemplo:

```text
StatusCode.ALREADY_EXISTS
```

---

## 11.3 NOT_FOUND

É utilizado quando o cliente tenta consultar uma placa que não existe.

Exemplo:

```text
StatusCode.NOT_FOUND
```

---

## 11.4 DEADLINE_EXCEEDED

É utilizado quando uma chamada demora mais do que o tempo máximo definido pelo cliente.

Exemplo:

```text
StatusCode.DEADLINE_EXCEEDED
```

---

## 11.5 UNAVAILABLE

Representa uma situação em que o serviço não está disponível para atender a chamada.

Por exemplo, quando o cliente tenta acessar o servidor enquanto o servidor está desligado.

Exemplo:

```text
StatusCode.UNAVAILABLE
```

Esse erro é diferente de `INVALID_ARGUMENT`.

No `INVALID_ARGUMENT`, o serviço está disponível, mas os dados ou argumentos enviados não são válidos.

No `UNAVAILABLE`, o cliente não consegue utilizar o serviço.

---

# 12. Executando o servidor

Abra um terminal na pasta do projeto.

Execute:

```powershell
.\.venv\Scripts\python.exe servidor.py
```

O resultado esperado é semelhante a:

```text
============================================================
SERVIDOR gRPC - AP4
============================================================
Servidor iniciado em localhost:50051
Aguardando chamadas...
Pressione Ctrl+C para encerrar.
```

Não feche esse terminal enquanto estiver realizando os testes.

O servidor utiliza a porta:

```text
50051
```

---

# 13. Executando o cliente

Com o servidor funcionando, abra um segundo terminal.

Execute:

```powershell
.\.venv\Scripts\python.exe cliente.py
```

O cliente realiza as principais demonstrações do serviço.

Durante os testes realizados, foram obtidos os seguintes resultados:

```text
[1] Cadastrando veículo...
  veículo cadastrado com sucesso

[2] Consultando veículo...
  veículo encontrado

[3] Testando argumento inválido...
  status: StatusCode.INVALID_ARGUMENT

[4] Consultando veículo inexistente...
  status: StatusCode.NOT_FOUND

[5] Tentando cadastrar a mesma placa novamente...
  status: StatusCode.ALREADY_EXISTS

[6] Testando deadline...
  status: StatusCode.DEADLINE_EXCEEDED

[7] Calculando média sem atraso...
  Média: 55.00 km/h
  Quantidade: 4
```

Isso demonstra o funcionamento das principais operações e mecanismos de tratamento de erro do serviço.

---

# 14. Experimento de deadline

O método `CalcularMediaVelocidade` possui um parâmetro:

```text
delay_ms
```

Ele permite simular uma operação demorada no servidor.

Por exemplo:

```text
delay_ms = 2000
```

significa aproximadamente:

```text
2 segundos
```

No cliente foi utilizado um timeout de:

```python
timeout=0.5
```

Ou seja:

```text
Servidor:
    demora aproximadamente 2 segundos

Cliente:
    aceita esperar 0,5 segundo
```

Como o servidor demora mais do que o limite estabelecido pelo cliente, a chamada termina com:

```text
StatusCode.DEADLINE_EXCEEDED
```

Esse experimento demonstra que uma chamada remota depende não apenas da execução do método, mas também do tempo de comunicação e processamento.

---

# 15. Experimento de servidor indisponível

Para demonstrar `UNAVAILABLE`:

### 1. Inicie o servidor

```powershell
.\.venv\Scripts\python.exe servidor.py
```

### 2. Deixe o servidor funcionando.

### 3. Pare o servidor com:

```text
Ctrl + C
```

### 4. Execute o cliente:

```powershell
.\.venv\Scripts\python.exe cliente.py
```

Como o servidor não está mais disponível na porta `50051`, as chamadas que tentarem acessar o serviço poderão retornar:

```text
StatusCode.UNAVAILABLE
```

Esse teste demonstra a diferença entre uma falha relacionada aos argumentos da chamada e uma falha de disponibilidade do serviço.

---

# 16. Experimento de concorrência

O arquivo:

```text
testes.py
```

foi criado especificamente para demonstrar chamadas concorrentes.

Ele utiliza:

```python
ThreadPoolExecutor
```

para realizar várias chamadas gRPC simultaneamente.

A ideia é simular vários clientes ou requisições acessando o mesmo serviço ao mesmo tempo.

## Executando

Com o servidor funcionando:

```powershell
.\.venv\Scripts\python.exe testes.py
```

## Resultado obtido

Durante o teste foram realizadas **10 chamadas concorrentes**, identificadas de:

```text
Chamada 0
até
Chamada 9
```

Todas retornaram:

```text
OK
```

O resultado obtido foi aproximadamente:

```text
Chamada 2: OK - média=12.00 - tempo=0.522s
Chamada 3: OK - média=13.00 - tempo=0.521s
Chamada 1: OK - média=11.00 - tempo=0.523s
Chamada 5: OK - média=15.00 - tempo=0.521s
Chamada 0: OK - média=10.00 - tempo=0.523s
Chamada 8: OK - média=18.00 - tempo=0.520s
Chamada 6: OK - média=16.00 - tempo=0.521s
Chamada 4: OK - média=14.00 - tempo=0.522s
Chamada 9: OK - média=19.00 - tempo=0.520s
Chamada 7: OK - média=17.00 - tempo=0.521s
```

Tempo total aproximado:

```text
0.529 segundos
```

Resultado:

```text
As chamadas foram executadas concorrentemente.
```

O resultado demonstra que as chamadas foram processadas de maneira concorrente, em vez de serem executadas uma após a outra.

---

# 17. ThreadPoolExecutor do servidor

O servidor utiliza um executor com múltiplos trabalhadores:

```python
ThreadPoolExecutor(max_workers=10)
```

Isso permite que o servidor processe diferentes chamadas utilizando múltiplas threads.

No experimento foram realizadas 10 chamadas concorrentes, permitindo observar o comportamento do serviço sob múltiplas requisições simultâneas.

---

# 18. Evolução do contrato `.proto`

O projeto também apresenta uma evolução do contrato utilizando duas versões:

```text
evolucao/
├── v1/
│   └── processador_v1.proto
│
└── v2/
    └── processador_v2.proto
```

A ideia é demonstrar como um contrato Protobuf pode evoluir mantendo compatibilidade com os campos existentes.

Na evolução proposta, a V2 adiciona um novo campo:

```protobuf
string observacao = 5;
```

O número `5` deve ser um número de campo que não era utilizado anteriormente.

---

# 19. Compatibilidade do Protocol Buffers

Uma regra importante do Protocol Buffers é não reutilizar números de campos que já foram utilizados.

Por exemplo, se a V1 possui:

```protobuf
string placa = 1;
string modelo = 2;
float velocidade = 3;
string setor = 4;
```

a V2 pode adicionar:

```protobuf
string observacao = 5;
```

Isso preserva os números dos campos antigos.

A ideia é:

```text
V1

placa       = 1
modelo      = 2
velocidade  = 3
setor       = 4


V2

placa       = 1
modelo      = 2
velocidade  = 3
setor       = 4
observacao  = 5
```

O campo novo recebe um número que ainda não era utilizado.

---

# 20. Por que não reutilizar números de campos?

Os números dos campos fazem parte da representação binária das mensagens Protobuf.

Por isso, remover um campo e posteriormente utilizar o mesmo número para representar outra informação pode gerar problemas de compatibilidade.

A regra geral é:

* não reutilizar números de campos antigos;
* manter os campos existentes;
* adicionar novos campos utilizando novos números;
* planejar mudanças incompatíveis utilizando versionamento ou migração.

---

# 21. Comparação com AP2 e AP3

O projeto também permite relacionar os conceitos estudados nas atividades anteriores.

## 21.1 gRPC — AP4

No AP4 o contrato é definido pelo:

```text
processador.proto
```

O cliente utiliza um stub gerado automaticamente e as mensagens são serializadas utilizando Protocol Buffers.

Principais características:

* chamadas RPC;
* contrato definido;
* geração automática de código;
* Protocol Buffers;
* deadlines;
* códigos de status;
* possibilidade de comunicação concorrente e streaming.

---

## 21.2 REST — AP2

Na API REST trabalhada anteriormente, a comunicação utiliza HTTP.

Exemplos de operações:

```text
POST /eventos
GET /eventos
```

Os dados normalmente são representados utilizando JSON.

A comunicação ocorre através do modelo de requisição e resposta HTTP.

---

## 21.3 MQTT — AP3

No MQTT a comunicação utiliza o modelo:

```text
Publisher
     |
     v
   Broker
     |
     v
Subscriber
```

O produtor publica mensagens em tópicos e os consumidores interessados recebem essas mensagens.

Exemplo utilizado na AP3:

```text
laboratorio/sensor1/telemetria
```

---

# 22. Comparação resumida

| Característica                    | gRPC                      | REST                                      | MQTT                   |
| --------------------------------- | ------------------------- | ----------------------------------------- | ---------------------- |
| Modelo                            | RPC                       | Requisição/Resposta HTTP                  | Pub/Sub                |
| Contrato                          | `.proto`                  | API/JSON ou outro formato                 | Tópicos e payload      |
| Comunicação                       | Chamada de método remoto  | Requisição HTTP                           | Publicação/assinatura  |
| Serialização utilizada no projeto | Protobuf                  | JSON                                      | Payload da mensagem    |
| Streaming                         | Suportado                 | Pode ser implementado conforme tecnologia | Fluxo de mensagens     |
| Deadline                          | Recurso direto do gRPC    | Depende da implementação                  | Não é o foco principal |
| Broker obrigatório                | Não                       | Não                                       | Sim                    |
| Geração de código                 | Sim, a partir do `.proto` | Depende da ferramenta                     | Depende da aplicação   |

---

# 23. Por que uma chamada remota não deve ser tratada como uma função local?

Uma função local normalmente depende do próprio processo e possui comunicação muito mais previsível.

Uma chamada remota depende de:

* rede;
* outro processo;
* servidor;
* serialização;
* transporte;
* tempo de resposta.

Por isso, uma chamada remota pode sofrer:

* latência;
* perda de conexão;
* indisponibilidade;
* timeout;
* erros de comunicação;
* falhas no servidor.

O programa precisa considerar essas possibilidades.

---

# 24. Diferença entre erro de aplicação e indisponibilidade

Um erro de aplicação pode acontecer quando o servidor está funcionando, mas os dados enviados não são válidos para aquela operação.

Exemplo:

```text
INVALID_ARGUMENT
```

Já:

```text
UNAVAILABLE
```

está relacionado à indisponibilidade do serviço ou à impossibilidade de utilizar o serviço naquele momento.

Portanto:

```text
INVALID_ARGUMENT
    ↓
Serviço disponível
Dados/argumentos inválidos


UNAVAILABLE
    ↓
Serviço indisponível
ou não acessível
```

---

# 25. O que significa contrato forte?

O contrato forte significa que cliente e servidor possuem uma definição estruturada das mensagens e operações.

No projeto, esse contrato é definido pelo:

```text
processador.proto
```

Isso aumenta o acoplamento ao contrato, mas também oferece vantagens:

* estrutura definida;
* tipos definidos;
* métodos conhecidos;
* geração automática de código;
* menor ambiguidade entre cliente e servidor.

Por outro lado, mudanças no contrato precisam ser planejadas.

---

# 26. Retry e operações duplicadas

Uma chamada remota pode sofrer timeout mesmo que o servidor tenha recebido ou executado a operação.

Por isso, simplesmente repetir uma operação pode causar duplicidade.

Por exemplo:

```text
Cliente
   |
   | Registrar veículo
   v
Servidor
   |
   | executa
   |
   X resposta perdida
   |
Cliente recebe timeout
```

O cliente pode interpretar que a operação falhou, mesmo que o servidor tenha executado a operação.

Para operações que alteram dados, uma estratégia possível é utilizar uma identificação única da operação, como uma **idempotency key**, permitindo que o servidor reconheça uma repetição.

---

# 27. Mudanças incompatíveis no `.proto`

Uma mudança pode ser incompatível quando altera de maneira inadequada um campo que já é utilizado pelos clientes.

Um exemplo perigoso é reutilizar o número de um campo removido para representar outra informação.

Por isso:

```text
Campo antigo
     ↓
Número preservado
     ↓
Novo campo
     ↓
Novo número
```

Quando uma alteração incompatível é necessária, pode ser necessário utilizar versionamento ou uma migração coordenada entre cliente e servidor.

---

# 28. Roteiro para apresentação

## Parte 1 — Introdução

Pode ser explicado:

> "Minha atividade implementa um serviço remoto utilizando gRPC. Eu escolhi trabalhar com um pequeno serviço de gerenciamento de veículos porque ele permite demonstrar cadastro, consulta, validação, tratamento de erros, deadline e concorrência."

---

## Parte 2 — Mostrar o `.proto`

Abra:

```text
processador.proto
```

Mostre:

```protobuf
service Processador
```

Depois apresente os três métodos:

```protobuf
rpc RegistrarVeiculo
rpc ConsultarVeiculo
rpc CalcularMediaVelocidade
```

Explique:

> "Eu comecei pelo contrato, definindo os métodos e as mensagens que serão utilizadas pelo cliente e pelo servidor."

---

## Parte 3 — Mostrar a geração dos stubs

Mostre:

```powershell
.\.venv\Scripts\python.exe -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

Explique:

> "Esse comando utiliza o arquivo `.proto` para gerar automaticamente os arquivos Python necessários para a comunicação gRPC."

Mostre:

```text
processador_pb2.py
processador_pb2_grpc.py
```

---

## Parte 4 — Mostrar o servidor

Abra:

```text
servidor.py
```

Mostre:

```python
class Processador(pb2_grpc.ProcessadorServicer):
```

Explique:

> "Essa classe implementa o serviço definido no arquivo `.proto`."

Depois mostre os três métodos RPC.

---

## Parte 5 — Mostrar o cliente

Abra:

```text
cliente.py
```

Mostre:

```python
stub = pb2_grpc.ProcessadorStub(channel)
```

Explique:

> "O stub é o código gerado que permite ao cliente chamar os métodos do serviço remoto."

---

## Parte 6 — Demonstrar os erros

Mostre:

```text
INVALID_ARGUMENT
NOT_FOUND
ALREADY_EXISTS
```

Explique a diferença entre eles.

Por exemplo:

> "`INVALID_ARGUMENT` ocorre quando os dados enviados são inválidos. `NOT_FOUND` ocorre quando o veículo solicitado não existe. `ALREADY_EXISTS` ocorre quando tento cadastrar uma placa que já está cadastrada."

---

## Parte 7 — Demonstrar deadline

Mostre:

```python
timeout=0.5
```

Explique:

> "Aqui existe um limite de tempo para a chamada. Como o servidor foi configurado para simular um atraso maior do que esse limite, o cliente recebe `DEADLINE_EXCEEDED`."

---

## Parte 8 — Demonstrar servidor indisponível

Pare o servidor:

```text
Ctrl + C
```

Execute o cliente:

```powershell
.\.venv\Scripts\python.exe cliente.py
```

Explique:

> "Agora o problema é diferente. O serviço não está disponível para receber a chamada, então podemos obter `UNAVAILABLE`."

---

## Parte 9 — Demonstrar concorrência

Inicie novamente o servidor:

```powershell
.\.venv\Scripts\python.exe servidor.py
```

Em outro terminal:

```powershell
.\.venv\Scripts\python.exe testes.py
```

Explique:

> "Aqui eu realizo dez chamadas simultaneamente utilizando `ThreadPoolExecutor`. O objetivo é demonstrar que o servidor consegue lidar com múltiplas chamadas concorrentes."

---

## Parte 10 — Demonstrar evolução do contrato

Abra:

```text
evolucao/v1/processador_v1.proto
```

Depois:

```text
evolucao/v2/processador_v2.proto
```

Mostre o campo adicional da V2, caso presente:

```protobuf
string observacao = 5;
```

Explique:

> "A evolução adiciona um novo campo utilizando um número que não era utilizado anteriormente, mantendo os números dos campos existentes."

---

# 29. Perguntas que o professor pode fazer

## O que é gRPC?

Resposta:

> "gRPC é um framework de chamada de procedimento remoto. O cliente chama métodos definidos em um contrato e o gRPC realiza a comunicação entre cliente e servidor."

---

## O que é Protocol Buffers?

Resposta:

> "Protocol Buffers, ou Protobuf, é utilizado para definir as mensagens e o contrato do serviço. A partir do arquivo `.proto`, são gerados os códigos necessários para cliente e servidor."

---

## O que é um stub?

Resposta:

> "É o código gerado que permite ao cliente chamar os métodos do serviço remoto através de uma interface local."

---

## O que é deadline?

Resposta:

> "É o limite de tempo que o cliente aceita esperar por uma chamada remota."

---

## Por que utilizar deadline?

Resposta:

> "Porque uma chamada remota pode ficar aguardando devido a problemas de rede, servidor ou processamento. O deadline impede que o cliente fique esperando indefinidamente."

---

## Qual a diferença entre `INVALID_ARGUMENT` e `UNAVAILABLE`?

Resposta:

> "`INVALID_ARGUMENT` indica que os argumentos enviados para a operação são inválidos. `UNAVAILABLE` indica que o serviço não está disponível ou não pode ser utilizado naquele momento."

---

## Por que utilizar `.proto`?

Resposta:

> "Para definir um contrato explícito entre cliente e servidor, incluindo os métodos RPC, mensagens e tipos de dados, além de permitir a geração automática dos códigos."

---

## Por que utilizar gRPC em vez de REST?

Resposta:

> "As duas tecnologias podem ser utilizadas para comunicação entre sistemas, mas possuem modelos diferentes. Nesta atividade, o gRPC foi utilizado porque permite demonstrar diretamente chamadas RPC, contrato com Protobuf, stubs, deadlines e códigos de status gRPC."

---

## O que acontece se o servidor estiver desligado?

Resposta:

> "O cliente não consegue utilizar o serviço remoto e pode receber o status `UNAVAILABLE`."

---

## Por que as chamadas concorrentes são importantes?

Resposta:

> "Porque sistemas distribuídos normalmente precisam atender múltiplas requisições ao mesmo tempo. O teste demonstra o comportamento do servidor quando várias chamadas são realizadas simultaneamente."

---

# 30. Checklist final

Antes de entregar o projeto, verificar:

* [x] `processador.proto` presente;
* [x] `servidor.py` presente;
* [x] `cliente.py` presente;
* [x] `testes.py` presente;
* [x] `requirements.txt` presente;
* [x] `gerar_stubs.bat` presente;
* [x] `README.md` presente;
* [x] stubs gerados;
* [x] cliente utiliza deadline;
* [x] `INVALID_ARGUMENT` implementado;
* [x] `NOT_FOUND` implementado;
* [x] `ALREADY_EXISTS` implementado;
* [x] `DEADLINE_EXCEEDED` demonstrado;
* [x] teste concorrente implementado;
* [x] 10 chamadas concorrentes executadas com sucesso;
* [x] evolução V1/V2 documentada;
* [x] comparação com REST documentada;
* [x] comparação com MQTT documentada.

### Teste de concorrência realizado

Resultado obtido:

```text
10 chamadas concorrentes
10 chamadas retornando OK
Tempo total aproximado: 0.529s
```

---

# 31. Comandos rápidos para a apresentação

## Terminal 1 — servidor

```powershell
.\.venv\Scripts\python.exe servidor.py
```

Resultado esperado:

```text
Servidor iniciado em localhost:50051
Aguardando chamadas...
```

---

## Terminal 2 — cliente

```powershell
.\.venv\Scripts\python.exe cliente.py
```

---

## Terminal 3 — teste concorrente

```powershell
.\.venv\Scripts\python.exe testes.py
```

---

## Regenerar os stubs

```powershell
.\.venv\Scripts\python.exe -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

---

# 32. Reprodução completa do projeto

Para executar o projeto do zero:

### 1. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 2. Instalar as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Gerar os stubs

```powershell
.\.venv\Scripts\python.exe -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

### 4. Iniciar o servidor

```powershell
.\.venv\Scripts\python.exe servidor.py
```

### 5. Em outro terminal, executar o cliente

```powershell
.\.venv\Scripts\python.exe cliente.py
```

### 6. Executar o teste de concorrência

Com o servidor ainda funcionando:

```powershell
.\.venv\Scripts\python.exe testes.py
```

---

# 33. Conclusão

A AP4 implementa um serviço remoto utilizando gRPC e Protocol Buffers, permitindo demonstrar na prática conceitos fundamentais de sistemas distribuídos.

O projeto apresenta:

* contrato formal utilizando `.proto`;
* geração automática de código;
* comunicação entre cliente e servidor;
* operações RPC;
* validação de dados;
* códigos de erro;
* deadlines;
* tratamento de indisponibilidade;
* chamadas concorrentes;
* evolução do contrato;
* comparação com outras tecnologias estudadas na disciplina.

A implementação também permite observar uma característica importante dos sistemas distribuídos: uma chamada remota possui dependências que não existem da mesma maneira em uma chamada local, como rede, disponibilidade, latência, timeout e falhas de comunicação.

O projeto foi estruturado de forma que o ambiente possa ser reproduzido a partir do arquivo `.proto`, das dependências e dos códigos-fonte.

O fluxo principal é:

```text
processador.proto
       |
       v
   protoc/gRPC
       |
       v
código gerado
       |
       +----------------+
       |                |
       v                v
    CLIENTE         SERVIDOR
       |                |
       +------ gRPC ----+
              |
              v
        Serviço remoto
```

---

# 34. Observação sobre os arquivos gerados

Os arquivos:

```text
processador_pb2.py
processador_pb2_grpc.py
```

podem ser removidos e gerados novamente utilizando:

```powershell
.\.venv\Scripts\python.exe -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

Isso demonstra que eles são artefatos gerados automaticamente.

A principal fonte do contrato é:

```text
processador.proto
```

Portanto:

```text
.proto
   ↓
protoc
   ↓
processador_pb2.py
processador_pb2_grpc.py
   ↓
cliente + servidor
```

Essa estrutura torna o projeto mais organizado e reproduzível.
