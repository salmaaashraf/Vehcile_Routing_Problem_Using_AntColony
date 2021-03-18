import math
import random as rn
import numpy as np
from numpy.random import choice as np_choice


class AntColony1(object):

    def __init__(self, distances, n_ants,n_best ,n_iterations, decay, start,alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
        """
        self.distances = distances
        # np.array return numpy.array with the same shape ,all it's elements initialized to one
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.start=start

    def run(self):
        min = math.inf
        shortest_path = None
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths,self.n_best)
            sum=0
            for j in range(len(all_paths)):
                sum=sum+all_paths[j][1]
            if sum < min:
                min= sum
                all_time_shortest_path=all_paths
            self.pheromone * self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best):
        #sort allpaths by index 1 meaning by the cost of path
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]


    def gen_all_paths(self):
        all_paths = []
        visited = set()
        visited.add(self.start)
        x=int((len(self.distances)-1)/self.n_ants)
        num=[int((len(self.distances)-1)/self.n_ants) for i in range(self.n_ants)]
        reminder=(len(self.distances)-1)%self.n_ants
        j=0
        for i in range(reminder):
            num[j]=1+num[j]
            j+=1
        for i in range(self.n_ants):
            if num[i]==0:
                break
            path = self.gen_path(visited,num[i])
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_path(self, visited,n):

        path = []
        prev = self.start
        for i in range(n):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, self.start))  # going back to where we started
        return path

    def pick_move(self, pheromone, dist, visited):
        # here we use this line to avoid any change in the reference array
        pheromone = np.copy(pheromone)
        #to make a probabilty being zero for those nodes which is already visited
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        norm_row = row / row.sum()
        # here we pick a random number from the nodes ,according to it's probapilities and using direct access as the choice function return list not element
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move
