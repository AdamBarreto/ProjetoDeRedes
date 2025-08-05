import socket
import ipaddress

#<--- Escolha das configurações de rede --->
def config_rede():
  
  #<-- verificar o ip digitado>
  while True:
        end_ip = input("Digite o seu endereço IP. Ex.: '127.0.0.1' ou 'fe80::1': ").strip()
        try:
            ip = ipaddress.ip_address(end_ip)
            print(f"Endereço IP válido: {ip}")
            break
        except ValueError:
            print("Endereço IP inválido. Digite-o corretamente")
  while True:
    t_ip = input("\nEscolha a versão do protocolo de internet (IP) para a criação do socket, digite 'ipv4' ou 'ipv6': ").lower().strip()

    if (t_ip == "ipv4" and isinstance(ip, ipaddress.IPv4Address)):
            familia = socket.AF_INET
            break

    elif (t_ip == "ipv6" and isinstance(ip, ipaddress.IPv6Address)):
            familia = socket.AF_INET6
            break

    else:
       print("\n-> Versão do IP inválida. Digite exclusivamente 'ipv4' ou 'ipv6', e certifique-se de que a versão do seu endereço IP seja condizente com sua escolha.")

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
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  print("-> Socket criado com sucesso")
  return ip, familia, protocolo, sock

#essa parte de baixo vai pro main
ip, familia, protocolo, sock = config_rede()


#tenho que importar a biblioteca ipaddress
#vai ser perguntado a pessoa a porta (1014-49151) e o seu IP
def hospedar_partida(host, porta, sock, familia, protocolo):
  
  while True:
    porta = input("\nDigite a porta que deseja iniciar o servidor (1024 - 65535): ").strip()
    if porta.isdigit() and 1024 <= int(porta) <= 65535:
      porta = int(porta)
      break
  print("-> Porta inválida. Digite apenas números entre 1024 e 65535.")

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
