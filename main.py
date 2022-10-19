# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import random


class SixMensMorris(TwoPlayerGame):
    """
    :authors: s21544 Mariusz Krzyżopolski s20499 Tomasz Baj
    Link to the rules: https://en.wikipedia.org/wiki/Nine_men%27s_morris

    This is simpler version of the game Nine_men_morris
    To run the game please install easyai ~2.0.12 with dependencies and run main.py
    """

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

    def possible_moves(self) -> list:
        """
        function generate possible movements for each players, on every turn, until no move lefts or any player reach
        win condition

        :return: list with indexes where players can still move
        """
        if self.nmove <= 12:
            return [i + 1 for i, e in enumerate(self.board) if e == 0]
        else:
            return [v for key in self.get_player_pieces_indexes(self.current_player) if key in self.board_connections
                    for v in self.board_connections[key]]

    def make_move(self, move: int) -> None:
        """
        Function add pieces to the board, passing movement to check if there beat on the board, and after 12 move
        manage the movement on the board, not add another pieces

        :param move: integer with field to move
        """
        move_index = int(move) - 1
        self.board[move_index] = self.current_player
        self.beat(move_index)
        if self.nmove > 12:
            for key, value in self.board_connections.items():
                if 6 in value:
                    piece_to_move = self.board_connections[key][0]
            self.board[piece_to_move] = 0

    def mill(self, move: int) -> bool:
        """
        Function check if there is a mill on the board, according to lines and newest movement

        :param move: integer with field to move
        :return: Boolean
        """
        lines = [[0, 1, 2],
                 [3, 4, 5],
                 [10, 11, 12],
                 [13, 14, 15],
                 [0, 6, 13],
                 [3, 7, 10],
                 [5, 8, 12],
                 [2, 9, 15]
                 ]

        for line in lines:
            if move in line and self.board[line[0]] == self.board[line[1]] == self.board[
                line[2]] == self.current_player:
                return True

        return False

    def get_player_pieces_indexes(self, player: int) -> list:
        """
        Function filter through all pieces on the board, return only pieces of target player

        :param player: integer with id of player (1 or 2)
        :return: list of pieces on the board, belonged to target player
        """
        return [i for i in range(len(self.board)) if self.board[i] == player]

    def beat(self, move: int) -> None:
        """
        Function take off random enemy piece, if new mill is on the board

        :param move: integer with field to move
        :return:
        """
        if self.mill(move):
            # player cannot be prompted because AI learn at both conditionals
            enemy_pieces_index = self.get_player_pieces_indexes(self.opponent_index)
            if self.current_player == 1:
                self.player_2_pieces = self.player_2_pieces - 1
                self.board[random.choice(enemy_pieces_index)] = 0
            else:
                self.player_1_pieces = self.player_1_pieces - 1
                self.board[random.choice(enemy_pieces_index)] = 0

    def lose(self) -> bool:
        """
        Function checks if any player has less than 3 pieces

        :return:
        """
        if self.player_1_pieces < 3 or self.player_2_pieces < 3:
            return True

    def is_over(self) -> bool:
        """
        Checking if any lose/win condition was achieved

        :return:
        """
        return (self.possible_moves() == []) or self.lose()

    def show(self) -> None:
        """
        Print board for every turn of play

        :return:
        """
        if self.current_player == 2 or self.nmove == 0:
            print([self.player_1_pieces, self.player_2_pieces])
            print(str(self.board[0]) + 5 * "-" + str(self.board[1]) + 5 * "-" + str(self.board[2]))
            print("|" + 5 * " " + "|" + 5 * " " + "|")
            print("|  " + str(self.board[3]) + "--" + str(self.board[4]) + "--" + str(self.board[5]) + "  |")
            print("|  |     |  |")
            print(str(self.board[6]) + "--" + str(self.board[7]) + 5 * " " + str(self.board[8]) + "--" + str(
                self.board[9]))
            print("|  |     |  |")
            print("|  " + str(self.board[10]) + "--" + str(self.board[11]) + "--" + str(self.board[12]) + "  |")
            print("|" + 5 * " " + "|" + 5 * " " + "|")
            print(str(self.board[13]) + 5 * "-" + str(self.board[14]) + 5 * "-" + str(self.board[15]))

    def scoring(self):
        return -100 if self.lose() else 0


def print_help() -> None:
    """
    Print help with numbered board

    :return:
    """
    print(str(1) + 5 * "-" + str(2) + 5 * "-" + str(3))
    print("|" + 5 * " " + "|" + 5 * " " + "|")
    print("|  " + str(4) + "--" + str(5) + "--" + str(6) + "  |")
    print("|  |     |  |")
    print(str(7) + "--" + str(8) + 5 * " " + str(9) + "--" + str(10))
    print("|  |     |  |")
    print("|  " + str(11) + "-" + str(12) + "-" + str(13) + " |")
    print("|" + 5 * " " + "|" + 5 * " " + "|")
    print(str(14) + 4 * "-" + str(15) + 4 * "-" + str(16))


if __name__ == "__main__":
    print_help()
    ai_algo = Negamax(6)
    SixMensMorris([Human_Player(), AI_Player(ai_algo)]).play()
