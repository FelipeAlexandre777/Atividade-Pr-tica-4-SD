# AP4 — Serviço remoto com gRPC

Projeto desenvolvido para a Atividade Prática 4 de Sistemas Distribuídos.

## 1. Objetivo

Implementar um serviço remoto usando **gRPC + Protocol Buffers**, demonstrando:

- contrato definido em `.proto`;
- geração automática dos stubs;
- cliente e servidor em Python;
- três operações RPC;
- validação de dados;
- erros com status gRPC;
- deadlines/timeouts;
- servidor indisponível;
- chamadas concorrentes;
- evolução compatível do contrato;
- comparação com REST e MQTT.

A ideia foi manter o projeto simples de executar no Windows, inclusive nos computadores do laboratório da faculdade.

---

# 2. Estrutura do projeto

```text
AP4-gRPC-Felipe/
│
├── processador.proto
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

Os arquivos `processador_pb2.py` e `processador_pb2_grpc.py` são gerados automaticamente pelo `protoc`.

---

# 3. Pré-requisitos

No Windows:

1. Instalar Python.
2. Instalar o VS Code.
3. Abrir a pasta do projeto no VS Code.
4. Ter acesso ao PowerShell ou terminal do VS Code.

Para conferir o Python:

```powershell
python --version
```

Exemplo:

```text
Python 3.13.x
```

Se o comando `python` não funcionar, verifique a instalação do Python e a opção de adicionar o Python ao PATH.

---

# 4. Criar o ambiente virtual

No terminal do VS Code:

```powershell
python -m venv .venv
```

Ativar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal ficará parecido com:

```text
(.venv) PS C:\...\AP4-gRPC-Felipe>
```

---

# 5. Instalar as bibliotecas

Com o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Ou, se preferir instalar diretamente:

```powershell
python -m pip install grpcio grpcio-tools
```

---

# 6. Gerar os arquivos do gRPC

O arquivo principal do contrato é:

```text
processador.proto
```

Para gerar os arquivos Python:

```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

Também existe o arquivo:

```text
gerar_stubs.bat
```

No Windows, basta executar:

```powershell
.\gerar_stubs.bat
```

Depois devem aparecer:

```text
processador_pb2.py
processador_pb2_grpc.py
```

Esses arquivos não são escritos manualmente. Eles são gerados a partir do `.proto`.

---

# 7. Como o projeto funciona

A comunicação é:

```text
CLIENTE
   |
   | chamada RPC
   v
gRPC
   |
   | Protocol Buffers
   v
SERVIDOR
   |
   +--> RegistrarVeiculo()
   |
   +--> ConsultarVeiculo()
   |
   +--> CalcularMediaVelocidade()
```

O cliente não chama diretamente uma função do servidor.

Ele chama um **stub**, que representa o serviço remoto.

---

# 8. Métodos RPC implementados

## RegistrarVeiculo

Recebe os dados de um veículo e registra no servidor.

Exemplo:

```text
Placa: ABC1D23
Modelo: Volvo FH
Setor: Transporte
Velocidade: 65.5 km/h
```

Retorna uma resposta informando que o veículo foi cadastrado.

---

## ConsultarVeiculo

Recebe uma placa e procura o veículo cadastrado.

Se existir:

```text
Veículo encontrado.
```

Se não existir:

```text
NOT_FOUND
```

---

## CalcularMediaVelocidade

Recebe uma lista de velocidades e calcula a média.

Exemplo:

```text
10, 20, 30
```

Resultado:

```text
20
```

O método também possui um campo `delay_ms`. Ele serve para demonstrar deadline.

---

# 9. Status de erro

O projeto utiliza mais de dois status gRPC.

## INVALID_ARGUMENT

Usado quando o cliente envia dados inválidos.

Exemplos:

- placa vazia;
- velocidade negativa;
- lista vazia;
- setor vazio.

---

## ALREADY_EXISTS

Usado quando o cliente tenta cadastrar uma placa que já existe.

---

## NOT_FOUND

Usado quando o cliente tenta consultar uma placa que não foi cadastrada.

---

## DEADLINE_EXCEEDED

Acontece quando o servidor demora mais do que o tempo que o cliente aceitou esperar.

---

## UNAVAILABLE

Normalmente aparece quando o cliente tenta acessar um servidor que está desligado ou indisponível.

