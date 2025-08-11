import pygame
import sys
import json

# Dimensões da janela
WIDTH, HEIGHT = 800, 800  
ROWS, COLS = 8, 8  # Tabuleiro de 8x8
SQUARE_SIZE = WIDTH // COLS  # Tamanho de cada casa do tabuleiro

# Cores utilizadas
DARK_GREEN = (34, 139, 34)   # Casas Escuras
LIGHT_GREEN = (144, 238, 144) # Casas Claras)
WHITE = (255, 255, 255)      # Peças brancas
BLACK = (0, 0, 0)            # Peças pretas
GOLD = (255, 215, 0)         # Cor para coroas das damas
RED = (255, 0, 0)            # Texto/avisos

COR_LOCAL = WHITE

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Damas")

# Define a fonte para textos
FONT = pygame.font.SysFont("Arial", 36)

# CLASSE DAS PEÇAS
class Piece:
    PADDING = 15   # Espaço interno para desenhar a peça
    OUTLINE = 2    # Espessura do contorno

    def __init__(self, row, col, color):
        # Posição inicial
        self.row = row
        self.col = col
        # Cor da peça
        self.color = color
        # Indica se é dama
        self.king = False
        # Direção do movimento
        self.direction = -1 if color == WHITE else 1

    def make_king(self):
        # Transforma a peça em dama
        self.king = True

    def move(self, row, col):
        # Atualiza posição da peça
        self.row = row
        self.col = col

    def draw(self, win, row=None, col=None):
        draw_row = row if row is not None else self.row
        draw_col = col if col is not None else self.col
        
        # gambiarra para inverter a posição das peças

        # Calcula o raio do círculo (peça)
        radius = SQUARE_SIZE // 2 - self.PADDING
        # Desenha contorno preto
        pygame.draw.circle(
            win, BLACK,
            (draw_col * SQUARE_SIZE + SQUARE_SIZE // 2,
             draw_row * SQUARE_SIZE + SQUARE_SIZE // 2),
            radius + self.OUTLINE
        )
        # Desenha o círculo da peça
        pygame.draw.circle(
            win, self.color,
            (draw_col * SQUARE_SIZE + SQUARE_SIZE // 2,
             draw_row * SQUARE_SIZE + SQUARE_SIZE // 2),
            radius
        )
        # Se for dama desenha uma bola dourado no centro
        if self.king:
            pygame.draw.circle(
                win, GOLD,
                (self.col * SQUARE_SIZE + SQUARE_SIZE // 2,
                 self.row * SQUARE_SIZE + SQUARE_SIZE // 2),
                radius // 2
            )

# CLASSE DO TABULEIRO
class Board:
    def __init__(self):
        self.board = []       # Matriz do tabuleiro
        self.create_board()   # Cria peças iniciais

    def draw_squares(self, win):
        # Desenha as casas do tabuleiro alternando as cores
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREEN
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        # Coloca as peças nas posições iniciais
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row % 2 != col % 2:
                    # Primeiras 3 linhas: peças pretas
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    # Últimas 3 linhas: peças brancas
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)  # Casa vazia
                else:
                    self.board[row].append(0)  # Casa vazia

    def draw(self, win, COR_LOCAL, turn):
        # Desenha o tabuleiro e as peças
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                draw_row, draw_col = (7 - row, 7 - col) if COR_LOCAL == BLACK else (row, col)
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win, draw_row, draw_col)

    def move(self, piece, row, col):
        # Troca a posição da peça na matriz
        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        piece.move(row, col)

        # Promove para dama se chegar no lado oposto
        if (row == 0 and piece.color == WHITE) or (row == ROWS - 1 and piece.color == BLACK):
            piece.make_king()

    def get_piece(self, row, col):
        # Retorna o objeto peça na posição informada
        return self.board[row][col]

    def remove(self, pieces):
        # Remove peças capturadas
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

    def get_valid_moves(self, piece):
        # Retorna todos os movimentos válidos para uma peça
        moves = {}
        capture_moves = {}

        # Direções possíveis
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d in directions:
            r, c = piece.row + d[0], piece.col + d[1]

            # Percorre na direção enquanto estiver dentro do tabuleiro
            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == 0:
                    # Movimento simples (sem captura)
                    if not capture_moves and (piece.king or d[0] == piece.direction):
                        moves[(r, c)] = []
                    if not piece.king:
                        break
                elif self.board[r][c] != 0 and self.board[r][c].color != piece.color:
                    # Possível captura
                    jump_r, jump_c = r + d[0], c + d[1]
                    while 0 <= jump_r < ROWS and 0 <= jump_c < COLS:
                        if self.board[jump_r][jump_c] == 0:
                            capture_moves[(jump_r, jump_c)] = [self.board[r][c]]
                            if not piece.king:
                                break
                        else:
                            break
                        jump_r += d[0]
                        jump_c += d[1]
                    break
                else:
                    break

                # Se for dama, continua explorando na mesma direção
                if piece.king:
                    r += d[0]
                    c += d[1]
                else:
                    break

        return capture_moves if capture_moves else moves

# FUNÇÕES AUXILIARES
def get_all_valid_moves(board, color):
    # Retorna todos os movimentos possíveis para todas as peças de uma cor
    all_moves = {}
    capture_available = False

    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece != 0 and piece.color == color:
                moves = board.get_valid_moves(piece)
                for move, captured in moves.items():
                    if captured:
                        capture_available = True
                        all_moves[(piece, move)] = captured
                    else:
                        all_moves[(piece, move)] = []

    # Só deixa jogar a peça que pode capturar
    if capture_available:
        all_moves = {k: v for k, v in all_moves.items() if v}

    return all_moves, capture_available

def draw_turn_indicator(win, turn):
    # Exibe na tela de quem é a vez
    text = "Vez das Brancas" if turn == WHITE else "Vez das Pretas"
    img = FONT.render(text, True, RED)
    win.blit(img, (10, 10))

def draw_winner(win, winner):
    # Mostra mensagem de vencedor e pausa 3 segundos
    text = "Brancas venceram!" if winner == WHITE else "Pretas venceram!"
    img = FONT.render(text, True, RED)
    win.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# FUNÇÕES PARA EXPORTAR E IMPORTAR O ESTADO DO JOGO
def export_board_state(board, turn):
    pieces = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece != 0:
                pieces.append({
                    'row': piece.row,
                    'col': piece.col,
                    'color': 'white' if piece.color == WHITE else 'black',
                    'king': piece.king
                })
    board_state = {
        'turn': 'white' if turn == WHITE else 'black',
        'pieces': pieces
    }

    return json.dumps(board_state)

#json_data = export_board_state(board, turn)

def import_board_state(board, json_data):
    data = json.loads(json_data)
    turn = WHITE if data['turn'] == 'white' else BLACK

    board.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for piece_info in data['pieces']:
        row = piece_info['row']
        col = piece_info['col']
        color = WHITE if piece_info['color'] == 'white' else BLACK
        piece = Piece(row, col, color)
        if piece_info['king']:
            piece.make_king()
        board.board[row][col] = piece
    return turn

#turn = import_board_state(board, json_data)


# FUNÇÃO PRINCIPAL DO JOGO
def main(COR_LOCAL):
    run = True
    clock = pygame.time.Clock()
    board = Board()      # Cria o tabuleiro
    turn = WHITE         # Brancas começam
    selected_piece = None
    valid_moves = {}
    capture_forced = False

    while run:
        clock.tick(60)  # Limita FPS a 60
        board.draw(WIN, COR_LOCAL, turn)  # Desenha o tabuleiro e peças
        draw_turn_indicator(WIN, turn)
        pygame.display.update()

        # Obtém todos os movimentos possíveis para a cor atual
        all_moves, capture_forced = get_all_valid_moves(board, turn)

        # Se não houver movimentos, fim de jogo
        if not all_moves:
            draw_winner(WIN, BLACK if turn == WHITE else WHITE)
            run = False
            continue

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if COR_LOCAL == BLACK:
                    col, row = 7 - col, 7 - row

                if selected_piece:
                    if (row, col) in valid_moves:
                        # Move a peça
                        board.move(selected_piece, row, col)

                        # Se capturou peça
                        if valid_moves[(row, col)]:
                            board.remove(valid_moves[(row, col)])
                            valid_moves = board.get_valid_moves(selected_piece)
                            valid_moves = {pos: capt for pos, capt in valid_moves.items() if capt}

                            # Se ainda puder capturar continua a jogada
                            if valid_moves:
                                continue

                        # Troca a vez
                        turn = BLACK if turn == WHITE else WHITE
                        selected_piece = None
                        valid_moves = {}
                    else:
                        selected_piece = None
                        valid_moves = {}
                else:
                    # Seleciona peça
                    piece = board.get_piece(row, col)
                    if piece != 0 and piece.color == turn:
                        moves = board.get_valid_moves(piece)
                        if capture_forced:
                            moves = {pos: capt for pos, capt in moves.items() if capt}
                        if moves:
                            selected_piece = piece
                            valid_moves = moves

main(COR_LOCAL)
