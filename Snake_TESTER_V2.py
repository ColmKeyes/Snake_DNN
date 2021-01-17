

import curses
import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from generating_data_Snake import keys_to_outputs
import pandas as pd
import pickle
#from Snake_DNN_V2 import model
import tensorflow as tf
import tflearn
import numpy as np
import time

#tf.reset_default_graph() #This is used to reset when odd errors occur


#data
food_position_data = np.load('food_position_data1_TRAINING_LOOP.npy')
score_data = np.load('score_data1_TRAINING_LOOP.npy')
key_data = np.load('key_data1_TRAINING_LOOP.npy')
body_position_data = np.load('body_position_data1_TRAINING_LOOP.npy')
#####################################################################################################################

#model
def snake_model(food_position_data, body_position_data):
	input_data1 = np.concatenate((food_position_data,body_position_data), axis=1)
	net = tflearn.input_data(shape = [None,4], name = ('food_position'))
	net = tflearn.fully_connected(net,32, activation = 'relu', weight_decay = 0.05)
	net = tflearn.fully_connected(net, 4, activation  ='relu')
	regression = tflearn.regression(net, optimizer='sgd', loss='mean_square',
								metric='R2', learning_rate=0.01)
	#training
	model = tflearn.DNN(regression, tensorboard_verbose=3)
	model.fit(input_data1, key_data, validation_set=0.15, show_metric = True ,n_epoch=1)#, batch_size = 200)
	print("done a round")
	model.save('Snake_DNN_v6_TRAINING_LOOP')#, weights_only = True)
	return model
#####################################################################################################################

#init
curses.initscr()
win = curses.newwin(20,60, 0,0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
key = KEY_RIGHT
score = 0
snake = [[4,10], [4,9], [4,8]]
food = [4,5]
win.addch(food[0], food[1], '*')

#####################################################################################################################

#main
start_time = time.time()
while key != 27:	
	elapsed_time = time.time() - start_time
	win.border(0)
	win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
	win.addstr(0, 27, ' SNAKE ') 
	win.timeout(int(150 - (len(snake)/5 + len(snake)/10)%120))
	prevKey = key
	event = win.getch()
	if key == 27:
		curses.endwin()
	key = key if event == -1 else event
	if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
		key = -1                                                   # one (Pause/Resume)
		while key != ord(' '):
			key = win.getch()
		key = prevKey
		continue

	snake1 = np.array(snake)
	predict_data = np.concatenate(([food],[snake[0]]),axis=1) 
	prediction1 = model.predict(predict_data)
	prediction_array = np.array(prediction1)
	prediction = np.sum(prediction_array, axis=0)/1

	if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
		key = prevKey
	if max(prediction) == prediction[0]:
		key = KEY_UP
		print(key)
	elif max(prediction) == prediction[1]:
		key = KEY_LEFT
		print(key)	
	elif max(prediction) == prediction[2]:
		key = KEY_DOWN
		print(key)
	elif max(prediction) == prediction[3]:
		key = KEY_RIGHT
		print(key)

	snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
	if snake[0][0] == 0: snake[0][0] = 18
	if snake[0][1] == 0: snake[0][1] = 58
	if snake[0][0] == 19: snake[0][0] = 1
	if snake[0][1] == 59: snake[0][1] = 1

	if snake[0] in snake[1:]:
		key = random.choice([KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN])
	if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break
	if snake[0] == food:
		food = []
		score  +=1
		while food == []:
			food = [randint(1,18), randint(1,58)]
			if food in snake: 
				score += 1
				food = []
		win.addch(food[0], food[1], '*')
	else:    
		last = snake.pop()
		win.addch(last[0], last[1], ' ')
	win.addch(snake[0][0], snake[0][1], '#')
	#if elapsed_time >10:
	#	quit()
	if key == -1:
		quit() 



curses.endwin()
print("\nScore - " + str(score))