O material da disciplina diferencia `INVALID_ARGUMENT` de `UNAVAILABLE`: o primeiro está relacionado à entrada/operação e o segundo tende a indicar problema transitório de infraestrutura.

---

# 10. Executar o servidor

Abra um terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python servidor.py
```

Resultado esperado:

```text
============================================================
SERVIDOR gRPC - AP4
============================================================
Servidor iniciado em localhost:50051
Aguardando chamadas...
```

Não feche esse terminal.

---

# 11. Executar o cliente

Abra um segundo terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python cliente.py
```

O cliente executa várias demonstrações:

1. cadastro;
2. consulta;
3. erro de validação;
4. veículo não encontrado;
5. cadastro duplicado;
6. deadline;
7. concorrência.

---

# 12. Testes separados

Também existe:

```text
testes.py
```

Executar:

```powershell
python testes.py
```

O script realiza chamadas concorrentes para o servidor.

Ele mede aproximadamente o tempo das chamadas e mostra o resultado de cada uma.

---

# 13. Experimento de deadline

O método `CalcularMediaVelocidade` recebe:

```text
delay_ms
```

Quando o cliente manda, por exemplo:

```text
delay_ms = 2000
```

o servidor espera 2 segundos antes de responder.

Se o cliente usar:

```python
timeout=0.5
```

ele aceita esperar somente 0,5 segundo.

Nesse caso o resultado esperado é:

```text
DEADLINE_EXCEEDED
```

A ideia é mostrar que o tempo da chamada remota faz parte do comportamento do sistema distribuído.

---

# 14. Experimento de servidor indisponível

1. Execute o servidor.
2. Execute o cliente uma vez.
3. Feche o servidor com `Ctrl + C`.
4. Execute novamente o cliente.

As chamadas não conseguirão chegar ao serviço.

O cliente deverá apresentar um erro relacionado à indisponibilidade, normalmente:

```text
StatusCode.UNAVAILABLE
```

Isso é diferente de `INVALID_ARGUMENT`.

---

# 15. Experimento concorrente

O arquivo `testes.py` usa:

```python
ThreadPoolExecutor
```

para realizar várias chamadas ao mesmo tempo.

A ideia é simular vários clientes acessando o mesmo servidor.

No servidor existe:

```python
ThreadPoolExecutor(max_workers=10)
```

Assim, o servidor consegue processar chamadas em múltiplas threads.

---

# 16. Evolução do contrato

A versão inicial possui:

```text
Placa
Modelo
Velocidade
Setor
```

Na evolução foi adicionado um novo campo:

```text
observacao
```

O novo campo recebe um número próprio no `.proto`.

Isso é uma mudança compatível porque clientes antigos podem continuar usando os campos que já conhecem.

Regra importante do Protocol Buffers:

- números de campos existentes não devem ser reutilizados;
- novos campos podem ser adicionados de forma compatível;
- mudanças incompatíveis precisam de versionamento ou migração coordenada.

---

# 17. Como demonstrar a evolução

Compare:

```text
evolucao/v1/processador_v1.proto
```

com:

```text
evolucao/v2/processador_v2.proto
```

Na V2 existe o campo adicional:

```protobuf
string observacao = 5;
```

O número `5` não era utilizado na V1.

Depois explique:

> "Eu adicionei um novo campo usando um número de campo que ainda não existia. Dessa forma, clientes antigos continuam reconhecendo os campos antigos, enquanto clientes novos conseguem utilizar o campo adicional."

---

# 18. Comparação com AP2 e AP3

## gRPC

No AP4 o contrato é definido pelo:

```text
processador.proto
```

O cliente utiliza um stub gerado e as mensagens são serializadas pelo Protocol Buffers.

Características:

- contrato forte;
- tipagem definida;
- geração automática de código;
- comunicação RPC;
- suporte a deadlines;
- códigos de status;
- suporte a streaming.

---

## REST — AP2

Na API REST trabalhamos com requisições HTTP e normalmente JSON.

Exemplo conceitual:

```text
POST /eventos
GET /eventos
```

No REST, o contrato pode ser mais flexível e a comunicação utiliza diretamente HTTP.

---

## MQTT — AP3

No MQTT a comunicação é baseada em:

```text
publisher -> broker -> subscriber
```

O produtor publica uma mensagem em um tópico e os consumidores interessados recebem a mensagem.

Exemplo:

```text
laboratorio/sensor1/telemetria
```

---

## Resumo

