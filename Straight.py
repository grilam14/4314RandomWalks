import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections

def scent(curr_x, curr_y, food, eaten, scentRange):
    closest_food_dist = 1000
    closest_food_coor = [-200, -200]
    for key in food.keys():
        x = food[key][0]
        y = food[key][1]

        dist_to_food = np.sqrt((curr_x-x)**2 + (curr_y-y)**2)

        alreadyEaten = False
        if dist_to_food < closest_food_dist and (key not in eaten):
            closest_food_dist = dist_to_food
            closest_food_coor = [x,y]
    
    if closest_food_dist < scentRange:
        x_disp = closest_food_coor[0] - curr_x
        y_disp = closest_food_coor[1] - curr_y
        direction = math.atan2(y_disp,x_disp)
        return 1, direction, direction, 0.75

    else:
        return 0,1,1,0

#The funciton generate 2D Biased Corrolated Random Walks
def Straight_s(N, realizations, v, theta_s_crw, theta_s_brw,w, Foods, eatRange, scentRange):
    X = np.zeros([realizations, N])
    Y = np.zeros([realizations, N])
    theta = np.zeros([realizations, N])
    X[:, 0] = 0
    Y[:, 0] = 0
    theta[:, 0] = 0
    FoodsEaten = []
    FoodsID = []

    for i in range(realizations):
        theta[i, 0] = np.random.uniform(-np.pi, np.pi)

    for realization_i in range(realizations):
        for step_i in range(1,N):
            foodNear, theta_c, theta_b, r = scent(X[realization_i, step_i-1],
                                                    Y[realization_i, step_i-1],
                                                    Foods, FoodsID, scentRange)
            
            #foodNear = 0
            if( X[realization_i, step_i-1] >= 100):
                
                num = np.random.choice([-1,1])
                # Half the time will go to second quadrant, other half to the third
                theta_crw = num * np.random.uniform(np.pi/2, np.pi)

            elif( X[realization_i, step_i-1] <= -100):

                num = np.random.choice([-1,1])
                # Half the time will go to first quadrant, other half to the fourth
                theta_crw = num * np.random.uniform(0, np.pi/2)

            elif( Y[realization_i, step_i-1] >= 100):
                theta_crw = np.random.uniform(-np.pi, 0)

            elif( Y[realization_i, step_i-1] <= -100):
                theta_crw = np.random.uniform(0, np.pi)

            elif (foodNear):
                theta_crw = theta_c

            else:
                theta_crw = theta[realization_i][step_i-1]

            X[realization_i, step_i] = X[realization_i][step_i-1] + (v * (math.cos(theta_crw)))
            Y[realization_i, step_i] = Y[realization_i][step_i-1] + (v * (math.sin(theta_crw)))

            for key in Foods.keys():
                food_x = Foods[key][0]
                food_y = Foods[key][1]
                # if the animal is within the range of a piece of food
                if ((food_x - eatRange <= X[realization_i, step_i] <= food_x + eatRange) 
                and (food_y - eatRange <= Y[realization_i, step_i] <= food_y + eatRange) 
                and (key not in FoodsID)):
                    FoodsEaten.append([food_x, food_y])
                    FoodsID.append(key)
                    break

            current_x_disp = X[realization_i][step_i] - X[realization_i][step_i-1]
            current_y_disp = Y[realization_i][step_i] - Y[realization_i][step_i-1]
            current_direction = math.atan2(current_y_disp,current_x_disp)

            theta[realization_i, step_i] = current_direction
    
    return X, Y, FoodsEaten

def Straight(N, realizations, v, theta_s_crw, theta_s_brw,w, Foods, eatRange, scentRange):
    X = np.zeros([realizations, N])
    Y = np.zeros([realizations, N])
    theta = np.zeros([realizations, N])
    X[:, 0] = 0
    Y[:, 0] = 0
    theta[:, 0] = 0
    FoodsEaten = []
    FoodsID = []

    for i in range(realizations):
        theta[i, 0] = np.random.uniform(-np.pi, np.pi)

    for realization_i in range(realizations):
        for step_i in range(1,N):
            
            if( X[realization_i, step_i-1] >= 100):
                
                num = np.random.choice([-1,1])
                # Half the time will go to second quadrant, other half to the third
                theta_crw = num * np.random.uniform(np.pi/2, np.pi)

            elif( X[realization_i, step_i-1] <= -100):

                num = np.random.choice([-1,1])
                # Half the time will go to first quadrant, other half to the fourth
                theta_crw = num * np.random.uniform(0, np.pi/2)

            elif( Y[realization_i, step_i-1] >= 100):
                theta_crw = np.random.uniform(-np.pi, 0)

            elif( Y[realization_i, step_i-1] <= -100):
                theta_crw = np.random.uniform(0, np.pi)

            else:
                theta_crw = theta[realization_i][step_i-1]

            X[realization_i, step_i] = X[realization_i][step_i-1] + (v * (math.cos(theta_crw)))
            Y[realization_i, step_i] = Y[realization_i][step_i-1] + (v * (math.sin(theta_crw)))

            for key in Foods.keys():
                food_x = Foods[key][0]
                food_y = Foods[key][1]
                # if the animal is within the range of a piece of food
                if ((food_x - eatRange <= X[realization_i, step_i] <= food_x + eatRange) 
                and (food_y - eatRange <= Y[realization_i, step_i] <= food_y + eatRange)
                and (key not in FoodsID)):
                    FoodsEaten.append([food_x, food_y])
                    FoodsID.append(key)
                    break

            current_x_disp = X[realization_i][step_i] - X[realization_i][step_i-1]
            current_y_disp = Y[realization_i][step_i] - Y[realization_i][step_i-1]
            current_direction = math.atan2(current_y_disp,current_x_disp)

            theta[realization_i, step_i] = current_direction
    
    return X, Y, FoodsEaten