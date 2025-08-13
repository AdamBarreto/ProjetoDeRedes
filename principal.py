import socket
import Redes
import damas
import sys
import threading
import time

# Configurações de rede
ip, familia, protocolo, sock = Redes.config_rede()

# definir se vai hospedar ou conectar
esc = input(
    "Você quer hospedar ou conectar a uma partida? (h/c): ").strip().lower()
if esc == 'h':
    COR_LOCAL = "WHITE"
    sock, coisado = Redes.hospedar_partida(ip, sock, familia, protocolo)
    if (protocolo == socket.SOCK_DGRAM):
        destino_ip = input(
            "Digite o endereço IP do computador que está se conectando ao servidor: ")
        destino = (destino_ip, coisado)
    else:
        destino = coisado

elif esc == 'c':
    COR_LOCAL = "BLACK"
    sock, destino = Redes.conectar_partida(familia, protocolo)

if sock is None:
    print("Não foi possível estabelecer conexão. Encerrando.")
    exit()


else:

    tranca = threading.Lock()

    def comunicacao():
        while damas.run:
            with tranca:
                if damas.turn == COR_LOCAL:
                    dados = damas.export_board_state(
                        damas.board)  # Exporta estado
                    Redes.enviar_mensagem(
                        sock, dados, protocolo, destino)  # Envia
                    damas.turn = damas.BLACK if damas.turn == damas.WHITE else damas.WHITE
                else:
                    # Espera jogada do adversário
                    dados_recebidos, origem = Redes.receber_mensagem(
                        sock, protocolo)
                    if dados_recebidos:
                        damas.import_board_state(
                            damas.board, dados_recebidos)  # Atualiza tabuleiro
                        damas.turn = COR_LOCAL  # Agora é sua vez
            time.sleep(1/60)

    threadComunicaco = threading.Thread(target=comunicacao)
    threadJogo = threading.Thread(
        target=damas.main(COR_LOCAL, tranca))  # Executa jogada local

    threadComunicaco.start()
    threadJogo.start()

    threadJogo.join()
    threadComunicaco.join()

sys.exit()
