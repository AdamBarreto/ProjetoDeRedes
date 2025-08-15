import socket
import ipaddress
import json
#<--- Escolha das configurações de rede --->
def config_rede():
  
  #<-- verificar o ip digitado>
  while True:
        end_ip = input("Digite o seu endereço IP. Ex.: '127.0.0.1' ou 'fe80::1': ").strip()
        try:
            ip = ipaddress.ip_address(end_ip)
            print(f"Endereço IP válido: {ip}")
            break
        
        # mensagem de erro
        except ValueError:
            print("Endereço IP inválido. Digite-o corretamente")
  while True:
    
    if (isinstance(ip, ipaddress.IPv4Address)):
            familia = socket.AF_INET
            break

    elif (isinstance(ip, ipaddress.IPv6Address)):
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



def hospedar_partida(host_ip, sock, familia, protocolo):
  
  while True:
    porta = input("\nDigite a porta que deseja iniciar o servidor (1024 - 65535): ").strip()
    if porta.isdigit() and 1024 <= int(porta) <= 65535:
      porta = int(porta)
      break
    print("-> Porta inválida. Digite apenas números entre 1024 e 65535.\n10.65.1.113")

  try:
    if familia == socket.AF_INET6:
      sock.bind(str((host_ip), porta, 0, 0))
    else:
      sock.bind((str(host_ip), porta))
    tipo_ip = "IPv6" if familia == socket.AF_INET6 else "IPv4"
    print(f"Host {tipo_ip} criado com sucesso. IP: {host_ip} - Porta: {porta}")
  
  # mensagem de erro
  except Exception as e:

        raise ValueError(
            "O Host não foi criado. Insira o seu endereço IP corretamente e "
            "certifique-se de que a porta esteja na faixa de 1024-65535."
        ) from e

  # TCP
  if (protocolo == socket.SOCK_STREAM):
    sock.listen(1)
    print("\nEsperando conexão com um jogador [...]")

    try:
      conexao, (cliente_ip, porta) = sock.accept()
      print(f"Servidor TCP conectado com IP {cliente_ip} da porta {porta}")
      return conexao, (cliente_ip, porta)
    
    # mensagem de erro
    except Exception as e:
      print("Não foi possível estabelecer conexão com jogador. Encerrando...")
      exit()

  # UDP
  elif protocolo == socket.SOCK_DGRAM:
    print("\nServidor UDP pronto para receber mensagens.")

    # Espera a primeira mensagem do cliente para capturar IP e porta
    print("Aguardando mensagem inicial do cliente UDP...")
    mensagem, origem = sock.recvfrom(4096)
    print(f"Mensagem inicial recebida de {origem}")
    
    try:
        dados = json.loads(mensagem.decode('utf-8'))
        print("\nMensagem inicial decodificada com sucesso.")
    except Exception as e:
        print(f"\nErro ao decodificar mensagem inicial: {e}")
        dados = None

    return sock, origem  # origem é uma tupla (ip, porta)





def conectar_partida(familia, protocolo):
  while True:
    destino_ip = input("Digite o endereço IP do computador que está hospedando a partida: ")
    try:
      dest_ip = ipaddress.ip_address(destino_ip)
      print(f"Endereço IP válido [{dest_ip}]")
      break
    except ValueError:
       print("Endereço IP inválido. Digite-o corretamente: ")
       


  while True:
    destino_porta = input("Digite a porta do socket do computador que está hospedando a partida: ").strip()
    if destino_porta.isdigit() and 1024 <= int(destino_porta) <= 65535:
        destino_porta = int(destino_porta)
        break
    print("-> Porta inválida. Digite apenas números entre 1024 e 65535.")

  try:
    # TCP
    if (protocolo == socket.SOCK_STREAM):
      sock = socket.socket(familia, protocolo)
      sock.connect((str(destino_ip), destino_porta))
      print(f"Conectado ao servidor TCP no IP {destino_ip} na porta {destino_porta}")
      
    # UDP
    elif (protocolo == socket.SOCK_DGRAM):
      sock = socket.socket(familia, protocolo)
      print(f"Conectado ao servidor UDP no IP {destino_ip} na porta {destino_porta}")
    return sock, (str(destino_ip), destino_porta)
  
  # mensagem de erro
  except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")
    print("Encerrando...")
    exit()
    
  

def enviar_mensagem(sock, dados, protocolo, destino):
    try:
        mensagem = json.dumps(dados).encode('utf-8')
        # TCP
        if protocolo == socket.SOCK_STREAM:
            sock.sendall(mensagem)

        #UDP
        elif protocolo == socket.SOCK_DGRAM:
            sock.sendto(mensagem, destino)

        print("Mensagem enviada com sucesso.")

    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")



def receber_mensagem(sock, protocolo, buffer_size=4096):
    print("Aguardando mensagem [...]")
    try:
        if protocolo == socket.SOCK_STREAM:
            mensagem = sock.recv(buffer_size)
            if not mensagem:
               return None, None
            dados = json.loads(mensagem.decode('utf-8'))
            print("Mensagem recebida com sucesso.")
            return dados, None

        elif protocolo == socket.SOCK_DGRAM:
            mensagem, origem = sock.recvfrom(buffer_size)
            if not mensagem:
              return None, origem
            dados = json.loads(mensagem.decode('utf-8'))
            print(f"Mensagem recebida de {origem}")
            return dados, origem

    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        return None, None