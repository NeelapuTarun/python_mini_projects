# SNAKE GAME

import turtle #  module in Python is used for creating graphics and simple animations by controlling a virtual “turtle” on the screen.
import time
import random # for placing food at random coordinates
import os #for checking if image files exist before loading them

# Game variables
delay = 0.1
level = 1
score = 0
high_score = 0

#  Setup screen
wn = turtle.Screen()
wn.title("Snake Game :-)")
wn.setup(width=600, height=600) #size of the screen
wn.tracer(0)#It turns off automatic screen updates in the Turtle graphics window.
#By default, Turtle updates the screen after every movement—this slows down complex animations.


#  Load background image if available
if os.path.exists("background.gif"):
    wn.bgpic("background.gif")
else:
    wn.bgcolor("green")  # fallback color

#  Snake head
head = turtle.Turtle() #It creates a new Turtle object named head, which represents the snake’s head in your game.
head.speed(0)
head.shape("square")
head.color("black")
head.penup() #It lifts the turtle’s pen, so it moves without drawing lines on the screen.
head.goto(0, 0) #is a command that moves the snake’s head to the center of the screen.
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []  # Body parts as squares like elements in a list

#  Score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0  Level: 1", align="center", font=("Courier", 16, "normal"))

# 🎮 Movement functions
# defining new functions for the body to move
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

#  Show Game Over image or text and reset

def show_game_over_image():
    global score, delay, level, segments

    if os.path.exists("game_over.gif"):
        wn.bgpic("game_over.gif")
        wn.update()
        time.sleep(2.5) # time duration of the game over text
        # Restore background
        if os.path.exists("background.gif"):
            wn.bgpic("background.gif")
        else:
            wn.bgcolor("green")
    else:
        # Show text in the middle of screen instead of crashing
        temp_pen = turtle.Turtle()
        temp_pen.speed(0)
        temp_pen.color("white")
        temp_pen.hideturtle()
        temp_pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        wn.update()
        time.sleep(2.5)
        temp_pen.clear()

    # Reset game state
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    delay = 0.1
    level = 1
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}  Level: {level}",
    align="center", font=("Courier", 16, "normal"))

#  Keyboard bindings
# To bind the actions of the snake moments with the arrow keys of the laptop
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

#  Main game loop
try:
    while True:
        wn.update()

        #  Border collision
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
            show_game_over_image()

        #  Food collision
        if head.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            # Score implemntation at eating fruit everytime

            delay = max(0.05, delay - 0.001)  # never too fast
            score += 10
            if score > high_score:
                high_score = score

            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}  Level: {level}",
                align="center", font=("Courier", 16, "normal"))

        #  Move segments
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move() #This function updates the position of the snake’s head based on its current direction.

        #  Body collision
        for segment in segments:
            if segment.distance(head) < 20:
                show_game_over_image()

        #  Level progression (speeds up)
        if level == 1 and score >= 50:
            level = 2
            delay = 0.08
        elif level == 2 and score >= 100:
            level = 3
            delay = 0.06
        elif level == 3 and score >= 150:
            level = 4
            delay = 0.05
        elif level == 4 and score >= 250:
            level = 5
            delay = 0.04
        elif level ==5 and score >= 300:
            level = "congrats"
            delay = 0.04

        time.sleep(delay)

except turtle.Terminator:
    print("Game window closed. Exiting gracefully.")
