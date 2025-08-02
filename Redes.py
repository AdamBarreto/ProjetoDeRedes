import socket

#<--- Escolha das configurações de rede no menu --->
def config_rede():
  while True:
    t_ip = input("Escolha a versão do protocolo de internet (IP), digite 'ipv4' ou 'ipv6': ").lower().strip()

    if(t_ip == "ipv4"):
      familia = socket.AF_INET
      break                              #Uma pessoa pode escolher ipv6 mesmo sendo ipv4?
    elif(t_ip == "ipv6"):
      familia = socket.AF_INET6
      break
    else: print("-> Versão do IP inválida, digite exclusivamente 'ipv4' ou 'ipv6': ")

  while True:
    protc = input("Escolha o protocolo de rede, digite 'tcp' ou 'udp': ").lower().strip()
    if(protc == "tcp"):
      protocolo = socket.SOCK_STREAM
      break
    elif(protc == "udp"):
      protocolo = socket.SOCK_DGRAM
      break
    else: print("-> Tipo de protocolo inválido, digite exclusivamente 'udp' ou 'tcp': ")

  sock = socket.socket(familia, protocolo)
  print("-> Socket criado com sucesso")
  return familia, protocolo, sock

#essa parte de baixo vai pro main
familia, protocolo, sock = config_rede()

#tenho que importar a biblioteca ipaddress
#vai ser perguntado a pessoa a porta (1014-49151) e o seu IP
def hospedar_partida(host, porta, sock, familia, protocolo):
  try:
    sock.bind((host, porta))
    if (familia == socket.AF_INET):
        print("Host IPv4 criado com sucesso. IP: {host} - Porta: {porta}")
    else: print("Host IPv6 criado com sucesso. IP: {host} - Porta: {porta}")
  except Exception as e:
    print("Host não foi criado, insira o seu endereço IP correto e certifique-se de que a porta esteja na faixa de 1024-49151")

  #<-- SE FOR TCP -->
  if (protocolo == socket.SOCK_STREAM):
    sock.listen(1)
    print("Esperando conexão com um jogador [...]")

    try:
      conexao, (cliente_ip, cliente_porta) = sock.accept()
      print("Servidor TCP conectado com IP {cliente_ip} da porta {cliente_porta}")
      return conexao
    except Exception as e:
      print("Não foi possível estabelecer conexão com jogador")

  #<-- SE FOR UDP -->
  elif(protocolo == socket.SOCK_DGRAM):   #ajeitar
    return sock
    print("Servidor UDP pronto para receber mensagens")
