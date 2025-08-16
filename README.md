# Jogo de damas
### O Projeto em questão, trata-se da construção de um jogo de damas virtual, onde é necessário ter dois computadores para se conectarem através de um socket, um dos jogadores pode hospedar a partida e outro se conectar, para assim possibilitar que duas pessoas joguem. Portanto, trata-se de uma comunicação P2P que tem suporte à IPv6 e IPv4, e funciona com os protocolos da Camada de transporte UDP e TCP.

## Requisitos para jogar
+ Ter o python com uma versão compatível para o seu computador. Site do python para download: https://www.python.org/
+ Ter o pygame. Site do pygame para download: https://www.pygame.org/downloads.shtml
+ Os dois dispositivos devem estar conectados na mesma rede local

## Como jogar?
### Abra o terminal do seu computador - CMD, Power Shell etc. - e estando conectado à internet digite e aperte Enter: pip install pygame. Esse procedimento é necessário para a instalação do pygame, biblioteca python necessária na execução do jogo. Depois, inicialize a classe damas.py.
### Para jogar o jogo basta clicar com o mouse na peça que deseja mover, logo em seguida o local desejado. E, caso de uma captura disponível, será obrigatório que o jogador realize a(s) captura(s). Em caso de captura multipla apenas selecione a próxima casa a seguir. O resto são regras do jogo de damas convencional.
<br>


## Componentes do projeto
<table>
 <tr align = "center">
  <td> Adam</td>
  <td>Alexandre</td>
  <td>João Gabriel</td>
  <td>Paulo César</td>
</tr>
<tr>
  <td>20231054010024</td>
  <td>20231054010039</td>
  <td>20231054010028</td>
  <td>20231054010026</td>
</tr>
</table> 
</br>

## Camada de aplicação 
### 2. Arquitetura de Solução
Um protocolo de camada de aplicação é um conjunto de regras que define como os dados são formatados e trocados entre aplicações que se comunicam por meio de uma rede. No contexto deste projeto, o protocolo especifica como os clientes do jogo de damas trocam informações sobre o estado do tabuleiro, jogadas realizadas e mensagens de controle.
#fazer o diagrama simples

2.1. Formato das Mensagens
As mensagens são codificadas em formato JSON e enviadas por meio de conexões TCP ou UDP, conforme a escolha do usuário. A estrutura das mensagens permite a representação clara e organizada do estado do jogo.
2.2. Tipos de Mensagens
2.2.1 INICIAR_JOGO
Mensagem para iniciar a partida com parâmetros no loop local do jogador. Porém, o jogo já define que quem começa é o jogador com a cor “WHITE”, sendo este o que hospedou a partida.
Formato: INICIAR_JOGO|<COR_LOCAL>
Exemplo: INICIAR_JOGO|”WHITE”
Então quem for “BLACK” deverá esperar que o outro jogador realize uma jogada antes de poder fazê-la, mas antes disso já será renderizado a interface do jogo.
2.2.2 Estado do Tabuleiro
Essa é a parte que o damas.py vai definir como as informações do tabuleiro vão ser enviadas ou recebidas para que o computador receptor possa atualizar o estado do tabuleiro.
Formato JSON:
{
  "tipo": "estado_tabuleiro",
  "pieces": [
	{
  	"row": <linha>,
  	"col": <coluna>,
  	"color": "white" | "black",
  	"king": true | false
	}]

Esses valores representam as informações de cada peça, localização no tabuleiro, sua cor, e se é dama ou não. O jogador realiza uma jogada e o estado do tabuleiro é exportado usando a função ‘export_board_state’. Em seguida, o estado é enviado ao outro jogador por meio da função ‘enviar_mensagem’. O jogador receptor utiliza ‘receber_mensagem’ para obter o estado e atualiza o tabuleiro com ‘import_board_state’. O jogo continua até que um dos jogadores fique sem jogadas possíveis, então o jogo vai mostrar quem venceu.
