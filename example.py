
from VRP import VRP


def ReadData(First_file,Second_file):
  with open(First_file) as f:
        Number_vehicles, Number_customers,Number_depots = [int(x) for x in next(f).split()] # read first line
        Customers = []
        for line in f: # read rest of lines
             Customers.append([int(x) for x in line.split()])

  with open(Second_file) as f:
        Depots = []
        for line in f: # read rest of lines
             Depots.append([int(x) for x in line.split()])
  return Customers,Depots,Number_vehicles,Number_customers,Number_depots

if __name__ == '__main__':

    Customers,Depots,Number_vehicles,Number_customers,Number_depots=ReadData('Customers.txt','depots.txt')
    Vehicle_Routing_Problem=VRP(Depots,Customers,Number_vehicles,Number_customers,Number_depots)
    Vehicle_Routing_Problem.Run()















