import socket
import Redes
import damas
import sys
# Configurações de rede
ip, familia, protocolo, sock = Redes.config_rede()

#definir se vai hospedar ou conectar
esc = input("Você quer hospedar ou conectar a uma partida? (h/c): ").strip().lower()
if esc == 'h':
    COR_LOCAL = "WHITE"
    sock, coisado = Redes.hospedar_partida(ip, sock, familia, protocolo)
    if (protocolo == socket.SOCK_DGRAM):
        destino_ip = input("Digite o endereço IP do computador que está se conectando ao servidor: ")
        destino = (destino_ip, coisado)
    else:
        destino = coisado

elif esc == 'c':
    COR_LOCAL = "BLACK"
    sock, destino = Redes.conectar_partida(familia, protocolo)

if sock is None:
    print("Não foi possível estabelecer conexão. Encerrando.")
    exit()

# recomendo o jogo iniciar aqui (oq colocar aqui?)

while damas.run:
    if turn == COR_LOCAL:
        # Jogador local faz jogada
        damas.main(COR_LOCAL)  # Executa jogada local
        dados = damas.export_board_state(damas.board)  # Exporta estado
        Redes.enviar_mensagem(sock, dados, protocolo, destino)  # Envia
        turn = damas.BLACK if turn == damas.WHITE else damas.WHITE
    else:
        # Espera jogada do adversário
        dados_recebidos, origem = Redes.receber_mensagem(sock, protocolo)
        if dados_recebidos:
            damas.import_board_state(damas.board, dados_recebidos)  # Atualiza tabuleiro
            turn = COR_LOCAL  # Agora é sua vez


sys.exit()