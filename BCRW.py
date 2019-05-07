def scent(self, curr_x, curr_y, food, eaten, scentRange):
    closest_food_dist = 1000
    closest_food_coor = [-200, -200]
    for x, y in food.values():
        dist_to_food = np.sqrt((curr_x-x)**2 + (curr_y-y)**2)

        alreadyEaten = False
        if dist_to_food < closest_food_dist and (x not in [e[0] for e in eaten]) and (y not in [e[1] for e in eaten]):
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
def BCRW(self, N, realizations, v, theta_s_crw, theta_s_brw,w, Foods, eatRange, scentRange):
    X = np.zeros([realizations, N])
    Y = np.zeros([realizations, N])
    theta = np.zeros([realizations, N])
    X[:, 0] = 0
    Y[:, 0] = 0
    theta[:, 0] = 0
    FoodsEaten = []

    for realization_i in range(realizations):
        for step_i in range(1,N):
            
            foodNear, theta_c, theta_b, r = self.scent(X[realization_i, step_i-1],
                                                    Y[realization_i, step_i-1],
                                                    Foods, FoodsEaten, scentRange)
            
            #foodNear = 0
            if( X[realization_i, step_i-1] >= 100):
                theta_crw = -np.pi
                theta_brw = -np.pi
                r = w

            elif( X[realization_i, step_i-1] <= -100):
                theta_crw = 0
                theta_brw = 0
                r = w

            elif( Y[realization_i, step_i-1] >= 100):
                theta_crw = -np.pi/2
                theta_brw = -np.pi/2
                r = w

            elif( Y[realization_i, step_i-1] <= -100):
                theta_crw = np.pi/2
                theta_brw = np.pi/2
                r = w

            elif (foodNear):
                theta_crw = theta_c
                theta_brw = theta_b

            else:
                theta_crw = theta[realization_i][step_i-1]+(theta_s_crw* 2.0 * (np.random.rand(1,1)-0.5))
                theta_brw = (theta_s_brw* 2.0 * (np.random.rand(1,1)-0.5))
                r = w

            X[realization_i, step_i] = X[realization_i][step_i-1] + (v * (r*math.cos(theta_brw))) + ((1-r) * math.cos(theta_crw))
            Y[realization_i, step_i] = Y[realization_i][step_i-1] + (v * (r*math.sin(theta_brw))) + ((1-r)* math.sin(theta_crw))

            for food_x, food_y in Foods.values():

                # if the animal is within the range of a piece of food
                if ((food_x - eatRange <= X[realization_i, step_i] <= food_x + eatRange) 
                and (food_y - eatRange <= Y[realization_i, step_i] <= food_y + eatRange)
                and (food_x not in [e[0] for e in FoodsEaten]) and (food_y not in [e[1] for e in FoodsEaten])):
                    FoodsEaten.append([food_x, food_y])
                    break

            current_x_disp = X[realization_i][step_i] - X[realization_i][step_i-1]
            current_y_disp = Y[realization_i][step_i] - Y[realization_i][step_i-1]
            current_direction = math.atan2(current_y_disp,current_x_disp)

            theta[realization_i, step_i] = current_direction

    return X, Y, FoodsEaten