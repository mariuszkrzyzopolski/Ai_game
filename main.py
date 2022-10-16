# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax


class SixMensMorris(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.player_1_pieces, self.player_2_pieces = 6, 6
        self.board = [0 for i in range(16)]
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        print(self.possible_moves())
        print([self.player_1_pieces, self.player_2_pieces])
        self.board[int(move) - 1] = self.current_player
        self.pound()

    def pound(self):
        mill = any(
            [
                all([(self.board[c - 1] == self.opponent_index) for c in line])
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
            if self.current_player == 1:
                self.player_1_pieces = self.player_1_pieces - 1
            else:
                self.player_2_pieces = self.player_2_pieces - 1
            print(f"{self.player_1_pieces} {self.player_2_pieces}")

    def lose(self):
        if self.player_1_pieces < 3 or self.player_2_pieces < 3:
            return True

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def show(self):
        print(self.board)

    def scoring(self):
        return -100 if self.lose() else 0


if __name__ == "__main__":

    ai_algo = Negamax(6)
    SixMensMorris([Human_Player(), AI_Player(ai_algo)]).play()
