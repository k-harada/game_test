import random


class Tile:

    def __init__(self, color, idx=0):
        self.color = color  # black 1, while -1, empty 0
        self.idx = idx
        self.color_str = ""
        self.pic_show = ""
        self.pic = ""
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def update(self):
        if self.color == 1:
            self.color_str = "black"
        elif self.color == -1:
            self.color_str = "white"
        else:
            self.color_str = "empty"
        self.pic_show = f'{self.color_str}.png'
        self.pic = self.color_str + "_" + str(self.idx)

    def __repr__(self):
        return self.pic

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.pic == other.pic


class Board:

    def __init__(self):

        self.line_dict = dict()

        for k in range(64):
            self.line_dict[k] = list()

        # row
        for i in range(8):
            line = [8 * i + j for j in range(8)]
            for j in range(8):
                k = 8 * i + j
                self.line_dict[k].append((line, line.index(k)))

        # col
        for j in range(8):
            line = [8 * i + j for i in range(8)]
            for i in range(8):
                k = 8 * i + j
                self.line_dict[k].append((line, line.index(k)))

                # lu -> rd
        for i in range(6):
            line = [i + 9 * j for j in range(8 - i)]
            for j in range(8 - i):
                k = i + 9 * j
                self.line_dict[k].append((line, line.index(k)))
        for i in range(8, 48, 8):
            line = [i + 9 * j for j in range(8 - (i // 8))]
            for j in range(8 - (i // 8)):
                k = i + 9 * j
                self.line_dict[k].append((line, line.index(k)))

        # ru -> ld
        for i in range(2, 8):
            line = [i + 7 * j for j in range(i + 1)]
            for j in range(i + 1):
                k = i + 7 * j
                self.line_dict[k].append((line, line.index(k)))
        for i in range(15, 55, 8):
            line = [i + 7 * j for j in range(8 - ((i - 7) // 8))]
            for j in range(8 - (i // 8)):
                k = i + 7 * j
                self.line_dict[k].append((line, line.index(k)))

    @staticmethod
    def reverse_line(line, i, black):

        line_new = [k for k in line]
        line_new[i] = black
        res = 0

        # forward
        for j in range(i + 1, len(line_new)):
            if line_new[j] == black:
                for k in range(i + 1, j):
                    line_new[k] = black
                    res += 1
                break
            elif line_new[j] == 0:
                break

        # backward
        for j in range(i - 1, -1, -1):
            if line_new[j] == black:
                for k in range(j + 1, i):
                    line_new[k] = black
                    res += 1
                break
            elif line_new[j] == 0:
                break

        return line_new, res

    def check_line(self, board_64, i, black):

        if board_64[i] != 0:
            return False
        else:
            res_sum = 0
            for line, idx in self.line_dict[i]:
                _, res = self.reverse_line([board_64[l] for l in line], idx, black)
                res_sum += res
            if res_sum > 0:
                return True
            else:
                return False

    def search(self, board_64, black):

        return [i for i in range(64) if self.check_line(board_64, i, black)]

    def play(self, board_64, i, black):

        board_64_new = [k for k in board_64]

        for line, idx in self.line_dict[i]:
            line_new, _ = self.reverse_line([board_64[l] for l in line], idx, black)
            for j in range(len(line)):
                board_64_new[line[j]] = line_new[j]

        return board_64_new


def create_init():
    init_board = [Tile(0, i) for i in range(27)] + [Tile(-1, 27), Tile(1, 28)] + \
                 [Tile(0, i) for i in range(29, 35)] + [Tile(1, 35), Tile(-1, 36)] + \
                 [Tile(0, i) for i in range(37, 64)]
    return init_board


def tile_from_pic(pic):
    color_str, idx_str = pic.split("_")
    if color_str == 'black':
        tile = Tile(1, int(idx_str))
    elif color_str == 'white':
        tile = Tile(-1, int(idx_str))
    else:
        tile = Tile(0, int(idx_str))
    return tile


b = Board()


def create_new_board(board, hand, black=1):

    white = - black
    board_64 = [t.color for t in board]

    # search
    valid_hands = b.search(board_64, black)

    # invalid input
    if len(valid_hands) != 0 and hand.idx not in valid_hands:
        # no change, request re-input
        return board
    # no valid input
    elif len(valid_hands) == 0:
        # pass
        board_64_new = board_64
    else:
        board_64_new = b.play(board_64, hand.idx, black)

    # white
    valid_hands_white = b.search(board_64_new, white)
    if len(valid_hands_white) > 0:
        # to be replaced by AI
        white_idx = random.choice(valid_hands_white)
        board_64_new = b.play(board_64_new, white_idx, white)

    # return
    for i in range(64):
        board[i].set_color(board_64_new[i])

    return board


def judge(board):
    return True


def play(board, hand):

    return None
