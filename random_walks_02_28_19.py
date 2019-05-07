import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections
from BCRW import BCRW
from Straight import Straight


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

        self.Random = {}

        self.Uniform = {}

        self.Cluster = {}

        # generate random points
        for i in range(food):
            self.Random[i] = [np.random.uniform(min, max), np.random.uniform(min, max)]

        # generate evenly spaced points
        xlen = np.linspace(min, max, int(round(np.sqrt(food))))
        ylen = np.linspace(min, max, int(round(np.sqrt(food))))
        cnt = 0
        for i in range(len(xlen)):
            for j in range(len(ylen)):
                self.Uniform[cnt] = [xlen[i], ylen[j]]
                cnt += 1

        # generate random w/ cluster points
        cnt = 0
        for _ in range(clusterCount): 
            xrand = np.random.uniform(min, max)
            yrand = np.random.uniform(min, max)
            for _ in range(clusterPoints):
                self.Cluster[cnt] = [np.random.uniform(xrand - clusterRange, xrand + clusterRange),
                                     np.random.uniform(yrand - clusterRange, yrand + clusterRange)]
                cnt += 1

        self.FoodDistribution = self.Cluster

    def change_distribution(self, dist_name):
        if dist_name == "random":
            self.FoodDistribution = self.Random

        elif dist_name == "uniform":
            self.FoodDistribution = self.Uniform

        elif dist_name == "cluster":
            self.FoodDistribution = self.Cluster
        

    def random_walks(self, fig_cnt):
        N = 1000 #no of steps per trajectory
        realizations = 1 #number of trajectories
        v = 1.0 #velocity (step size)
        #theta_s_array = [round(math.pi/24,4),round(math.pi/12,4),round(math.pi/3,4)] #the width of the random walk turning angle distribution (the lower it is, the more straight the trajectory will be)
        theta_s_array = [round(math.pi/24,4)]
        #w_array = [0.0, 0.5, 1.0] #w is the weighting given to the directional bias (and hence (1-w) is the weighting given to correlated motion)
        w_array = [0.0]
        ratio_theta_s_brw_crw = 1
        plot_walks = 0
    
        for w_i in range(len(w_array)):
            w = w_array[w_i]
            for theta_s_i in range(len(theta_s_array)):
                theta_s_crw = np.multiply(ratio_theta_s_brw_crw,theta_s_array[theta_s_i])
                theta_s_brw = theta_s_array[theta_s_i]
                x,y, FoodsEaten = Straight(N, realizations, v, theta_s_crw, 
                                            theta_s_brw, w, self.FoodDistribution,
                                            self.eatRange, self.scentRange)

                if plot_walks == 1:
                    

                    fig = plt.figure()
                  
                    plt.title("w: " + str(w) + " theta: " + str(theta_s_array[theta_s_i]))
                    plt.plot(x.T, y.T, linewidth=0.75)
                    for val_x, val_y in self.FoodDistribution.values():
                        plt.scatter(val_x, val_y, color="blue", zorder=1)
                    plt.scatter([self.FoodDistribution[val][0] for val in FoodsEaten], [self.FoodDistribution[val][1] for val in FoodsEaten], color="red", zorder=2)
                    plt.axis('equal')
                    
                    plt.show()
                    
        #plt.figure()
        legend_array = []
        for theta_s_i in range(0, len(theta_s_array)):
            legend_array.append(["$\theta^{*CRW}=$", (ratio_theta_s_brw_crw*theta_s_array[theta_s_i]),"$\theta^{*BRW}=$",(theta_s_array[theta_s_i])])
        
        return len(FoodsEaten)/len(self.FoodDistribution.keys())



rdm_plt = Random_Walks_Python()

dists = ['random', 'uniform', 'cluster']

N = 100
fig = plt.figure()
ax = fig.add_subplot(111)

# TO DO: Consider what parameters to change/compare, clustered is the superior distribution with current code

randomHist =[]
uniformHist =[]
clusterHist =[]
for dist in dists:
    ratios = [0] * N
    rdm_plt.change_distribution(dist)
    for i in range(0,N):
        ratios[i] = rdm_plt.random_walks(i)
        if(dist == 'random'):
            randomHist.append(ratios[i])
        if(dist == 'uniform'):
            uniformHist.append(ratios[i])
        else:
            clusterHist.append(ratios[i]) 

print("random: ", sum(randomHist)/len(randomHist))
print("uniform: ", sum(uniformHist)/len(uniformHist))
print("cluster: ", sum(clusterHist)/len(clusterHist))
plt.hist([randomHist, uniformHist, clusterHist], bins=9, label=['random', 'uniform','cluster'])
plt.legend(loc='upper right')
plt.xlabel("% food discovered")
plt.show()







