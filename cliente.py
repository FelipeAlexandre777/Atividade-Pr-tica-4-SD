import grpc

import processador_pb2 as pb2
import processador_pb2_grpc as pb2_grpc


ENDERECO_SERVIDOR = "localhost:50051"


def mostrar_erro(nome, exc):
    print(f"{nome}:")
    print(f"  status: {exc.code()}")
    print(f"  detalhe: {exc.details()}")


def main():
    print("=" * 60)
    print("CLIENTE gRPC - AP4")
    print("=" * 60)

    # O canal representa a conexão lógica com o servidor.
    with grpc.insecure_channel(ENDERECO_SERVIDOR) as channel:
        # Stub gerado automaticamente a partir do .proto.
        stub = pb2_grpc.ProcessadorStub(channel)

        # ---------------------------------------------------------
        # 1. Cadastro
        # ---------------------------------------------------------
        print("\n[1] Cadastrando veículo...")

        try:
            resposta = stub.RegistrarVeiculo(
                pb2.VeiculoRequest(
                    placa="ABC1D23",
                    modelo="Volvo FH",
                    velocidade=65.5,
                    setor="Transporte",
                ),
                timeout=2.0,
            )

            print(f"  {resposta.mensagem}")
            print(f"  Placa: {resposta.placa}")
            print(f"  Modelo: {resposta.modelo}")
            print(f"  Setor: {resposta.setor}")
            print(f"  Velocidade: {resposta.velocidade} km/h")

        except grpc.RpcError as exc:
            mostrar_erro("  Falha no cadastro", exc)

        # ---------------------------------------------------------
        # 2. Consulta
        # ---------------------------------------------------------
        print("\n[2] Consultando veículo...")

        try:
            resposta = stub.ConsultarVeiculo(
                pb2.ConsultaRequest(placa="ABC1D23"),
                timeout=2.0,
            )

            print(f"  {resposta.mensagem}")
            print(f"  {resposta.placa} - {resposta.modelo}")
            print(f"  Setor: {resposta.setor}")

        except grpc.RpcError as exc:
            mostrar_erro("  Falha na consulta", exc)

        # ---------------------------------------------------------
        # 3. Validação explícita
        # ---------------------------------------------------------
        print("\n[3] Testando argumento inválido...")

        try:
            stub.RegistrarVeiculo(
                pb2.VeiculoRequest(
                    placa="",
                    modelo="Caminhão",
                    velocidade=50,
                    setor="Transporte",
                ),
                timeout=2.0,
            )

        except grpc.RpcError as exc:
            mostrar_erro("  Esperado", exc)

        # ---------------------------------------------------------
        # 4. NOT_FOUND
        # ---------------------------------------------------------
        print("\n[4] Consultando veículo inexistente...")

        try:
            stub.ConsultarVeiculo(
                pb2.ConsultaRequest(placa="ZZZ9Z99"),
                timeout=2.0,
            )

        except grpc.RpcError as exc:
            mostrar_erro("  Esperado", exc)

        # ---------------------------------------------------------
        # 5. ALREADY_EXISTS
        # ---------------------------------------------------------
        print("\n[5] Tentando cadastrar a mesma placa novamente...")

        try:
            stub.RegistrarVeiculo(
                pb2.VeiculoRequest(
                    placa="ABC1D23",
                    modelo="Outro modelo",
                    velocidade=30,
                    setor="Teste",
                ),
                timeout=2.0,
            )

        except grpc.RpcError as exc:
            mostrar_erro("  Esperado", exc)

        # ---------------------------------------------------------
        # 6. Deadline
        # ---------------------------------------------------------
        print("\n[6] Testando deadline...")

        try:
            # O servidor espera 2 segundos, mas o cliente aceita
            # esperar somente 0,5 segundo.
            stub.CalcularMediaVelocidade(
                pb2.MediaVelocidadeRequest(
                    velocidades=[10, 20, 30],
                    delay_ms=2000,
                ),
                timeout=0.5,
            )

        except grpc.RpcError as exc:
            mostrar_erro("  Esperado", exc)

        # ---------------------------------------------------------
        # 7. Chamada normal de média
        # ---------------------------------------------------------
        print("\n[7] Calculando média sem atraso...")

        try:
            resposta = stub.CalcularMediaVelocidade(
                pb2.MediaVelocidadeRequest(
                    velocidades=[40, 50, 60, 70],
                    delay_ms=0,
                ),
                timeout=2.0,
            )

            print(f"  Média: {resposta.media:.2f} km/h")
            print(f"  Quantidade: {resposta.quantidade}")

        except grpc.RpcError as exc:
            mostrar_erro("  Falha", exc)

    print("\nFim do cliente.")


if __name__ == "__main__":
    main()
