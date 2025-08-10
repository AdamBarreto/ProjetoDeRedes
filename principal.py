
import pygame
import json
import socket
import sys

import Redes

# Configurações de rede
ip, familia, protocolo, sock = Redes.config_rede()

#definir se vai hospedar ou conectar
esc = input("Você quer hospedar ou conectar a uma partida? (h/c): ").strip().lower()
if esc == 'h':
    sock, coisado = Redes.hospedar_partida(ip, sock, familia, protocolo)
    if (protocolo == socket.SOCK_DGRAM):
        destino_ip = input("Digite o endereço IP do computador que está se conectando ao servidor: ")
        destino = (destino_ip, coisado)
    else:
        destino = coisado

elif esc == 'c':
    sock, destino = Redes.conectar_partida(familia, protocolo)

