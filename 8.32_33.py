# -*- coding:Utf8 -*-
########################################################
# single file                                          #
# Autor: Autin Alexandre, 31/05/23 (creation)          #
########################################################

""" It's a copy of the game Snake-'97. Here you control the skape with the
directions arrows of the keyboard, the goal is to make the snake longer by
eating circles, you lose when the snake touch an edge or itself. """


#############################imported-fonctions##############################
import tkinter

import time 

import random
from random import randrange, choice

import pygame
from pygame import mixer


##########################initial-global-variables###########################
party_statut = 'no_game'

image_number = []

snake_body = []

snake_coords = []
coords = []
fruit_coords = []

snake_eyes = []

snake_direction = []
movement_direction = ''


###############################local-fonctions###############################
def background_music(step):
    """ Simple function which sets and play (or stop and quit) the 
    music in the mixer. """
    if step == 'start':
        pygame.mixer.init(44100, -16, 4, 5000)
        mixer.music.load(
            "./Zelda_music_remix_320.mp3")
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)
    elif step == 'stop':
        mixer.music.stop()
        pygame.mixer.quit()


def create_area_game():
    """ Prepare the whole area which will be play the game. """
    create_shapes_cases()
    create_borders()
def create_shapes_cases():
    """ It makes appear the case of the game_zone by separating the zone in
    10x10 squares of 50 pixels of height and width. """
    for row in range(11):
        game_zone.create_line(
            0, 0 + row*50,
            500, 0 + row*50,
            width=4, fill='#37DF60',
        )
    for column in range(11):
        game_zone.create_line(
            0 + column*50, 0,
            0 + column*50, 500,
            width=4, fill='#37DF60',
        )
def create_borders():
    """ It demands the drawing of the 4 lines in the game_zone,
    which form the borders of the movements's snake area."""
    create_border(25, 25, 25, 475)
    create_border(25, 475, 475, 475)
    create_border(475, 475, 475, 25)
    create_border(475, 25, 25, 25)
def create_border(x1, y1, x2, y2):
    """ It draws a line with the color and the width of the border. """
    game_zone.create_line(
            x1, y1, x2, y2,
            width=4, fill='#768F7C',
        )


def start_and_stop_game(event=None):
    """ Triggered by space-key or the play button, it updates the 
    playing state and updates the text of play button. """
    global party_statut
    if party_statut == 'no_game':
        party_statut = 'starting'
        play_btn.configure(text='WAIT')
        place_snake_head()
        fruit_appearance()
        timer_before_play()
        main_window.after(3000, play_party)
    elif party_statut == 'playing':
        party_statut = 'pause'
        play_btn.configure(text='PLAY')
    elif party_statut == 'pause':
        party_statut = 'restarting'
        play_btn.configure(text='WAIT')
        timer_before_play()
        main_window.after(3000, play_party)
       

def play_party():
    global party_statut
    if party_statut == 'starting' or party_statut == 'restarting':
        party_statut = 'playing'
        play_btn.configure(text='BREAK')
        movement_cycle()


def place_snake_head():
    """ If snake exists (if party begun), adds coords of the snake head to 
    the snake_coords list, and adds the actually orange ball item to 
    the snake_body. """
    global party_statut
    if len(snake_coords) == 0 and party_statut == 'starting':
        snake_coords.append([randrange(1,9), randrange(1,9)])
        snake_body.append(game_zone.create_oval(
            1 + 50*snake_coords[0][0],
            1 + 50*snake_coords[0][1],
            49 + 50*snake_coords[0][0],
            49 + 50*snake_coords[0][1],
            fill='#DBB748',
            ))
        place_snake_eyes()
def place_snake_eyes():
    """ Creates the 2 item which form the eyes of the snake and selects
    randomly the look direction. """
    snake_eyes.append(game_zone.create_oval(
        0,0,0,0,fill='white'
    ))
    snake_eyes.append(game_zone.create_oval(
        0,0,0,0,fill='black'
    ))
    snake_look(random.choice(['left', 'right', 'up', 'down']))


def left(event=None):
    """ Links the click-on-leftkey event and the function which set the 
    look direction. Triggered by an event or a function call"""
    snake_look('left')
def right(event=None):
    """ Links the click-on-rightkey event and the function which set the 
    look direction. Triggered by an event or a function call"""
    snake_look('right')
def up(event=None):
    """ Links the click-on-upkey event and the function which set the 
    look direction. Triggered by an event or a function call"""
    snake_look('up')
def down(event=None):
    """ Links the click-on-downkey event and the function which set the 
    look direction. Triggered by an event or a function call"""
    snake_look('down')


