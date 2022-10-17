# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import random


class SixMensMorris(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.player_1_pieces, self.player_2_pieces = 6, 6
        self.board = [0 for i in range(16)]
        self.current_player = 1  # player 1 starts.
        self.board_connections = {0: [1, 6], 1: [0, 4, 2], 2: [1, 9], 3: [4, 7], 4: [3, 1, 5], 5: [4, 8],
                                  6: [0, 7, 13], 7: [3, 6, 10], 8: [5, 9, 12], 9: [2, 8, 15],
                                  10: [7, 11], 11: [10, 12, 14], 12: [8, 11], 13: [6, 14], 14: [11, 13, 15],
                                  15: [9, 14]}
        self.nmove = 0

    def possible_moves(self):
        if self.nmove >= 12:
            return [v for key in self.get_player_pieces_indexes(self.current_player) if key in self.board_connections
                    for v in self.board_connections[key]]
        else:
            return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.current_player
        self.pound(move)
        if self.nmove >= 12:
            # TODO take off nearby piece to move it
            pass

    def get_player_pieces_indexes(self, player):
        return [i for i in range(len(self.board)) if self.board[i] == player]

    def pound(self, move):
        # mill in place that player made move
        mill = any(
            [
                all([(self.board[c - 1] == self.current_player) for c in line])
                for line in [
                [1, 2, 3],
                [4, 5, 6],
                [11, 12, 13],
                [14, 15, 16],
                [1, 7, 14],
                [4, 8, 11],
                [6, 9, 13],
                [3, 10, 16],
            ]
            ]
        )
        if mill:
            # player cannot be prompted because AI learn at both conditionals
            enemy_pieces_index = self.get_player_pieces_indexes(self.opponent_index)
            if self.current_player == 1:
                self.player_2_pieces = self.player_2_pieces - 1
                self.board[random.choice(enemy_pieces_index)] = 0
            else:
                self.player_1_pieces = self.player_1_pieces - 1
                self.board[random.choice(enemy_pieces_index)] = 0

    def lose(self):
        if self.player_1_pieces < 3 or self.player_2_pieces < 3:
            return True

    def is_over(self):
        # TODO winner message?
        return (self.possible_moves() == []) or self.lose()

    def show(self):
        print(self.nmove)
        print([i for i in range(len(self.board)) if self.board[i] == 2])
        print([self.player_1_pieces, self.player_2_pieces])
        print(str(self.board[0]) + 3 * "-" + str(self.board[1]) + 3 * "-" + str(self.board[2]))
        print("|" + 3 * " " + "|" + 3 * " " + "|")
        print("| " + str(self.board[3]) + "-" + str(self.board[4]) + "-" + str(self.board[5]) + " |")
        print("| |   | |")
        print(str(self.board[6]) + "-" + str(self.board[7]) + 3 * " " + str(self.board[8]) + "-" + str(self.board[9]))
        print("| |   | |")
        print("| " + str(self.board[10]) + "-" + str(self.board[11]) + "-" + str(self.board[12]) + " |")
        print("|" + 3 * " " + "|" + 3 * " " + "|")
        print(str(self.board[13]) + 3 * "-" + str(self.board[14]) + 3 * "-" + str(self.board[15]))

    def scoring(self):
        return -100 if self.lose() else 0


if __name__ == "__main__":
    ai_algo = Negamax(6)
    SixMensMorris([Human_Player(), AI_Player(ai_algo)]).play()
