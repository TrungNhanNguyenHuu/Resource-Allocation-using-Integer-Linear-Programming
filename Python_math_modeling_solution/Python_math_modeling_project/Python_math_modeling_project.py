from pulp import *

# able to change parameter begin

## Two main sets 
#CUSTOMERS = [1,2,3,4,5]         # m customers
#WAREHOUSE = ['h1','h2','h3','h4','h5']    # n warehouses

## Parameters: demand (d_j), f_i, c_ij

#demand = {1 : 80,               # d_j
#          2 : 270,
#          3 : 250,
#          4 : 160,
#          5 : 180}  

#fixed_operating_cost = {'h1' : 1000,    # f_i
#                        'h2' : 1000,
#                        'h3' : 1000,
#                        'h4' : 1000,
#                        'h5' : 1000}

#transport_cost = {'h1':{1 : 4, 2 : 5, 3 : 6, 4 : 8, 5 : 10},        # c_ij
#                  'h2':{1 : 6, 2 : 4, 3 : 3, 4 : 5, 5 : 8},
#                  'h3':{1 : 9, 2 : 7, 3 : 4, 4 : 3, 5 : 4},
#                  'h4':{1 : 4, 2 : 5, 3 : 6, 4 : 8, 5 : 10},
#                  'h5':{1 : 4, 2 : 5, 3 : 6, 4 : 8, 5 : 10}}

########################################################################### 
CUSTOMERS = [1,2,3,4,5,6,7,8,9,10]         # m customers
WAREHOUSE = ['h1','h2','h3','h4','h5']    # n warehouses

demand = {1 : 30,               # d_j
          2 : 49,
          3 : 23,
          4 : 33,
          5 : 19,
          6 : 40,
          7 : 20,
          8 : 30,
          9 : 38,
          10 : 46}

fixed_operating_cost = {'h1' : 4.24,    # f_i
                        'h2' : 4.64,
                        'h3' : 1.52,
                        'h4' : 4.64,
                        'h5' : 3.52}

transport_cost = {'h1':{1 : 1.40, 2 : 1.64, 3 : 1.56, 4 : 3.64, 5 : 4.04, 6 : 3.84, 7 : 4.28, 8 : 2.76, 9 : 2.96, 10 : 2.12},        # c_ij
                  'h2':{1 : 2.12, 2 : 4.88, 3 : 2.68, 4 : 1.16, 5 : 3.96, 6 : 1.12, 7 : 3.76, 8 : 2.52, 9 : 2.80, 10 : 3.72},
                  'h3':{1 : 3.20, 2 : 4.84, 3 : 4.68, 4 : 4.40, 5 : 2.56, 6 : 2.12, 7 : 2.28, 8 : 4.08, 9 : 3.60, 10 : 3.64},
                  'h4':{1 : 4.84, 2 : 2.96, 3 : 4.16, 4 : 4.72, 5 : 3.64, 6 : 1.20, 7 : 4.80, 8 : 4.20, 9 : 3.84, 10 : 1.64},
                  'h5':{1 : 4.84, 2 : 4.20, 3 : 4.84, 4 : 3.72, 5 : 1.68, 6 : 1.40, 7 : 1.12, 8 : 1.76, 9 : 4.00, 10 : 1.48}}


# able to change paremeter end

# The total cost
total_cost = LpProblem("ILP",LpMinimize)

# x_ij , y_i
amount_sent = LpVariable.dicts("Amount",
                             [(j,i) for j in CUSTOMERS
                                    for i in WAREHOUSE],
                             0)

is_opened = LpVariable.dicts("Opened_Warehouse",WAREHOUSE,0,1,LpBinary)

#OBJECTIVE FUNCTION
total_cost += lpSum(fixed_operating_cost[i]*is_opened[i] for i in WAREHOUSE) + lpSum(transport_cost[i][j]*amount_sent[(j,i)] for i in WAREHOUSE for j in CUSTOMERS)

#CONSTRAINTS
for j in CUSTOMERS:
    total_cost += lpSum(amount_sent[(j,i)] for i in WAREHOUSE) == demand[j]                                             #Constraint 1

for i in WAREHOUSE:
    total_cost += lpSum(amount_sent[(j,i)] for j in CUSTOMERS) - is_opened[i]*lpSum(demand[j] for j in CUSTOMERS) <= 0      #Constraint 2

##for j in FACILITY:
##    prob += lpSum(serv_vars[(i,j)] for i in CUSTOMERS) <= maxam[j]*use_vars[j]

##for i in CUSTOMERS:
##    for j in FACILITY:
##        prob += serv_vars[(i,j)] <= demand[i]*use_vars[j]

#SOLUTION
total_cost.solve()
print("Status:",LpStatus[total_cost.status])

TOL = .00001
for i in WAREHOUSE:
    if is_opened[i].varValue > TOL:
       print("The opened warehouse is",i)

for v in total_cost.variables():
    print(v.name,"=",v.varValue)

#PRINT OPTIMAL SOLUTION
print("The total cost =",value(total_cost.objective))




    



    




     


