import math

import numpy
import numpy as np
from Ant_Colony import AntColony1


class VRP:
    def __init__(self,CoordDepots,CoordCustomers,n_vechicles,n_customers,n_depots):
        self.CoordDepots=CoordDepots
        self.CoordCustomers=CoordCustomers
        self.n_vechicles=n_vechicles
        self.n_customers=n_customers
        self.n_depots=n_depots
        return

    def AssignDepots(self):
        depot = list([] for val in range(self.n_depots))
        for i in range(len(self.CoordCustomers)):
            min= math.inf
            for j in range(len(self.CoordDepots)):
                d=pow(self.CoordCustomers[i][1]-self.CoordDepots[j][0], 2)+pow(self.CoordCustomers[i][2]-self.CoordDepots[j][1], 2)
                d=math.sqrt(d)
                if(d<min):
                    min=d
                    no_depot=j
            if(no_depot!=-1):
                depot[no_depot].append(self.CoordCustomers[i][0])

        return depot


    def AssignVehicles(self):
        num=int(self.n_vechicles / self.n_depots)
        reminder=self.n_vechicles % self.n_depots
        NoOfVeh= list([num for i in range(self.n_depots)])
        j=0
        for i in range(reminder):
            NoOfVeh[j]+=1
            j+=1

        return NoOfVeh

    def CreateGraph(self,depot_no,cunstomers_no):
        graph=list([] for val in range(len(cunstomers_no)+1))


        for i in range(len(cunstomers_no)+1):

            if i==0:
              graph[0].append(math.inf)
            else:
             graph[0].append(
             pow(self.CoordCustomers[i-1][1] - self.CoordDepots[depot_no][0], 2) + pow(
             self.CoordCustomers[i-1][2] - self.CoordDepots[depot_no][1], 2))
             graph[0][i] == math.sqrt(graph[0][i])
        for i in range(len(cunstomers_no)):
            graph[i+1].append(graph[0][i+1])
            for j in range(len(cunstomers_no)):
                if i==j:
                    graph[i+1].append(numpy.inf)
                else :
                   graph[i+1].append( pow(self.CoordCustomers[i][1] - self.CoordCustomers[j][1], 2) + pow(
                    self.CoordCustomers[i][2] - self.CoordCustomers[j][2], 2))
                   graph[i+1][j] = math.sqrt(graph[i+1][j])
        return graph

    def Run(self):

        # get the customers of each depot
        depot=self.AssignDepots()
        # get the number of vehicles in each depot
        Vehicles=self.AssignVehicles()
        Vehicle_Number=1
        Depot_Number=1
        #for every depot
        for i in range(self.n_depots):
            print("Depot Number ",Depot_Number)
            Distances=np.array(self.CreateGraph(i,depot[i]))
            ant_colony=AntColony1(Distances,Vehicles[i],10,100,0.95,0)
            #get shortest path
            shortest_path = ant_colony.run()

            if len(shortest_path)>1 :

               for n in shortest_path:
                  print("Vehicle Number ",Vehicle_Number)
                  print("shorted_path: {}".format(n))
                  Vehicle_Number+=1
            else:
                print("Vehicle Number ",Vehicle_Number)
                print ("shorted_path: {}".format(shortest_path))
                Vehicle_Number+=1
            Depot_Number+=1
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        return