| Característica | gRPC | REST | MQTT |
|---|---|---|---|
| Modelo | RPC | HTTP/recursos | Pub/Sub |
| Contrato | `.proto` | normalmente API/JSON | tópicos/mensagens |
| Comunicação | chamada de método | requisição HTTP | publicação/assinatura |
| Streaming | possui | possível via tecnologias HTTP | fluxo de mensagens |
| Deadline | recurso direto do cliente gRPC | depende da implementação | não é o foco principal |
| Broker obrigatório | não | não | sim |
| Tipagem | forte com Protobuf | geralmente mais flexível | payload depende da aplicação |

---

# 19. Respostas das questões da atividade

## 1. Por que uma chamada remota não deve ser tratada como função local?

Porque uma função local normalmente depende apenas do próprio processo, enquanto uma chamada remota depende da rede e de outro processo.

Uma RPC pode sofrer:

- latência;
- perda de conexão;
- indisponibilidade;
- timeout;
- erros de serialização;
- falhas no servidor.

Por isso, o programa precisa tratar essas situações.

---

## 2. Qual diferença entre erro de aplicação e indisponibilidade do serviço?

Um erro de aplicação acontece quando o serviço está acessível, mas a solicitação não é válida para aquela operação.

Exemplo:

```text
INVALID_ARGUMENT
```

Já `UNAVAILABLE` indica que o cliente não conseguiu utilizar o serviço, normalmente por uma falha de infraestrutura ou indisponibilidade.

---

## 3. O contrato forte aumenta qual tipo de acoplamento?

Aumenta principalmente o acoplamento ao contrato/esquema.

Isso traz benefícios porque cliente e servidor compartilham uma definição clara de mensagens e métodos.

Por outro lado, mudanças no contrato precisam ser planejadas.

---

## 4. Como fazer retry sem duplicar efeitos perigosos?

Primeiro é necessário verificar se a operação é segura para repetição.

Operações de leitura normalmente são mais simples de repetir.

Para operações que alteram dados, uma estratégia possível é utilizar uma chave/idempotency key para identificar a mesma operação.

Também é importante considerar que `DEADLINE_EXCEEDED` não garante que o servidor não tenha executado a operação.

---

## 5. Que mudança no .proto seria incompatível?

Uma mudança incompatível pode acontecer ao reutilizar o número de um campo removido para representar outra informação.

Outra possibilidade é alterar de forma incompatível o tipo ou a semântica de um campo já utilizado.

Por isso, números de campos antigos devem ser preservados.

---

# 20. Roteiro para apresentação

## Parte 1 — Introdução

Fale:

> "Minha atividade implementa um serviço remoto usando gRPC. Eu escolhi trabalhar com um pequeno serviço de gerenciamento de veículos porque ele permite demonstrar cadastro, consulta, validação, erro, timeout e concorrência."

---

## Parte 2 — Mostrar o `.proto`

Abra:

```text
processador.proto
```

Fale:

> "Eu comecei pelo contrato, antes de implementar o servidor. Aqui eu defino os métodos RPC e as mensagens que serão utilizadas."

Mostre:

```protobuf
service Processador
```

Depois:

```protobuf
rpc RegistrarVeiculo
rpc ConsultarVeiculo
rpc CalcularMediaVelocidade
```

Explique que são três métodos RPC, atendendo ao requisito mínimo da atividade.

---

## Parte 3 — Mostrar a geração

Mostre:

