# write your code here
import random
import sys

# THis code is a big mess. I was in a hurry after stage 4 and wrote many ugly lines of code.


class Field:

    def __init__(self):
        self.content = {"1 1": " ", "1 2": " ", "1 3": " ",
                        "2 1": " ", "2 2": " ", "2 3": " ",
                        "3 1": " ", "3 2": " ", "3 3": " "}

    win_conditions = [["1 1", "1 2", "1 3"], ["2 1", "2 2", "2 3"], ["3 1", "3 2", "3 3"],
                      ["1 1", "2 1", "3 1"], ["1 2", "2 2", "3 2"], ["1 3", "2 3", "3 3"],
                      ["1 1", "2 2", "3 3"], ["3 1", "2 2", "1 3"]]

    def print_raster(self):
        print("---------")
        print("|", self.content["1 1"], self.content["1 2"], self.content["1 3"], "|")
        print("|", self.content["2 1"], self.content["2 2"], self.content["2 3"], "|")
        print("|", self.content["3 1"], self.content["3 2"], self.content["3 3"], "|")
        print("---------")

    def reset(self):
        self.content = {key: " " for key in self.content}

    def field_array(self):
        return [[self.content["1 1"], self.content["1 2"], self.content["1 3"]],
                [self.content["2 1"], self.content["2 2"], self.content["2 3"]],
                [self.content["3 1"], self.content["3 2"], self.content["3 3"]]]

    def check_win(self, field, first, second, third):
        if field[first] == field[second] == field[third]:
            if not field[first] == " ":
                return field[first]

    def check_for_win(self, field):
        for condition in self.win_conditions:
            if self.check_win(field, *condition):
                return self.content.get(condition[0])

    def empty_indexes(self):
        return [key for key in self.content if self.content[key] == " "]

    def check_for_opportunity(self, first, second, third, mark):
        print('Counting " "')
        check_dic = {first: self.content[first], second: self.content[second], third: self.content[third]}
        print("Checklist:", check_dic)
        if list(check_dic.values()).count(" ") >= 2:
            print('found 2 or 3 " ", returning')
            return False
        case = []
        if self.content[second] == self.content[third] and self.content[first] == " ":
            case.append(self.content[second])
            print(case)
        else:
            case.append("No")
        if self.content[first] == self.content[third] and self.content[second] == " ":
            case.append(self.content[first])
            print(case)
        else:
            case.append("No")
        if self.content[first] == self.content[second] and self.content[third] == " ":
            case.append(self.content[first])
            print(case)
        else:
            case.append("No")
        print(case)
        if case.count("No") == 3:
            return False
        elif mark in case:
            print("own mark found")
            return mark, list(check_dic.keys())[list(check_dic.values()).index(" ")]
        else:
            if "X" in case:
                print("X mark found")
                return "X", list(check_dic.keys())[list(check_dic.values()).index(" ")]
            else:
                print("O mark found")
                return "O", list(check_dic.keys())[list(check_dic.values()).index(" ")]

    def get_game_status(self, field):
        winstate = self.check_for_win(field)
        if not winstate:
            if any(" " in v for v in field.values()):
                return False, "in progress"
            else:
                # print("Draw detected.")
                return True, "Draw"
        else:
            return True, winstate


class Player:
    def __init__(self, mark):
        self.mark = mark

    def insert_mark(self, x, y, field):
        field.content[f"{x} {y}"] = self.mark

    def turn(self, field):
        pass


class Human(Player):

    def turn(self, field):
        user_coordinate = input("Enter the coordinates: ")
        str_list = user_coordinate.split()
        if not len(str_list) == 2:
            print("You should enter numbers!")
            self.turn(field)
            return
        if not (str_list[0].isdigit() and str_list[1].isdigit()):
            print("You should enter numbers!")
            self.turn(field)
            return
        x = int(str_list[0])
        y = int(str_list[1])
        if not (1 <= x <= 3 and 1 <= y <= 3):
            print("Coordinates should be from 1 to 3!")
            self.turn(field)
            return
        if field.content[f"{x} {y}"] != " ":
            print("This cell is occupied! Choose another one!")
            self.turn(field)
            return
        self.insert_mark(x, y, field)


class AI(Player):
    level = None

    def print_move_plan(self):
        print('Making move level "' + self.level + '"')

    def random_mark(self, field):
        mark_inserted = False
        while not mark_inserted:
            x_rand = random.randint(1, 3)
            y_rand = random.randint(1, 3)
            if not field.content[f"{x_rand} {y_rand}"] == " ":
                continue
            mark_inserted = True
            self.insert_mark(x_rand, y_rand, field)


class EasyAI(AI):

    def __init__(self, mark):
        super().__init__(mark)
        self.level = "easy"

    def turn(self, field):
        self.print_move_plan()
        self.random_mark(field)


