import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections
from random_walks_02_28_19 import Random_Walks_Python

#Implements a biased a correlated random walk, I wish we workedo on this during this month.

def main():
    rdm_plt = Random_Walks_Python()

    dists = ['random', 'uniform', 'cluster']
    walks = ['CRW', 'BCRW_s', "Straight", "Straight_s"]
    N = 100
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #Remove # in the line below if you want to see the walk. It is recommended to reduce N first
    #rdm_plt.change_plot_walks()

    for walk in walks:

        randomHist = []
        uniformHist =[]
        clusterHist =[]

        for dist in dists:
            ratios = [0] * N
            rdm_plt.change_distribution(dist)
            for i in range(0,N):
                ratios[i] = rdm_plt.random_walks(walk)
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
        plt.ylabel("Count")

        if walk == "CRW":
            plt.title("Food found with CRW w/o scent")
        elif walk == "BCRW_s":
            plt.title("Food found with BCRW with scent")
        elif walk == "Straight":
            plt.title("Food found with Straight w/o scent")
        elif walk == "Straight_s":
            plt.title("Food found with Straight with scent")
        else:
            plt.title("Not found")

        #plt.savefig("./figures/Straight_smell.png")
        plt.show()

if __name__ == "__main__":
    main()
