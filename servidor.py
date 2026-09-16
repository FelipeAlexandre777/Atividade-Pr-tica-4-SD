from concurrent import futures
import time

import grpc

import processador_pb2 as pb2
import processador_pb2_grpc as pb2_grpc


# Dicionário simples para simular um armazenamento em memória.
# Não é um banco de dados: ele existe apenas durante a execução.
veiculos = {}


class Processador(pb2_grpc.ProcessadorServicer):
    """Implementação dos métodos definidos no arquivo .proto."""

    def RegistrarVeiculo(self, request, context):
        placa = request.placa.strip().upper()
        modelo = request.modelo.strip()
        setor = request.setor.strip()

        # Validação explícita dos dados recebidos.
        if not placa:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "a placa não pode ser vazia",
            )

        if not modelo:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "o modelo não pode ser vazio",
            )

        if not setor:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "o setor não pode ser vazio",
            )

        if request.velocidade < 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "a velocidade não pode ser negativa",
            )

        if placa in veiculos:
            context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                f"o veículo {placa} já está cadastrado",
            )

        veiculos[placa] = {
            "modelo": modelo,
            "velocidade": request.velocidade,
            "setor": setor,
        }

        return pb2.VeiculoResponse(
            placa=placa,
            modelo=modelo,
            velocidade=request.velocidade,
            setor=setor,
            mensagem="veículo cadastrado com sucesso",
        )

    def ConsultarVeiculo(self, request, context):
        placa = request.placa.strip().upper()

        if not placa:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "a placa não pode ser vazia",
            )

        veiculo = veiculos.get(placa)

        if veiculo is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"veículo {placa} não encontrado",
            )

        return pb2.VeiculoResponse(
            placa=placa,
            modelo=veiculo["modelo"],
            velocidade=veiculo["velocidade"],
            setor=veiculo["setor"],
            mensagem="veículo encontrado",
        )

    def CalcularMediaVelocidade(self, request, context):
        if not request.velocidades:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "a lista de velocidades não pode ser vazia",
            )

        for velocidade in request.velocidades:
            if velocidade < 0:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "a lista possui velocidade negativa",
                )

        # Esse atraso é proposital para demonstrar deadline/timeout.
        if request.delay_ms > 0:
            time.sleep(request.delay_ms / 1000)

        media = sum(request.velocidades) / len(request.velocidades)

        return pb2.MediaVelocidadeResponse(
            media=media,
            quantidade=len(request.velocidades),
        )


def serve():
    # O servidor usa um pool de threads para atender chamadas concorrentes.
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    pb2_grpc.add_ProcessadorServicer_to_server(
        Processador(),
        server,
    )

    # Porta usada apenas para o laboratório local.
    server.add_insecure_port("localhost:50051")
    server.start()

    print("=" * 60)
    print("SERVIDOR gRPC - AP4")
    print("=" * 60)
    print("Servidor iniciado em localhost:50051")
    print("Aguardando chamadas...")
    print("Pressione Ctrl+C para encerrar.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
