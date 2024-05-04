import random

class CheckersGame:
    def __init__(self, player_mode):
        self.gameBoard = [[' ', 'r', ' ', 'r', ' ', 'r', ' ', 'r'],
                          ['r', ' ', 'r', ' ', 'r', ' ', 'r', ' '],
                          [' ', 'r', ' ', 'r', ' ', 'r', ' ', 'r'],
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
                          [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
                          ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' ']]
        self.current_player = 'r'
        self.player_mode = player_mode

        while self.player_mode not in ['1', '2']:
            print("Invalid option selected.")
            self.player_mode = input("Please select again (1 for human vs human, 2 for human vs AI): ")

        if self.player_mode == '1':
            print("'r' represents Human 1, and 'b' represents Human 2.")
        elif self.player_mode == '2':
            print("'r' represents Human, and 'b' represents AI.")

    def print_gameBoard(self):
        print("   0   1   2   3   4   5   6   7")
        print("  ------------------------------")
        for i in range(8):
            print(f"{i} | {' | '.join(self.gameBoard[i])} |")
            print("  ------------------------------")

    def is_move_valid(self, start, end):
        row_start, column_start = start
        row_end, column_end = end

        # Check if start and end positions are valid
        if not (0 <= row_start < 8 and 0 <= column_start < 8 and 0 <= row_end < 8 and 0 <= column_end < 8):
            return False

        # Check if the end position is empty
        if self.gameBoard[row_end][column_end] != ' ':
            return False

        # Check if the move is diagonal and within one or two spaces
        if abs(row_end - row_start) != 1 and abs(row_end - row_start) != 2:
            return False
        if abs(column_end - column_start) != 1 and abs(column_end - column_start) != 2:
            return False

        # Check if the player is moving their own piece
        if self.current_player == 'r' and self.gameBoard[row_start][column_start] not in ['r', 'R']:
            return False
        elif self.current_player == 'b' and self.gameBoard[row_start][column_start] not in ['b', 'B']:
            return False

        # Check if the move captures an opponent's piece
        if abs(row_end - row_start) == 1:
            return True  # Normal move
        elif abs(row_end - row_start) == 2:
            row_captured = (row_start + row_end) // 2
            column_captured = (column_start + column_end) // 2
            if self.gameBoard[row_captured][column_captured] in ['r', 'R', 'b', 'B']:
                return True  # Capture move
            else:
                return False


    def make_move(self, start, end):
        row_start, column_start = start
        row_end, column_end = end

        # Make the move on the gameBoard
        self.gameBoard[row_end][column_end] = self.gameBoard[row_start][column_start]
        self.gameBoard[row_start][column_start] = ' '

        # Check if this move captured an opponent's piece
        if abs(row_end - row_start) == 2:
            row_captured = (row_start + row_end) // 2
            column_captured = (column_start + column_end) // 2
            self.gameBoard[row_captured][column_captured] = ' '

    def switch_player(self):
        # Switch to the next player
        self.current_player = 'b' if self.current_player == 'r' else 'r'

    def ai_make_move(self):
        possible_moves = self.generate_possible_moves()
        if possible_moves:
            jump_moves = [move for move in possible_moves if self.is_diagonal_jump(move)]
            if jump_moves:
                move = random.choice(jump_moves)
            else:
                move = random.choice(possible_moves)

            while not self.is_move_valid(move[0], move[1]):
                if jump_moves:
                    move = random.choice(jump_moves)
                else:
                    move = random.choice(possible_moves)

            self.make_move(move[0], move[1])
            self.switch_player()


    def is_diagonal_jump(self, move):
        start, end = move
        row_start, col_start = start
        row_end, col_end = end
        row_captured = (row_start + row_end) // 2
        col_captured = (col_start + col_end) // 2
        return (
            0 <= row_captured < 8 and
            0 <= col_captured < 8 and
            self.gameBoard[row_captured][col_captured] in ['r', 'R'] and
            abs(row_end - row_start) == 2  # Check if it's a jump move
        )

    def generate_possible_moves(self):
        possible_moves = []
        for row in range(8):
            for col in range(8):
                if self.gameBoard[row][col] == 'b' or self.gameBoard[row][col] == 'B':
                    for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        if 0 <= row + i < 8 and 0 <= col + j < 8:
                            if self.gameBoard[row + i][col + j] == ' ':
                                possible_moves.append(((row, col), (row + i, col + j)))
                            elif self.gameBoard[row + i][col + j] == 'r' or self.gameBoard[row + i][col + j] == 'R':
                                if 0 <= row + 2*i < 8 and 0 <= col + 2*j < 8:
                                    if self.gameBoard[row + 2*i][col + 2*j] == ' ':
                                        possible_moves.append(((row, col), (row + 2*i, col + 2*j)))
        return possible_moves
    
    def monte_carlo_simulation(self, possible_moves, simulations=1000):
        scores = {}
        for move in possible_moves:
            scores[move] = 0

        for _ in range(simulations):
            for move in possible_moves:
                temp_game = CheckersGame('1')  # Create a temporary game instance
                temp_game.gameBoard = [row[:] for row in self.gameBoard]  # Copy current game board
                temp_game.current_player = self.current_player  # Set current player

                temp_game.make_move(move[0], move[1])  # Simulate move
                while True:
                    temp_game.switch_player()  # Switch player
                    temp_possible_moves = temp_game.generate_possible_moves()  # Get possible moves

                    # Check for jump moves if AI's turn
                    if temp_game.current_player == 'b':
                        jump_moves = [temp_move for temp_move in temp_possible_moves if temp_game.is_diagonal_jump(temp_move)]
                        if jump_moves:
                            temp_move = random.choice(jump_moves)
                        else:
                            temp_move = random.choice(temp_possible_moves)
                    else:
                        temp_move = random.choice(temp_possible_moves)  # Choose random move

                    temp_game.make_move(temp_move[0], temp_move[1])  # Simulate move

                    if not temp_possible_moves:
                        break

                # Evaluate game outcome and update scores
                if temp_game.current_player == 'b':  # AI wins
                    scores[move] += 1
                elif temp_game.current_player == 'r':  # Human wins
                    scores[move] -= 1

        # Choose the move with the highest score
        best_move = max(scores, key=scores.get)
        return best_move

