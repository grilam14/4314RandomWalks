import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections


class Random_Walks_Python():
    def __init__(self):
                # Our code start
        min = -100
        max = 100
        # better if food has an integer sqrt
        food = 49
        # better if clusterCount is divisible by food
        clusterCount = 7
        clusterPoints = round(food/clusterCount)
        clusterRange = 15
        self.eatRange = 2
        self.scentRange = 10

        self.xRandom = collections.deque()
        self.yRandom = collections.deque()
        self.xUniform = collections.deque()
        self.yUniform = collections.deque()
        self.xCluster = collections.deque()
        self.yCluster = collections.deque()

        # generate random points
        for _ in range(food):
            self.xRandom.append(np.random.uniform(min, max, 1))
            self.yRandom.append(np.random.uniform(min, max, 1))
            

        # generate evenly spaced points
        xlen = np.linspace(min, max, round(np.sqrt(food)))
        ylen = np.linspace(min, max, round(np.sqrt(food)))
        for i in range(len(xlen)):
            for j in range(len(ylen)):
                self.xUniform.append(xlen[i])
                self.yUniform.append(ylen[j])

        # generate random w/ cluster points
        for _ in range(clusterCount): 
            xrand = np.random.uniform(min, max, 1)
            yrand = np.random.uniform(min, max, 1)
            for _ in range(clusterPoints):
                self.xCluster.append(np.random.uniform(xrand - clusterRange, xrand + clusterRange, 1))
                self.yCluster.append(np.random.uniform(yrand - clusterRange, yrand + clusterRange, 1))


        ##USE THIS TO CHANGE DATA STRUCTURE

        self.xFoodDistribution = self.xCluster
        self.yFoodDistribution = self.yCluster
        # Hello world

    def change_distribution(self, dist_name):
        if dist_name == "random":
            self.xFoodDistribution = self.xRandom
            self.yFoodDistribution = self.yRandom

        elif dist_name == "uniform":
            self.xFoodDistribution = self.xUniform
            self.yFoodDistribution = self.yUniform

        elif dist_name == "cluster":
            self.xFoodDistribution = self.xCluster
            self.yFoodDistribution = self.yCluster
        

    def random_walks(self, fig_cnt):
        N = 500 #no of steps per trajectory
        realizations = 1 #number of trajectories
        v = 1.0 #velocity (step size)
        #theta_s_array = [round(math.pi/24,4),round(math.pi/12,4),round(math.pi/3,4)] #the width of the random walk turning angle distribution (the lower it is, the more straight the trajectory will be)
        theta_s_array = [round(math.pi/24,4)]
        #w_array = [0.0, 0.5, 1.0] #w is the weighting given to the directional bias (and hence (1-w) is the weighting given to correlated motion)
        w_array = [0.0]
        ratio_theta_s_brw_crw = 1
        plot_walks = 1
    
        for w_i in range(len(w_array)):
            w = w_array[w_i]
            for theta_s_i in range(len(theta_s_array)):
                theta_s_crw = np.multiply(ratio_theta_s_brw_crw,theta_s_array[theta_s_i])
                theta_s_brw = theta_s_array[theta_s_i]
                x,y, xFoodsEaten, yFoodsEaten = self.BRCW(N, 
                                                    realizations, 
                                                    v, 
                                                    theta_s_crw, 
                                                    theta_s_brw, 
                                                    w, 
                                                    self.xFoodDistribution, 
                                                    self.yFoodDistribution, 
                                                    self.eatRange, 
                                                    self.scentRange)
                if plot_walks == 1:
                    

                    #fig = plt.figure()
                    '''
                    plt.title("w: " + str(w) + " theta: " + str(theta_s_array[theta_s_i]))
                    plt.plot(x.T, y.T)
                    plt.scatter(self.xFoodDistribution, self.yFoodDistribution, zorder=1)
                    plt.scatter(xFoodsEaten, yFoodsEaten, color="red", zorder=2)
                    plt.axis('equal')
                    
                    
                    #fig.savefig("figures/animal_"+str(fig_cnt)+".png")
                    plt.show()
                    '''
        #plt.figure()
        legend_array = []
        for theta_s_i in range(0, len(theta_s_array)):
            legend_array.append(["$\theta^{*CRW}=$", (ratio_theta_s_brw_crw*theta_s_array[theta_s_i]),"$\theta^{*BRW}=$",(theta_s_array[theta_s_i])])
        
        return len(xFoodsEaten)/len(self.xFoodDistribution)



    def scent(self, curr_x, curr_y, x_food, y_food, x_eaten, y_eaten, scentRange):
        closest_food_dist = 1000
        closest_food_coor = [-200, -200]
        for x, y in zip(x_food, y_food):
            dist_to_food = np.sqrt((curr_x-x)**2 + (curr_y-y)**2)
            if dist_to_food < closest_food_dist and (x not in x_eaten) and (y not in y_eaten):
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
    def BRCW(self, N, realizations, v, theta_s_crw, theta_s_brw,w, xFoods, yFoods, eatRange, scentRange):
        X = np.zeros([realizations, N])
        Y = np.zeros([realizations, N])
        theta = np.zeros([realizations, N])
        X[:, 0] = 0
        Y[:, 0] = 0
        theta[:, 0] = 0
        xFoodsEaten = collections.deque()
        yFoodsEaten = collections.deque()

        for realization_i in range(realizations):
            for step_i in range(1,N):
                
                foodNear, theta_c, theta_b, r = self.scent(X[realization_i, step_i-1],
                                                        Y[realization_i, step_i-1],
                                                        xFoods, yFoods, 
                                                        xFoodsEaten, yFoodsEaten, scentRange)
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

                for food_x, food_y in zip(xFoods, yFoods):

                    # if the animal is within the range of a piece of food
                    if(food_x - eatRange <= X[realization_i, step_i] <= food_x + eatRange 
                    and food_y - eatRange <= Y[realization_i, step_i] <= food_y + eatRange
                    and (food_x not in xFoodsEaten) and (food_y not in yFoodsEaten)):
                        xFoodsEaten.append(food_x)
                        yFoodsEaten.append(food_y)
                        break

                current_x_disp = X[realization_i][step_i] - X[realization_i][step_i-1]
                current_y_disp = Y[realization_i][step_i] - Y[realization_i][step_i-1]
                current_direction = math.atan2(current_y_disp,current_x_disp)

                theta[realization_i, step_i] = current_direction

        return X, Y, xFoodsEaten, yFoodsEaten

rdm_plt = Random_Walks_Python()

dists = ['random', 'uniform', 'cluster']

N = 10
fig = plt.figure()
ax = fig.add_subplot(111)

# TO DO: Consider what parameters to change/compare, clustered is the superior distribution with current code

for dist in dists:
    ratios = [0] * N
    rdm_plt.change_distribution(dist)
    for i in range(0,N):
        ratios[i] = rdm_plt.random_walks(i)
        ax.scatter(dist,ratios[i])

plt.ylabel("% food discovered")
plt.show()    







