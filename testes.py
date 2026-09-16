from concurrent.futures import ThreadPoolExecutor, as_completed
import time

import grpc

import processador_pb2 as pb2
import processador_pb2_grpc as pb2_grpc


ENDERECO_SERVIDOR = "localhost:50051"


def chamada_concorrente(numero):
    inicio = time.perf_counter()

    try:
        # Cada tarefa cria seu próprio canal.
        # Isso deixa o teste simples de entender e simula
        # chamadas independentes chegando ao serviço.
        with grpc.insecure_channel(ENDERECO_SERVIDOR) as channel:
            stub = pb2_grpc.ProcessadorStub(channel)

            resposta = stub.CalcularMediaVelocidade(
                pb2.MediaVelocidadeRequest(
                    velocidades=[numero, numero + 10, numero + 20],
                    delay_ms=500,
                ),
                timeout=2.0,
            )

        duracao = time.perf_counter() - inicio

        return (
            numero,
            f"OK - média={resposta.media:.2f} - "
            f"tempo={duracao:.3f}s",
        )

    except grpc.RpcError as exc:
        duracao = time.perf_counter() - inicio

        return (
            numero,
            f"ERRO - status={exc.code()} - "
            f"tempo={duracao:.3f}s",
        )


def main():
    print("=" * 60)
    print("TESTE DE CONCORRÊNCIA - AP4")
    print("=" * 60)

    quantidade = 10

    inicio_total = time.perf_counter()

    # Várias chamadas são disparadas ao mesmo tempo.
    with ThreadPoolExecutor(max_workers=10) as executor:
        tarefas = [
            executor.submit(chamada_concorrente, numero)
            for numero in range(quantidade)
        ]

        for tarefa in as_completed(tarefas):
            numero, resultado = tarefa.result()
            print(f"Chamada {numero}: {resultado}")

    tempo_total = time.perf_counter() - inicio_total

    print("-" * 60)
    print(f"Tempo total aproximado: {tempo_total:.3f}s")
    print("As chamadas foram executadas concorrentemente.")


if __name__ == "__main__":
    main()