# Example usage
player_mode = input("Select player mode (human vs human - '1', human vs AI - '2'): ")
game = CheckersGame(player_mode)

while True:
    game.print_gameBoard()

    if game.player_mode == '1' and game.current_player == 'r':
        print("Human 1 turn (r)")
        start_str = input("Enter the coordinates of the piece you want to move (row col): ")
        end_str = input("Enter the coordinates of the destination (row col): ")
        start = tuple(map(int, start_str.split()))
        end = tuple(map(int, end_str.split()))

        if game.is_move_valid(start, end):
            game.make_move(start, end)
            game.switch_player()
        else:
            print("Invalid move! Try again.")

    elif game.player_mode == '1' and game.current_player == 'b':
        print("Human 2 turn (b)")
        start_str = input("Enter the coordinates of the piece you want to move (row col): ")
        end_str = input("Enter the coordinates of the destination (row col): ")
        start = tuple(map(int, start_str.split()))
        end = tuple(map(int, end_str.split()))

        if game.is_move_valid(start, end):
            game.make_move(start, end)
            game.switch_player()
        else:
            print("Invalid move! Try again.")

    elif game.player_mode == '2' and game.current_player == 'r':
        print("Human's turn (r)")
        start_str = input("Enter the coordinates of the piece you want to move (row col): ")
        end_str = input("Enter the coordinates of the destination (row col): ")
        start = tuple(map(int, start_str.split()))
        end = tuple(map(int, end_str.split()))

        if game.is_move_valid(start, end):
            game.make_move(start, end)
            game.switch_player()
        else:
            print("Invalid move! Try again.")
    else:
        print("AI's turn (b)")
        game.ai_make_move()