```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

Explique:

> "Esse comando pega o contrato `.proto` e gera automaticamente os arquivos Python necessários para cliente e servidor."

---

## Parte 4 — Mostrar servidor

Abra:

```text
servidor.py
```

Mostre primeiro:

```python
class Processador(pb2_grpc.ProcessadorServicer):
```

Explique:

> "Essa classe implementa o serviço definido no arquivo `.proto`."

Depois mostre os três métodos.

---

## Parte 5 — Mostrar cliente

Abra:

```text
cliente.py
```

Mostre:

```python
stub = pb2_grpc.ProcessadorStub(channel)
```

Explique:

> "O stub é a representação local do serviço remoto. Eu chamo o método pelo stub, mas a execução acontece no servidor."

---

## Parte 6 — Mostrar deadline

Mostre:

```python
timeout=0.5
```

Explique:

> "Aqui eu configurei um limite de tempo. Se o servidor demorar mais do que esse limite, o cliente encerra a espera e recebe DEADLINE_EXCEEDED."

---

## Parte 7 — Demonstrar erro

Mostre uma consulta de placa inexistente.

Explique:

> "Nesse caso o servidor está funcionando. O problema é que o recurso solicitado não existe. Por isso eu uso NOT_FOUND."

Depois mostre o cadastro duplicado:

```text
ALREADY_EXISTS
```

---

## Parte 8 — Demonstrar servidor desligado

Pare o servidor:

```text
Ctrl + C
```

Execute o cliente.

Explique:

> "Agora a situação é diferente. O serviço não está disponível. Por isso o cliente recebe UNAVAILABLE."

---

## Parte 9 — Demonstrar concorrência

Ligue novamente o servidor.

Execute:

```powershell
python testes.py
```

Explique:

> "Aqui eu estou fazendo várias chamadas simultaneamente para demonstrar concorrência."

---

## Parte 10 — Evolução

Abra:

```text
evolucao/v1/processador_v1.proto
```

e depois:

```text
evolucao/v2/processador_v2.proto
```

Mostre o novo campo:

```protobuf
string observacao = 5;
```

Explique que o número é novo e não substitui um campo antigo.

---

# 21. Checklist antes de entregar

- [ ] `.proto` presente.
- [ ] `servidor.py` presente.
- [ ] `cliente.py` presente.
- [ ] `testes.py` presente.
- [ ] `requirements.txt` presente.
- [ ] `gerar_stubs.bat` presente.
- [ ] README atualizado.
- [ ] Stubs podem ser regenerados.
- [ ] Cliente possui timeout.
- [ ] Existe erro `INVALID_ARGUMENT`.
- [ ] Existe erro `NOT_FOUND`.
- [ ] Existe erro `ALREADY_EXISTS`.
- [ ] Existe teste de `DEADLINE_EXCEEDED`.
- [ ] Existe teste de `UNAVAILABLE`.
- [ ] Existe concorrência.
- [ ] Existe evolução compatível do `.proto`.
- [ ] Comparação com AP2 e AP3 documentada.

---

# 22. Comandos rápidos para o dia da apresentação

### Terminal 1 — servidor

```powershell
.\.venv\Scripts\Activate.ps1
python servidor.py
```

### Terminal 2 — cliente

```powershell
.\.venv\Scripts\Activate.ps1
python cliente.py
```

### Terminal 3 — concorrência

```powershell
.\.venv\Scripts\Activate.ps1
python testes.py
```

### Regenerar stubs

```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto
```

---

# 23. O que eu preciso saber explicar

Se o professor perguntar "o que é gRPC?":

> "É um framework de chamada de procedimento remoto. O cliente chama métodos definidos no contrato e o gRPC cuida da comunicação, serialização e transporte."

Se perguntar "o que é Protobuf?":

> "É a forma usada no projeto para definir as mensagens e o contrato. A partir do `.proto`, são gerados os códigos necessários para cliente e servidor."

Se perguntar "o que é stub?":

> "É o código gerado que permite ao cliente chamar o serviço remoto como se estivesse utilizando uma interface local."

Se perguntar "o que é deadline?":

> "É o limite de tempo que o cliente aceita esperar por uma chamada remota."

Se perguntar "por que não usar timeout infinito?":

> "Porque uma chamada remota pode ficar bloqueada devido a uma falha ou indisponibilidade, consumindo recursos sem necessidade."

Se perguntar "qual diferença entre INVALID_ARGUMENT e UNAVAILABLE?":

> "`INVALID_ARGUMENT` representa uma entrada inválida para a operação. `UNAVAILABLE` indica que o serviço não está disponível para atender a chamada."

Se perguntar "por que usar `.proto`?":

> "Para ter um contrato explícito entre cliente e servidor e permitir geração dos stubs."

Se perguntar "por que gRPC e não REST?":

> "Eles atendem necessidades diferentes. Neste projeto eu precisava demonstrar RPC, contrato com Protobuf, stubs, deadlines e status gRPC, que são recursos centrais do gRPC."

---

# 24. Observação importante

Os arquivos `*_pb2.py` e `*_pb2_grpc.py` podem ser apagados e recriados com o comando de geração.

Isso demonstra que o projeto é reproduzível a partir do contrato:

```text
.proto
  ↓
protoc
  ↓
código gerado
  ↓
cliente + servidor
```

O arquivo `.proto` é a fonte do contrato.
