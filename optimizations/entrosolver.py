from pulp import *
import networkx as nx,copy
from networkx.algorithms.approximation import *
from fractions import Fraction
from itertools import *


"""
rules:
1) if two compared element same, dont add.
2) except 2nd condition, if has empty element. ignore
3) if 3rd cond comp same in 2, ignore.
4) set of union, int, with a,b ==2, ignore.
5) always go n, n+1 for 4.
6) dont do it with topset. after 2.
7) no need for 5.nd cond
8) embed cond 1

"""


def subsetCreator(totalList):
    return list(chain.from_iterable(combinations(totalList, size) for size in range(0,len(totalList))))
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

#triangle broken
# G.add_node(0)
# G.add_node(1)
# G.add_node(2)
# G.add_edge(0,1)
# G.add_edge(1,2)
# G.add_edge(2,0)



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



nodeList=G.nodes()

subsets=subsetCreator(range(len(nodeList)))
subsets=[frozenset(e) for e in subsets]+[frozenset(nodeList)]
initVarList = LpVariable.dicts("subsets",range(len(subsets)),lowBound=0)

subCond2=set()
varSet2=[]
for each in (nodeList):
    changed=len(subCond2)
    n=frozenset(G.neighbors(each))
    neach=frozenset(list(n)+[each])
    subCond2.add(frozenset([neach,n]))
    if changed!=len(subCond2):
        varSet2.append([initVarList[subsets.index(neach)],initVarList[subsets.index(n)]])

cond2=subCond2

subCond3=set()
varSet3=[]
subCond4=set()
varSet4=[]
for eachS in range(1,len(subsets)-1):#S
    for eachT in range(eachS+1,len(subsets)-1):#T
        s=subsets[eachS]
        t=subsets[eachT]
        query=frozenset([t,s])
        if s.issubset(t) and not query in cond2 and len(query)>1:
            changed=len(subCond3)
            subCond3.add(query)
            if changed!=len(subCond3):
                varSet3.append([initVarList[subsets.index(t)],initVarList[subsets.index(s)]])
        ##4th cond
        u=s.union(t)
        inter=s.intersection(t)
        query=frozenset([s,t,u,inter])
        if not len(query)<=2:
            changed=len(subCond4)
            subCond4.add(query)
            if changed!=len(subCond4):
                varSet4.append([initVarList[subsets.index(s)],initVarList[subsets.index(t)],initVarList[subsets.index(u)],initVarList[subsets.index(inter)]])

# cond3=subCond3
# print("c3",cond3)
# print("vs3",varSet3)
# cond4=subCond4
# print("c4",cond4)
# print("vs4",varSet4)
# print("set done")


prob = LpProblem("Maximum Shannon Entropy", LpMaximize)
prob+= initVarList[len(initVarList)-1], "objective func"
prob+= initVarList[0]==0, "empty set const"

#cond1
for each in range(1,len(nodeList)+1):
    prob+= initVarList[each]<=1

#cond2
for each in varSet2:
    prob+= each[0]-each[1]==0

#cond2
for each in varSet3:
    prob+= each[0]-each[1]>=0

#cond3
for each in varSet4:
    prob+= each[0]+each[1]-each[2]-each[3]>=0

# print("cond done")
status = prob.solve()

print("status:",LpStatus[prob.status])

# print(Fraction(1/(Fraction(str(round(1/(lpSum(varSet).value()),5))))))
print(initVarList[len(initVarList)-1].value())
# print(Fraction(1/(Fraction(str(round(1/(initVarList[len(initVarList)-1].value()),2))))))
# for variable in prob.variables():
#     if variable.varValue>0:
#         print("{} = {}".format(variable.name, Fraction(1/(Fraction(str(round(1/(lpSum(variable.varValue).value()),5)))))))
#
#     else:
#         print("{} = {}".format(variable.name, variable.varValue))


# for variable in prob.variables():
# #     print(list(subsets[int(variable.name[8:])]),variable.varValue)
#     print("{} = {}".format(variable.name, variable.varValue))
