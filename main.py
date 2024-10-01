from tkinter import *
import random

GAME_WIDTH = 500
# OG is 700
GAME_HEIGHT = 500
SPEED = 50
# OG is 50
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#0096FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    # here we called an init method to construct a food object for us
    #init basically initialises a constructor
    def __init__(self):
        # we need to place our food object randomly
        # init is where you can define the starting state of an object when it's instantiated
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#       we need to place our food object randomly


# these are all  functions

def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y-= SPACE_SIZE
    elif direction == "down":
        y+= SPACE_SIZE
    elif direction == "left":
        x-= SPACE_SIZE
    elif direction == "right":
        x+= SPACE_SIZE

    # 0 is the head of the snake, then we insert new x and y coordinates at the new location
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # indicates overlap
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score +=1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    # we will only delete the last body part of the snake if we didn't eat a food object
    else:
        # here we delete the body part of our snake
        del snake.coordinates[-1]

        # here we update our canvas
        canvas.delete(snake.squares[-1] )

         # now we delete the list of squares that appear at index -1
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        # update to next turn
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

#   global direction is the old direction
    global direction

    # so that we don't make a 180 degree turn
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_WIDTH:
        return True

    # this is in case the snake runs into its body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")



window = Tk()
window.title("Snake game")
# in order  to make the window non-resizable we have to pass in false twice
window.resizable(False, False)

score = 0
direction = 'down'

# we pass window because we're adding the label to our window
# we also pass in our score into the format
#generally this part right here creates our title at the top
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# this part right here creates our gameboard
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


# this part affects the actual game window which contains the title (label) and the canvas
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# this makes it so that the window is centered on your screen
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# here we bind our keys from our keyboard in order to move the snake
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
# here we are creating a snake object and food object
# we want to make a "snake" object and thus call the "Snake" constructor
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()