import matplotlib.pyplot as plt
import math
import numpy as np
import random
import pylab
import collections
from random_walks_02_28_19 import Random_Walks_Python

def main():
    rdm_plt = Random_Walks_Python()

    dists = ['random', 'uniform', 'cluster']
    walks = ['BCRW', 'BCRW_s', "Straight", "Straight_s"]
    N = 100
    fig = plt.figure()
    ax = fig.add_subplot(111)

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
        plt.hist([randomHist, uniformHist, clusterHist], bins=9, label=['random', 'uniform','cluster'], density=True)
        plt.legend(loc='upper right')
        plt.xlabel("% food discovered")
        plt.ylabel("% of time food ratio found")
        if walk == "BCRW":
            plt.title("Food found with BCRW w/o scent")
        if walk == "BCRW_s":
            plt.title("Food found with BCRW with scent")
        if walk == "Straight":
            plt.title("Food found with Straight w/o scent")
        if walk == "Straight_s":
            plt.title("Food found with Straight with scent")

        plt.show()

if __name__ == "__main__":
    main()