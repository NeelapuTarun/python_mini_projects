# X and O game:

import turtle

# Screen setup
wn = turtle.Screen()
wn.title("XO Game with AI")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Constants
GRID_SIZE = 500
CELL_SIZE = GRID_SIZE / 3
TOP_LEFT_X = -GRID_SIZE / 2
TOP_LEFT_Y = GRID_SIZE / 2

# Grid drawer
grid_drawer = turtle.Turtle()
grid_drawer.color("cyan")
grid_drawer.pensize(4)
grid_drawer.hideturtle()
grid_drawer.speed(0)

def draw_grid():
    grid_drawer.clear()
    for i in range(1, 3):
        x = TOP_LEFT_X + i * CELL_SIZE
        grid_drawer.penup()
        grid_drawer.goto(x, TOP_LEFT_Y)
        grid_drawer.pendown()
        grid_drawer.goto(x, TOP_LEFT_Y - GRID_SIZE)
    for i in range(1, 3):
        y = TOP_LEFT_Y - i * CELL_SIZE
        grid_drawer.penup()
        grid_drawer.goto(TOP_LEFT_X, y)
        grid_drawer.pendown()
        grid_drawer.goto(TOP_LEFT_X + GRID_SIZE, y)
    grid_drawer.penup()
    grid_drawer.goto(TOP_LEFT_X, TOP_LEFT_Y)
    grid_drawer.pendown()
    for _ in range(4):
        grid_drawer.forward(GRID_SIZE)
        grid_drawer.right(90)

draw_grid()

# Score variables (only player and opponent)
player_score = 0
ai_score = 0

# Game state
game_over = False

# Scoreboard writer (only two scores)
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.color("green")
score_writer.goto(0, 270)

def update_scoreboard():
    score_writer.clear()
    score_text = f"Player X: {player_score}   AI O: {ai_score}"
    score_writer.write(score_text, align="center", font=("Courier", 18, "bold"))

# Symbol drawer
symbol_drawer = turtle.Turtle()
symbol_drawer.hideturtle()
symbol_drawer.penup()
symbol_drawer.speed(0)

# Winning line drawer
line_drawer = turtle.Turtle()
line_drawer.hideturtle()
line_drawer.pensize(6)
line_drawer.color("deeppink")

# Game board
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

def draw_symbol(player, row, col):
    x = TOP_LEFT_X + col * CELL_SIZE + CELL_SIZE / 2
    y = TOP_LEFT_Y - row * CELL_SIZE - CELL_SIZE / 2
    # slightly lower for better visual centering
    y_offset = -75 if player == "X" else -80
    symbol_drawer.goto(x, y + y_offset)
    symbol_drawer.color("lime" if player == "X" else "deeppink")
    symbol_drawer.write(player, align="center", font=("Arial", 110, "bold"))

def draw_board():
    symbol_drawer.clear()
    for r in range(3):
        for c in range(3):
            if board[r][c] != "":
                draw_symbol(board[r][c], r, c)

def highlight_win(cells):
    line_drawer.clear()
    r1, c1 = cells[0]
    r2, c2 = cells[2]
    x1 = TOP_LEFT_X + c1 * CELL_SIZE + CELL_SIZE / 2
    y1 = TOP_LEFT_Y - r1 * CELL_SIZE - CELL_SIZE / 2
    x2 = TOP_LEFT_X + c2 * CELL_SIZE + CELL_SIZE / 2
    y2 = TOP_LEFT_Y - r2 * CELL_SIZE - CELL_SIZE / 2

    line_drawer.penup()
    line_drawer.goto(x1, y1)
    line_drawer.pendown()

    steps = 30
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps

    for _ in range(steps):
        new_x = line_drawer.xcor() + dx
        new_y = line_drawer.ycor() + dy
        line_drawer.goto(new_x, new_y)
        wn.update()

def get_win_pattern(player):
    # Rows
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return [(i, 0), (i, 1), (i, 2)]
    # Columns
    for j in range(3):
        if all(board[i][j] == player for i in range(3)):
            return [(0, j), (1, j), (2, j)]
    # Diagonals
    if all(board[i][i] == player for i in range(3)):
        return [(0, 0), (1, 1), (2, 2)]
    if all(board[i][2 - i] == player for i in range(3)):
        return [(0, 2), (1, 1), (2, 0)]
    return None

def ai_move():
    if game_over:
        return
    # try to win
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                if get_win_pattern("O"):
                    return
                board[r][c] = ""
    # block player
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "X"
                if get_win_pattern("X"):
                    board[r][c] = "O"
                    return
                board[r][c] = ""
    # pick first empty
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                return

def reset_board():
    global board, game_over
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    game_over = False
    symbol_drawer.clear()
    line_drawer.clear()
    draw_grid()
    draw_board()
    update_scoreboard()

def click(x, y):
    global player_score, ai_score, game_over
    if game_over:
        return
    col = int((x - TOP_LEFT_X) // CELL_SIZE)
    row = int((TOP_LEFT_Y - y) // CELL_SIZE)
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
        board[row][col] = "X"
        draw_board()
        win_cells = get_win_pattern("X")
        if win_cells:
            game_over = True
            highlight_win(win_cells)
            player_score += 1
            update_scoreboard()
            wn.ontimer(reset_board, 1000)
            return
        ai_move()
        draw_board()
        win_cells = get_win_pattern("O")
        if win_cells:
            game_over = True
            highlight_win(win_cells)
            ai_score += 1
            update_scoreboard()
            wn.ontimer(reset_board, 1000)
            return
        if all(cell != "" for row in board for cell in row):
            game_over = True
            wn.ontimer(reset_board, 1000)

# Start game
wn.onclick(click)
update_scoreboard()
wn.update()
wn.mainloop()