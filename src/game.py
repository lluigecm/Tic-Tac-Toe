import os
import pygame
import math


class Game:

    height: int
    width: int
    fps: int
    turn: int

    click: pygame.mouse
    click_status: pygame.mouse
    surface: pygame.Surface
    clock: pygame.time.Clock

    running: bool
    end: bool = False
    count = 0

    def __init__(self, width: int = 600, height: int = 600, fps: int = 60):
        self.width = width
        self.height = height
        self.fps = fps
        self.board: list[list] = [["n", "n", "n"],
                                  ["n", "n", "n"],
                                  ["n", "n", "n"]]

        self.click_status = 0
        self.turn = 1
        pygame.display.set_caption("Tic Tac Toe (Aperta R pra reiniciar, idiota)")
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

    def init_mouse_logic(self):
        self.mouse = pygame.mouse.get_pos()  # pega a posição do mouse
        self.click = pygame.mouse.get_pressed()  # confere se houve clique, e de qual botao do mouse
        self.mouse_logic()  # guardar a ultima posição do clique

    def run(self):
        while self.running:
            self.init_mouse_logic()  #inicia operações com o mouse
            #print(f"{self.click[0]} - ({self.last_mouse_x}, {self.last_mouse_y}") teste pra conferir se os atributos estavam funcionando como esperado
            self.handle_events()
            self.draw_board()  #desenha o tabuleiro

            if self.click[0]:  #não achei outro lugar que encaixasse esse if. Mas, se houve clique, então o click_status recebe 1
                self.click_status = 1
            else:
                self.click_status = 0

            self.draw_in_surface()
            self.pass_to_board()
            # print(self.board)
            if self.is_winner():
                self.count = 1

            pygame.display.flip()
            self.clock.tick(self.fps)

    def handle_events(self):  #confere eventos do game, seja fechar,,vencedor, ou tecla apertada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()

    def draw_board(self):  #desenha o tabuleiro
        self.surface.fill("white")
        pygame.draw.line(self.surface, "black", (1 / 3 * self.width, 0), (1 / 3 * self.width, self.height), 10)
        pygame.draw.line(self.surface, "black", (2 / 3 * self.width, 0), (2 / 3 * self.width, self.height), 10)
        pygame.draw.line(self.surface, "black", (0, 1 / 3 * self.height), (self.width, 1 / 3 * self.height), 10)
        pygame.draw.line(self.surface, "black", (0, 2 / 3 * self.height), (self.width, 2 / 3 * self.height), 10)

    def mouse_logic(self):  #eu reduzo as coordenadas do mouse pra ficar de acordo o tabuleiro, de 0 a 2
        if self.click[0] is False and self.click_status == 1:  #se click[0] é falso, e click_status é verdadeiro, então foi clicado
            self.last_mouse_x = math.ceil(self.mouse[0] /200) - 1
            self.last_mouse_y = math.ceil(self.mouse[1] / 200) - 1
            self.click_status = 0
        elif self.click[0] is False and self.click_status == 0:
            self.last_mouse_x = -1
            self.last_mouse_y = -1

    def draw_in_surface(self):  #confere o que está na board, pra poder desenhar na tela posteriormente
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "x":
                    self.player_x(i, j)
                elif self.board[i][j] == "o":
                    self.player_o(i, j)
                else:
                    pass

    def player_x(self, x, y):  #desenha o x
        pygame.draw.line(self.surface, "red", ((x * 200) + 30, (y * 200) + 30), ((x * 200) + 170, (y * 200) + 170), 10)
        pygame.draw.line(self.surface, "red", ((x * 200) + 170, (y * 200) + 30), ((x * 200) + 30, (y * 200) + 170), 10)

    def player_o(self, x, y):  #desenha a bola
        pygame.draw.circle(self.surface, "blue", ((x * 200) + 100, (y * 200) + 100), 75, 10)

    def pass_to_board(self):  #passa os X e as O para a board
        if -1 != self.last_mouse_x < 3 and -1 != self.last_mouse_y < 3:  #se as coordenadas estiverem denrtro do range da board
            if self.turn == 1 and self.board[self.last_mouse_x][self.last_mouse_y] == "n" and self.end == 0:  #se o espaço da board estiver vazio, for a vez de x, e não for fim de jogo
                self.board[self.last_mouse_x][self.last_mouse_y] = "x"
                self.turn = 2
            if self.turn == 2 and self.board[self.last_mouse_x][self.last_mouse_y] == "n" and self.end == 0:  #se o espaço da board tiver vazio, for a vez de o, e não for fim de jogo
                self.board[self.last_mouse_x][self.last_mouse_y] = "o"
                self.turn = 1

    def restart(self):  #restarta o game
        self.board =  [["n", "n", "n"],
                       ["n", "n", "n"],
                       ["n", "n", "n"]]
        self.turn = 1
        self.end = False
        self.count = 0
        os.system("cls")

    def is_winner(self):  #confere se há vencedor
        if (self.board[0][0] == "x" and self.board[0][1] == "x" and self.board[0][2] == "x") or \
            (self.board[1][0] == "x" and self.board[1][1] == "x" and self.board[1][2] == "x") or \
             (self.board[2][0] == "x" and self.board[2][1] == "x" and self.board[2][2] == "x"): #confere linhas para x
            if self.count == 0:
                print("X Win")
            self.end = True
            return True
        if (self.board[0][0] == "x" and self.board[1][0] == "x" and self.board[2][0] == "x") or \
              (self.board[0][1] == "x" and self.board[1][1] == "x" and self.board[2][1] == "x") or \
               (self.board[0][2] == "x" and self.board[1][2] == "x" and self.board[2][2] == "x"): #confere colunas para x
            if self.count == 0:
                print("X Win")
            self.end = True
            return True
        if (self.board[0][0] == "x" and self.board[1][1] == "x" and self.board[2][2] == "x") or \
              (self.board[0][2] == "x" and self.board[1][1] == "x" and self.board[2][0] == "x"): # confere diagonais para x
            if self.count == 0:
                print("X Win")
            self.end = True
            return True
        if (self.board[0][0] == "o" and self.board[0][1] == "o" and self.board[0][2] == "o") or \
            (self.board[1][0] == "o" and self.board[1][1] == "o" and self.board[1][2] == "o") or \
             (self.board[2][0] == "o" and self.board[2][1] == "o" and self.board[2][2] == "o"): #confere linhas para o
            if self.count == 0:
                print("O Win")
            self.end = True
            return True
        if (self.board[0][0] == "o" and self.board[1][0] == "o" and self.board[2][0] == "o") or \
              (self.board[0][1] == "o" and self.board[1][1] == "o" and self.board[2][1] == "o") or \
               (self.board[0][2] == "o" and self.board[1][2] == "o" and self.board[2][2] == "o"): #confere colunas para o
            if self.count == 0:
                print("O Win")
            self.end = True
            return True
        if (self.board[0][0] == "o" and self.board[1][1] == "o" and self.board[2][2] == "o") or \
              (self.board[0][2] == "o" and self.board[1][1] == "o" and self.board[2][0] == "o"): # confere diagonais para o
            if self.count == 0:
                print("O Win")
            self.end = True
            return True

        if self.is_tie():
            if self.count == 0:
                print("It's a tie")
            self.end = True
            return True

        return False

    def is_tie(self):  #confere se houve empate
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != "n":
                    count += 1

        if count == 9:
            return True
        else:
            return False
