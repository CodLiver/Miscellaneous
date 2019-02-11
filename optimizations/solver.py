import networkx as nx,copy
from networkx.algorithms.approximation import *
from pulp import *
from fractions import Fraction

G=nx.Graph().to_undirected()
#2d
# G.add_node(0)
# G.add_node(1)
# G.add_edge(0,1)
#triangle
# G.add_node(0)
# G.add_node(1)
# G.add_node(2)
# G.add_edge(0,1)
# G.add_edge(1,2)
# G.add_edge(2,0)
#square
# G.add_node(0)
# G.add_node(1)
# G.add_node(2)
# G.add_node(3)
# G.add_edge(0,1)
# G.add_edge(0,2)
# G.add_edge(0,3)
# G.add_edge(1,2)
# G.add_edge(1,3)
# G.add_edge(2,3)

#penta
# G.add_node(0)
# G.add_node(1)
# G.add_node(2)
# G.add_node(3)
# G.add_node(4)
# G.add_edge(0,1)
# G.add_edge(0,4)
# G.add_edge(1,2)
# G.add_edge(2,3)
# G.add_edge(3,4)

#max paper
G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)

G.add_edge(0,1)
G.add_edge(0,4)
G.add_edge(0,5)
G.add_edge(1,2)
G.add_edge(1,5)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(3,6)
G.add_edge(5,6)

cliques=[set(s) for s in nx.enumerate_all_cliques(G)]
totsubset=set(frozenset(list(G.neighbors(each))+[each]) for each in range(0,len(G)))

initVarList = LpVariable.dicts("clique",range(len(cliques)),lowBound=0)

# checker={}
# ptr=0
# for eachh in cliques:
#     checker[ptr]=eachh
#     ptr+=1
# print("checkerInd",checker)

assignment={}
ptr=0
varSet=set([])
for each in totsubset:
    subassignment=[]
    subset=set([])
    for eacher in range(len(cliques)-1,-1,-1):
        if cliques[eacher].issubset(each) and not cliques[eacher].issubset(subset):
            subassignment.append(initVarList[eacher])
            varSet.add(initVarList[eacher])
            subset|= cliques[eacher]
            if subset==each:
                break
    if not subassignment==[]:
        assignment[ptr]=subassignment
        ptr+=1

prob = LpProblem("mininum clique cover number", LpMinimize)
prob+= lpSum(varSet), "objective func"
prob+= lpSum(varSet)>=1, "objective const"
for eachSet in varSet:
    prob+=eachSet>=0
for eachNode in assignment:
    prob+=lpSum(assignment[eachNode])>=1

status = prob.solve()
print("status:",LpStatus[prob.status])


print("result: ",lpSum(varSet).value())
# print(Fraction(1/(Fraction(str(round(1/(lpSum(varSet).value()),5))))))
# print("result: ",Fraction())

for variable in prob.variables():
    if variable.varValue>0:
        print("{} = {}".format(variable.name, Fraction(1/(Fraction(str(round(1/(lpSum(variable.varValue).value()),5)))))))

    else:
        print("{} = {}".format(variable.name, variable.varValue))
