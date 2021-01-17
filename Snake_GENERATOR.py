

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from generating_data_Snake import keys_to_outputs
import pandas as pd
import pickle
import numpy as np
import time
from time import sleep
#######################################################################################################################

#init
curses.initscr()
win = curses.newwin(20,60,0,0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
curses.start_color()
win.border(0)
win.nodelay(1)

key = KEY_RIGHT
score = 0
snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = [randint(3,36), randint(3,36)]
win.addch(food[0], food[1], '*')
key_data = []
other_data = []
score_data = []
body_position_data =[]
food_position_data = []
mid_position_data = []
#######################################################################################################################

#main
while key != 27:
	win.border(0)
	win.addstr(0, 2, 'Score : ' + str(score) + ' ')
	win.addstr(0, 20, ' SNAKE ') 
	win.timeout(int(150 - (len(snake)/5 + len(snake)/10)%120))
	
	prevKey = key
	event = win.getch()
	key = key if event == -1 else event
	#saving keypress data
	key_data.append(keys_to_outputs(key))
	if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
		key = -1                                                   # one (Pause/Resume)
		while key != ord(' '):
			key = win.getch()
		key = prevKey
		continue

 
	if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
		key = prevKey

	snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
	k = randint(0,1)

	if snake[0][0] == 0: snake[0][0] = 38
	if snake[0][1] == 0: snake[0][1] = 38
	if snake[0][0] == 39: snake[0][0] = 1
	if snake[0][1] == 39: snake[0][1] = 1

	if snake[0] == food:
		food = []
		score  +=1
		while food == []:
			food = [randint(3,36), randint(3,36)]
			if food in snake: 
				score += 1
				food = []
		win.addch(food[0], food[1], '*')
	else:    
		last = snake.pop()
		win.addch(last[0], last[1], ' ')
	win.addch(snake[0][0], snake[0][1], '#', curses.COLOR_RED)
	food_position_data.append(food)
	body_position_data.append(snake[0])
	mid_position_data.append(snake[1])
	score_data.append(score)
	print(snake[0])
	sleep(0.05)
curses.endwin()
print("\nScore - " + str(score))
#######################################################################################################################

#saving/appending data
food_position_data1 = np.load('food_position_data1.npy')
key_data1 = np.load('key_data1.npy')
body_position_data1 = np.load('body_position_data1.npy')
mid_position_data1 = np.load('mid_position_data1.npy')

food_position_data1 = np.concatenate(( food_position_data1, food_position_data), axis = 0)
key_data1 = np.concatenate((  key_data1,  key_data), axis = 0)
body_position_data1 = np.concatenate(( body_position_data1,  body_position_data), axis = 0)
mid_position_data1 = np.concatenate(( mid_position_data1,  mid_position_data), axis = 0)

np.save('food_position_data1.npy',food_position_data1)
np.save('body_position_data1.npy', body_position_data1)
np.save('key_data1.npy',key_data1)
np.save('mid_position_data1.npy',mid_position_data1)
