import copy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import random

class Board(GridLayout):
    def __init__(self):
        GridLayout.__init__(self)
        self.board = list()
        self.cols = 3
        self.turn = 1
        self.isdraw = 0
        for i in range(self.cols**2):
            self.board.append(Button())
            self.board[i].bind(on_press=self.click)
            self.add_widget(self.board[i])


    def click(self, touch):
        board = self.convert()
        if touch.text == "":
            self.isdraw += 1
            if self.turn == 1:
                touch.font_size = 250
                touch.text = "X"
                self.turn = 0
                board = self.convert()
                if Board.isover(board) == -1:
                    if self.isdraw != 9:
                        if self.turn == 0:
                            self.isdraw += 1
                            i = Board.minimax(board, 9)
                            i = i[1]
                            self.board[i].font_size = 250
                            self.board[i].text = "O"
                            self.turn = 1
                            board = self.convert()
                            if self.isover(board) == 1:
                                self.clear_widgets()
                                self.add_widget(Label(text="X WON", font_size="100sp"))
                            if self.isover(board) == 0:
                                self.clear_widgets()
                                self.add_widget(Label(text="O WON", font_size="100sp"))
                            if self.isover(board) == 2:
                                self.clear_widgets()
                                self.add_widget(Label(text="IT A DRAW", font_size="100sp"))
                else:
                    if self.isover(board) == 1:
                        self.clear_widgets()
                        self.add_widget(Label(text="X WON", font_size="100sp"))
                    if self.isover(board) == 0:
                        self.clear_widgets()
                        self.add_widget(Label(text="O WON", font_size="100sp"))
                    if self.isover(board) == 2:
                        self.clear_widgets()
                        self.add_widget(Label(text="IT'S A DRAW", font_size="100sp"))

    def convert(self):
        board = list()
        for i in self.board:
            if i.text == "X":
                board.append(1)
            if i.text == "O":
                board.append(0)
            if i.text == "":
                board.append(-1)
        return board
    @staticmethod
    def pointsboard(board):
        sum = 0
        if Board.isover(board) == 1:
            return -1000
        elif Board.isover(board) == 0:
            return 1000
        elif Board.isover(board) == 2:
            return 0
        counter1, counter0, counter = 0, 0, 0
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i+i+i+j] == 1:
                    counter1 += 1
                elif board[i+i+i+j] == 0:
                    counter0 += 1
                else:
                    counter += 1
            if counter0 ==2 and counter == 1:
                sum += 100
            elif counter1 == 2 and counter ==1:
                sum += -300
    @staticmethod
    def isover(board):
        x = 0
        y = 0
        for i in range(0, 3):
            if board[x] == 1 and board[x+1] == 1 and board[x+2] == 1:
                return 1
            if board[y] == 1 and board[y + 3] == 1 and board[y + 6] == 1:
                return 1
            if board[0] == 1 and board[4] == 1 and board[8] == 1:
                return 1
            if board[2] == 1 and board[4] == 1 and board[6] == 1:
                return 1
            if board[x] == 0 and board[x + 1] == 0 and board[x + 2] == 0:
                return 0
            if board[y] == 0 and board[y + 3] == 0 and board[y + 6] == 0:
                return 0
            if board[0] == 0 and board[4] == 0 and board[8] == 0:
                return 0
            if board[2] == 0 and board[4] == 0 and board[6] == 0:
                return 0
            x += 3
            y += 1
        if board.count(-1) == 0:
            return 2
        return -1

    @staticmethod
    def nextboard(board, turn):
        board1 = copy.deepcopy(board)
        counter = 0
        option = list()
        options = list()
        for i in board1:
            if i != 1 and i != 0:
                board1[counter] = turn
                option.append(board1)
                option.append(counter)
                options.append(option)
                option = []
                board1 = copy.deepcopy(board)
            counter += 1
        return options

    @staticmethod
    def minimax(game_state, depth):
        moves = Board.nextboard(game_state, 0)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            score = Board.min_play(move, depth - 1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    @staticmethod
    def min_play(game_state, depth):
        if depth == 0 or Board.isover(game_state[0]) == 0 or game_state[0].count(-1) == 0 or Board.isover(game_state[0]) == 1:
            return Board.pointsboard(game_state[0])
        moves = Board.nextboard(game_state[0], 1)
        best_score = float('inf')
        best_move = moves[0]
        for move in moves:
            score = Board.max_play(move, depth - 1)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    @staticmethod
    def max_play(game_state, depth):
        if depth == 0 or Board.isover(game_state[0]) == 1 or game_state[0].count(-1) == 0 or Board.isover(game_state[0]) == 0:
            return Board.pointsboard(game_state[0])
        moves = Board.nextboard(game_state[0], 0)
        best_score = float('-inf')
        best_move = moves[0]
        for move in moves:
            score = Board.min_play(move, depth - 1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score


class TestApp(App):
    def build(self):
        self.title = 'Tic Tac Toc'
        return Board()
TestApp().run()