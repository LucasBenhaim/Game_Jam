import turtle
import os

wn = turtle.Screen()
wn.title("PONGO")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

#First Paddle
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("pink")
left_paddle.shapesize(stretch_wid=5, stretch_len=1)
left_paddle.penup()
left_paddle.goto(-360, 0)

right_paddle = turtle.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color("purple")
right_paddle.shapesize(stretch_wid=5, stretch_len=1)
right_paddle.penup()
right_paddle.goto(360, 0)


#BALL
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("orange")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = -0.1

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("orange")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player 1: 0                            Player 2: 0", align="center", font=("Times New Roman", 26, "normal"))

#Score
score_1 = 0
score_2 = 0

#Function Paddle 1
def left_paddle_up():
    y = left_paddle.ycor()
    y += 75
    left_paddle.sety(y)
    if left_paddle.ycor() > 245:
        left_paddle.sety(245)
    os.system("aplay data/pong/paddle.wav&")

def left_paddle_down():
    y = left_paddle.ycor()
    y -= 75
    left_paddle.sety(y)
    if left_paddle.ycor() < -242:
        left_paddle.sety(-242)
    os.system("aplay data/pong/paddle.wav&")

#Function Paddle 2
def right_paddle_up():
    y = right_paddle.ycor()
    y += 75
    right_paddle.sety(y)
    if right_paddle.ycor() > 245:
        right_paddle.sety(245)
    os.system("aplay data/pong/paddle.wav&")

def right_paddle_down():
    y = right_paddle.ycor()
    y -= 75
    right_paddle.sety(y)
    if right_paddle.ycor() < -242:
        right_paddle.sety(-242)
    os.system("aplay data/pong/paddle.wav&")

#Keyboard binding
wn.listen()
wn.onkeypress(left_paddle_up, "z")
wn.onkeypress(left_paddle_down, "s")
wn.onkeypress(right_paddle_up, "Up")
wn.onkeypress(right_paddle_down, "Down")

def gameloop_pong():
    #Main game loop
    while True:
        wn.update()

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            os.system("aplay data/pong/keb.wav&")

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            os.system("aplay data/pong/keb.wav&")

        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_1 += 1
            pen.clear()
            pen.write("Player 1: {}                            Player 2: {}".format(score_1, score_2), align="center", font=("Times New Roman", 26, "normal"))
            os.system("aplay data/pong/pongo.wav&")

        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_2 += 1
            pen.clear()
            pen.write("Player 1: {}                            Player 2: {}".format(score_1, score_2), align="center", font=("Times New Roman", 26, "normal"))
            os.system("aplay data/pong/pongo.wav&")

        #Collision
        if ball.xcor() > 340 and (ball.ycor() < right_paddle.ycor() + 40 and ball.ycor() > right_paddle.ycor() - 40):
            ball.setx(340)
            ball.dx *= -1
            os.system("aplay data/pong/keb.wav&")

        if ball.xcor() < -340 and (ball.ycor() < left_paddle.ycor() + 40 and ball.ycor() > left_paddle.ycor() - 40):
            ball.setx(-340)
            ball.dx *= -1
            os.system("aplay data/pong/keb.wav&")