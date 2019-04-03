import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections

'''
Generate set of points, go through list of points to see if our location is within 1. searching range and
2. eating range via distance calculation. Apply appropriate logic if it's either are true. 

'''

class Random_Walks_Python():
    def random_walks(self):
        N = 500 #no of steps per trajectory
        realizations = 1 #number of trajectories
        v = 1.0 #velocity (step size)
        #theta_s_array = [round(math.pi/24,4),round(math.pi/12,4),round(math.pi/3,4)] #the width of the random walk turning angle distribution (the lower it is, the more straight the trajectory will be)
        theta_s_array = [round(math.pi/3,4)]
        #w_array = [0.0, 0.5, 1.0] #w is the weighting given to the directional bias (and hence (1-w) is the weighting given to correlated motion)
        w_array = [0.0]
        ratio_theta_s_brw_crw = 1
        plot_walks = 1
        count = 0

        # Our code start
        min = -100
        max = 100
        # better if food has an integer sqrt
        food = 49
        # better if clusterCount is divisible by food
        clusterCount = 7
        clusterPoints = round(food/clusterCount)
        clusterRange = 15
        eatRange = 10

        xRandom = collections.deque()
        yRandom = collections.deque()
        xUniform = collections.deque()
        yUniform = collections.deque()
        xRandomCluster = collections.deque()
        yRandomCluster = collections.deque()

        # generate random points
        for _ in range(food):
            xRandom.append(np.random.uniform(min, max, 1))
            yRandom.append(np.random.uniform(min, max, 1))
            

        # generate evenly spaced points
        xlen = np.linspace(min, max, round(np.sqrt(food)))
        ylen = np.linspace(min, max, round(np.sqrt(food)))
        for i in range(len(xlen)):
            for j in range(len(ylen)):
                xUniform.append(xlen[i])
                yUniform.append(ylen[j])

        # generate random w/ cluster points
        for _ in range(clusterCount): 
            xrand = np.random.uniform(min, max, 1)
            yrand = np.random.uniform(min, max, 1)
            for _ in range(clusterPoints):
                xRandomCluster.append(np.random.uniform(xrand - clusterRange, xrand + clusterRange, 1))
                yRandomCluster.append(np.random.uniform(yrand - clusterRange, yrand + clusterRange, 1))


        ##USE THIS TO CHANGE DATA STRUCTURE

        xFoodDistribution = xRandomCluster
        yFoodDistribution = yRandomCluster
        # Our code end

        
        efficiency_array = np.zeros([len(theta_s_array),len(w_array)])
        for w_i in range(len(w_array)):
            w = w_array[w_i]
            for theta_s_i in range(len(theta_s_array)):
                theta_s_crw = np.multiply(ratio_theta_s_brw_crw,theta_s_array[theta_s_i])
                theta_s_brw = theta_s_array[theta_s_i]
                x,y, xFoodsEaten, yFoodsEaten = self.BRCW(N, realizations, v, theta_s_crw, theta_s_brw, w, xFoodDistribution, yFoodDistribution, eatRange)
                if plot_walks == 1:
                    count += 1
                    plt.figure(count)
                    plt.title("w: " + str(w) + " theta: " + str(theta_s_array[theta_s_i]))
                    plt.plot(x.T, y.T)
                    plt.scatter(xRandomCluster, yRandomCluster)
                    plt.scatter(xFoodsEaten, yFoodsEaten, color="red")
                    plt.axis('equal')
                efficiency_array[theta_s_i, w_i] = np.divide(np.mean(x[:,-1]-x[:,0]),(v*N))
                print(efficiency_array[theta_s_i, w_i])
            plt.show()
        plt.figure()
        legend_array = []
        w_array_i = np.repeat(w_array,len(efficiency_array))
        for theta_s_i in range(0, len(theta_s_array)):
            legend_array.append(["$\theta^{*CRW}=$", (ratio_theta_s_brw_crw*theta_s_array[theta_s_i]),"$\theta^{*BRW}=$",(theta_s_array[theta_s_i])])

        '''
        plt.xlabel('w')
        plt.ylabel('navigational efficiency')
        plt.title('Navigational Efficiency Aggregate')
        plt.plot(w_array, efficiency_array[0],'bo', label = legend_array[0])
        #plt.plot(w_array, efficiency_array[1],'go', label = legend_array[1])
        #plt.plot(w_array, efficiency_array[2],'ro', label = legend_array[2])
        plt.legend(loc='best', prop={'size': 5.2})
        plt.show()
        '''



#The funciton generate 2D Biased Corrolated Random Walks
    def BRCW(self,N, realizations, v, theta_s_crw, theta_s_brw,w, xFoods, yFoods, eatRange):
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
                theta_crw = theta[realization_i][step_i-1]+(theta_s_crw* 2.0 * (np.random.rand(1,1)-0.5))
                theta_brw = (theta_s_brw* 2.0 * (np.random.rand(1,1)-0.5))

                X[realization_i, step_i] = X[realization_i][step_i-1] + (v * (w*math.cos(theta_brw))) + ((1-w) * math.cos(theta_crw))
                Y[realization_i, step_i] = Y[realization_i][step_i-1] + (v* (w*math.sin(theta_brw))) +((1-w)* math.sin(theta_crw))

                index = 0;
                eaten = False
                for food_x, food_y in zip(xFoods, yFoods):
                    print(food_x, food_y)
                    # if the animal is within the range of a piece of food
                    if(food_x - eatRange <= X[realization_i, step_i] <= food_x + eatRange and food_y - eatRange <= Y[realization_i, step_i] <= food_y + eatRange):
                        xFoodsEaten.append(food_x)
                        yFoodsEaten.append(food_y)
                        eaten = True
                        break
                    index+=1
                # remove food
                if(eaten):
                    del xFoods [index]
                    del yFoods [index]

                current_x_disp = X[realization_i][step_i] - X[realization_i][step_i-1]
                current_y_disp = Y[realization_i][step_i] - Y[realization_i][step_i-1]
                current_direction = math.atan2(current_y_disp,current_x_disp)

                theta[realization_i, step_i] = current_direction

        return X, Y, xFoodsEaten, yFoodsEaten

rdm_plt = Random_Walks_Python()
rdm_plt.random_walks()