def snake_look(direction):
    """ Uses the direction arg to turn the eyes in the right way, 2 items:
    the white oval and the more little black oval"""
    global snake_eyes, snake_direction, party_statut, movement_direction, coords
    if party_statut == 'starting' or party_statut == 'playing':
        if len(snake_eyes) != 0:
            if direction == 'left' and movement_direction != 'right':
                snake_direction = direction
                coords = [6, 15, 16, 35, 8, 24, 11, 27]
            elif direction == 'right' and movement_direction != 'left':
                snake_direction = direction
                coords = [44, 15, 34, 35, 42, 24, 39, 27]
            elif direction == 'up' and movement_direction != 'down':
                snake_direction = direction
                coords = [15, 16, 35, 6, 23, 8, 27, 11]
            elif direction == 'down' and movement_direction != 'up':
                snake_direction = direction
                coords = [35, 34, 15, 44, 27, 42, 23, 39]
            else:
                snake_direction = movement_direction
            game_zone.coords(
                snake_eyes[0],
                coords[0] + 50*snake_coords[0][0],
                coords[1] + 50*snake_coords[0][1],
                coords[2] + 50*snake_coords[0][0],
                coords[3] + 50*snake_coords[0][1],
            )
            game_zone.coords(
                snake_eyes[1],
                coords[4] + 50*snake_coords[0][0],
                coords[5] + 50*snake_coords[0][1],
                coords[6] + 50*snake_coords[0][0],
                coords[7] + 50*snake_coords[0][1],
            )


def timer_before_play():
    global image_number
    if len(image_number) == 0:
        image_number.append(0)
        image_number[0] = game_zone.create_image(
        250, 250,
        image=number_3_img,
        anchor=tkinter.CENTER,
    )
        main_window.after(1000,  timer_before_play)
    elif len(image_number) == 1:
        game_zone.delete(image_number[0])
        image_number.append(1)
        image_number[1] = game_zone.create_image(
        250, 250,
        image=number_2_img,
        anchor=tkinter.CENTER,
    )
        main_window.after(1000,  timer_before_play)
    elif len(image_number) == 2:
        game_zone.delete(image_number[1])
        image_number.append(2)
        image_number[2] = game_zone.create_image(
        250, 250,
        image=number_1_img,
        anchor=tkinter.CENTER,
    )
        main_window.after(1000,  timer_before_play)
    elif len(image_number) == 3:
        game_zone.delete(image_number[2])
        image_number = []


def close_game(event=None):
    """ Triggered by escape-key or the exit button, it quits the program. """
    background_music('stop')
    main_window.quit()


def movement_cycle():
    """ If party started, trigger the snake movement at each cycle time. """
    global party_statut
    if party_statut == 'playing':
        move_snake()
        main_window.after(400, movement_cycle)


def move_snake():
    """ If party playing and, tests to move the snake_coords of a single case:
    - if the snake goes outside: doesnt move snake, trigger the end-game
    - if the snake stays inside: moves snake, updates the look_direction. """
    global snake_direction, party_statut, fruit_coords, movement_direction
    global snake_body, snake_eyes, snake_coords
    if snake_direction == 'left':
        add_x = -1
        add_y = 0
        look = 'left'
        movement_direction = 'left'
    elif snake_direction == 'right':
        add_x = 1
        add_y = 0
        look = 'right'
        movement_direction = 'right'
    elif snake_direction == 'up':
        add_x = 0
        add_y = -1
        look = 'up'
        movement_direction = 'up'
    elif snake_direction == 'down':
        add_x = 0
        add_y = 1
        look = 'down'
        movement_direction = 'down'
    in_x = 0 < snake_coords[0][0] + add_x and snake_coords[0][0] + add_x < 9
    in_y = 0 < snake_coords[0][1] + add_y and snake_coords[0][1] + add_y < 9
    in_xy_snake_touches_itself = test_snake_touches_itself(snake_coords, 
                                                           add_x, add_y, 
                                                           snake_body,
                                                           )
    if (in_x and in_y) and not (in_xy_snake_touches_itself):
        occupied = compare_places_fruit_snake(fruit_coords, 
                                              snake_coords, 
                                              add_x, add_y,
                                              )
        if occupied:
            game_zone.delete(fruit_body)
            fruit_coords = []
            fruit_appearance()
            snake_get_longer()
        for number_snake_ball in range(0, len(snake_body)-1):
            num_ball = len(snake_body)-1 - number_snake_ball
            game_zone.coords(
                    snake_body[num_ball],
                    1 + 50*snake_coords[num_ball-1][0],
                    1 + 50*snake_coords[num_ball-1][1],
                    49 + 50*snake_coords[num_ball-1][0],
                    49 + 50*snake_coords[num_ball-1][1],
                    )
            snake_coords[num_ball][0] = snake_coords[num_ball-1][0]
            snake_coords[num_ball][1] = snake_coords[num_ball-1][1]
        snake_coords[0][0] += add_x
        snake_coords[0][1] += add_y
        game_zone.coords(
                    snake_body[0],
                    1 + 50*snake_coords[0][0],
                    1 + 50*snake_coords[0][1],
                    49 + 50*snake_coords[0][0],
                    49 + 50*snake_coords[0][1],
                    )
        snake_look(look)
    else:
        print('Game over')
        score_printing()
        party_statut = 'no_game'
        for i in range(len(snake_body)):
            game_zone.delete(snake_body[i])
        game_zone.delete(fruit_body)
        game_zone.delete(snake_eyes[0])
        game_zone.delete(snake_eyes[1])
        snake_body = []
        snake_coords = []
        snake_eyes = []
        snake_direction = []
        fruit_coords = []
        play_btn.configure(text='START')