class MediumAI(AI):
    def __init__(self, mark):
        super().__init__(mark)
        self.level = "medium"

    def turn(self, field):
        self.print_move_plan()
        result_list = []
        for condition in field.win_conditions:
            result = field.check_for_opportunity(*condition, self.mark)
            if result is False:
                continue
            result_list.append(result)
            # self.insert_mark(int(condition[result][0]), int(condition[result][2]), field)
        print(result_list)
        if not result_list:
            print("Random move...")
            self.random_mark(field)
            return
        for tp in result_list:
            if tp[0] == self.mark:
                print("own-mark-to-win")
                self.insert_mark(int(tp[1][0]), int(tp[1][2]), field)
                return
        print("mark against the enemy")
        self.insert_mark(int(result_list[0][1][0]), int(result_list[0][1][2]), field)


class HardAI(AI):
    def __init__(self, mark):
        super().__init__(mark)
        self.level = "hard"
        if self.mark == "X":
            self.enemy_mark = "O"
        else:
            self.enemy_mark = "X"
        self.scores = {
            self.mark: 10,
            self.enemy_mark: -10,
            "Draw": 0
        }

    def minimax(self, board, depth, is_maximising):
        mm_field = Field()
        mm_field.content["1 1"] = board[0][0]
        mm_field.content["1 2"] = board[0][1]
        mm_field.content["1 3"] = board[0][2]
        mm_field.content["2 1"] = board[1][0]
        mm_field.content["2 2"] = board[1][1]
        mm_field.content["2 3"] = board[1][2]
        mm_field.content["3 1"] = board[2][0]
        mm_field.content["3 2"] = board[2][1]
        mm_field.content["3 3"] = board[2][2]

        result = mm_field.get_game_status(mm_field.content)
        if result[0]:
            # print("returning", self.scores[result[1]])
            return self.scores[result[1]]

        if is_maximising:
            best_score = -100
            for i in range(0, 3):
                for j in range(0, 3):
                    # is the spot available?
                    if board[i][j] == " ":
                        board[i][j] = self.mark
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 100
            for i in range(0, 3):
                for j in range(0, 3):
                    # is the spot available?
                    if board[i][j] == " ":
                        board[i][j] = self.enemy_mark
                        # print("false board", board)
                        score = self.minimax(board, depth + 1, True)
                        # print("false score", score)
                        board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def turn(self, true_field):
        board = true_field.field_array()
        best_score = -100
        best_move = None
        for i in range(0, 3):
            for j in range(0, 3):
                # is the spot available?
                if board[i][j] == " ":
                    board[i][j] = self.mark
                    score = self.minimax(board, 0, False)
                    board[i][j] = " "
                    # print(score)
                    if score > best_score:
                        best_score = score
                        # print(score)
                        # print("changing move")
                        best_move = (i, j)
        # print(board)
        # print(best_move)
        board[best_move[0]][best_move[1]] = self.mark
        # print(board)
        true_field.content[f"{best_move[0] + 1} {best_move[1] + 1}"] = self.mark


class TicTacToe:

    field = Field()

    def setup(self, first, second):
        if first == "user":
            player1 = Human("X")
        elif first == "easy":
            player1 = EasyAI("X")
        elif first == "medium":
            player1 = MediumAI("X")
        else:
            player1 = HardAI("X")

        if second == "user":
            player2 = Human("O")
        elif second == "easy":
            player2 = EasyAI("O")
        elif second == "medium":
            player2 = MediumAI("O")
        else:
            player2 = HardAI("O")

        return player1, player2

    def play(self, first, second):
        # first setup empty raster and print it
        self.field.print_raster()
        players = self.setup(first, second)
        p1 = players[0]
        p2 = players[1]
        game_in_progress = True
        while game_in_progress:
            p1.turn(self.field)
            self.field.print_raster()
            if self.field.get_game_status(self.field.content)[0]:
                break
            p2.turn(self.field)
            self.field.print_raster()
            if self.field.get_game_status(self.field.content)[0]:
                break
        mark = self.field.get_game_status(self.field.content)[1]
        if mark == "Draw":
            print("Draw")
        else:
            print(f"{mark} wins")
        print()

    def main_menu(self):
        input_command = input("Input command: ")
        if input_command == "exit":
            sys.exit()
        ic_list = input_command.split()
        if len(ic_list) == 3:
            if not (ic_list[0] == "start"
                    and ic_list[1] in ("user", "easy", "medium", "hard")
                    and ic_list[2] in ("user", "easy", "medium", "hard")):
                print("Bad parameters!")
                self.main_menu()
            # print("success")
        else:
            print("Bad parameters!")
            self.main_menu()
        self.play(ic_list[1], ic_list[2])
        self.field.reset()
        self.main_menu()


game = TicTacToe()
game.main_menu()
