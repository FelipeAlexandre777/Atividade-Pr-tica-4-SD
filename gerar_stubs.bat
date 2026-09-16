@echo off
echo ============================================================
echo GERANDO STUBS gRPC
echo ============================================================

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processador.proto

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Stubs gerados com sucesso!
    echo Arquivos:
    echo   processador_pb2.py
    echo   processador_pb2_grpc.py
) else (
    echo.
    echo Erro ao gerar os stubs.
    echo Verifique se grpcio-tools esta instalado.
)

pause