def test_snake_touches_itself(snake_coords, add_x, add_y, snake_body):
    in_x, in_y = False, False
    for num_ball in range(1, len(snake_body)-1):
        if snake_coords[0][0] + add_x == snake_coords[num_ball][0]:
            in_x = True
        if snake_coords[0][1] + add_y == snake_coords[num_ball][1]:
            in_y = True
    if in_x and in_y:
        return True
    else:
        return False


def fruit_appearance():
    global snake_coords, fruit_coords, fruit_body
    fruit_coords.append([randrange(1, 9), randrange(1, 9)])
    occupied = compare_places_fruit_snake(fruit_coords, snake_coords)
    if not occupied:
        fruit_body = game_zone.create_oval(
            7 + 50*fruit_coords[0][0],
            7 + 50*fruit_coords[0][1],
            43 + 50*fruit_coords[0][0],
            43 + 50*fruit_coords[0][1],
            fill='white'
        )
    else:
        fruit_coords = []
        fruit_appearance()


def snake_get_longer():
    snake_coords.append([snake_coords[len(snake_body)-1][0], 
                         snake_coords[len(snake_body)-1][1],
                         ])
    snake_body.append(game_zone.create_oval(
            1 + 50*snake_coords[len(snake_body)-1][0],
            1 + 50*snake_coords[len(snake_body)-1][1],
            49 + 50*snake_coords[len(snake_body)-1][0],
            49 + 50*snake_coords[len(snake_body)-1][1],
            fill='#DBB748',
            ))
    


def compare_places_fruit_snake(fruit_coords, snake_coords, add_x=0, add_y=0):
    for i in range(len(snake_body)):
        if snake_coords[i][0] + add_x == fruit_coords[0][0]:
            if snake_coords[i][1] + add_y == fruit_coords[0][1]:
                return True
    return False


def score_printing():
    global snake_body
    print(len(snake_body))


#################################body-script#################################
main_window = tkinter.Tk()
main_window.title('')
main_window.geometry('550x700')
main_window.configure(background='#174A5A')
main_window.resizable(width=False, height=False)


game_zone = tkinter.Canvas(
    main_window,
    background='#3DEF69',
    height=500,
    width=500,
)
game_zone.place(
    relx=0.5, 
    rely=0.5, 
    anchor=tkinter.CENTER,
)


play_btn = tkinter.Button(
    main_window,
    foreground='BLACK',
    background='#DBB748',
    text='PLAY',
    font=('URW Gothic L', '12', 'bold'),
    command=start_and_stop_game
)
play_btn.place(
    x=24,
    y=677,
    height=50,
    width=120,
    anchor=tkinter.SW
)


exit_btn = tkinter.Button(
    main_window,
    foreground='BLACK',
    background='#DBB748',
    text='EXIT',
    font=('URW Gothic L', '12', 'bold'),
    command=close_game
)
exit_btn.place(
    x=526,
    y=677,
    height=50,
    width=120,
    anchor=tkinter.SE
)


number_1_img = tkinter.PhotoImage(file=
                        './Images/number_1.gif')
number_2_img = tkinter.PhotoImage(file=
                        './Images/number_2.gif')
number_3_img = tkinter.PhotoImage(file=
                        './Images/number_3.gif')
snake_img = tkinter.PhotoImage(file=
                        './Images/snake.gif')
snake_image_zone = tkinter.Canvas(
    main_window,
    background='#174A5A',
    height=50,
    width=210,
    bd=0, 
    highlightthickness=0, 
    relief='ridge',
)
snake_image_zone.place(
    anchor=tkinter.SW,
    x=170,
    y=677,
)
snake_image_zone.create_image(0, 0, image=snake_img, anchor=tkinter.NW)


game_title_canvas = tkinter.Canvas(
    main_window,
    background='#174A5A',
    bd=0, 
    highlightthickness=0,
    relief='ridge',
    height=50,
    width=500,
)
game_title_canvas.place(
    anchor=tkinter.CENTER,
    x=275,
    y=50,
)
game_title_canvas.create_text(
        250,
        25,
        anchor=tkinter.CENTER,
        text='Snake \'92 - Remastered',
        font=('URW Gothic L', '24', 'bold'),
        fill='#DBB748',
    )


main_window.bind('<space>', start_and_stop_game)
main_window.bind('<Escape>', close_game)
main_window.bind('<KeyPress-Left>', left)
main_window.bind('<KeyPress-Right>', right)
main_window.bind('<KeyPress-Up>', up)
main_window.bind('<KeyPress-Down>', down)
main_window.protocol("WM_DELETE_WINDOW", close_game)


create_area_game()
background_music('start')


main_window.mainloop()





# To-do:
#
# Développer : agrandissement de la queue du serpent dès qu'il mange un 
# fruit ainsi que le déplacement de tout son corps dans la game_zone 
# (bloquer retour en arrière)
#
# Donner une impression de physique au serpent (comme limites de la game_zone)
#
# Commenter chaque fonction 