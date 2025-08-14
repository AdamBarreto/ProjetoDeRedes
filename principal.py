import socket
import Redes
import damas
import sys

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
    dama = damas.JogoDamas()
    dama.main(COR_LOCAL)
    while dama.run:
        if dama.turn == COR_LOCAL:
            while True:
                    dados = dama.retornar_dado()
                    if dados:
                        Redes.enviar_mensagem(sock, dados, protocolo, destino)  # Envia
                        dados = {}
                        if (dama.turn != COR_LOCAL):
                            break
        else:
            while True:
                # Espera jogada do adversário
                dados_recebidos, origem = Redes.receber_mensagem(sock, protocolo)
                if dados_recebidos:
                    dama.import_board_state(dama.board, dados_recebidos)  # Atualiza tabuleiro
                    dados_recebidos = {}
                    if(dama.turn == COR_LOCAL):
                        break

sys.exit()