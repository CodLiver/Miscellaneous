from pulp import *
import networkx as nx,copy,random,time
from networkx.algorithms.approximation import *
from itertools import *
from fractions import *


def loadGraph(name):
    #read
    with open(name+".graph","r") as f:
        data=f.readlines()
        G=nx.Graph().to_undirected()
        N=len(eval(data[0]))
        edges=eval(data[1])
        for each in range(N):
            G.add_node(each)
        for each in edges:
            G.add_edge(each[0],each[1])

    print(G.nodes(),G.edges)
    return G


def randomGraph(N,p):
    G=nx.Graph().to_undirected()
    for each in range(N):
        G.add_node(each)
        for eacher in range(each+1,N):
            if random.random()<p:
                G.add_edge(each,eacher)

    print(G.nodes(),G.edges)
    return G

def manualGraph(N):
    G=nx.Graph().to_undirected()
    man="""
    to create graphs randomly put each node's number
    to have edge with current node and put space
    You dont need to put lower number as the graph is undirected. e.g when the counter hits the last one.

    e.g
    0: 1 2 3
    1: 3 5 4
    2: 3 5
    3: 5
    4:
    5: 6
    ..
    -------
    """
    print(man)
    for each in range(N):
        G.add_node(each)
        nodesIN=input(str(each)+": ").split(" ")
        if len(nodesIN)>0 and nodesIN[0]!="":
            for eachEdge in nodesIN:
                G.add_edge(each,int(eachEdge))

    print(G.nodes(), G.edges)
    #     G.add_node(each)
    #     for eacher in range(each+1,N):
    #         if random.random()<p:
    #             G.add_edge(each,eacher)

    return G


def exportG(G):
    yn=input("Do you want to export this graph? Y/n ")
    if yn=="Y":
        name=input("name (without extenstion (.graph will be added))? ")
        with open(name+".graph","a+") as f:
            f.write(str(G.nodes())+"\n"+str(G.edges))



def AddGraph(answer):
    if answer[2]=="-m":
        G=manualGraph(int(answer[1]))
        exportG(G)
        return G
    elif answer[2]=="-ld":
        return loadGraph(answer[1])
    elif len(answer)==3:
        G=randomGraph(int(answer[1]),float(answer[2]))
        exportG(G)
        return G
    else:
        return None

def shannon(G,fulRes):
    print()
    print("calculating shannon entropy..")
    print()

    starting=time.time()

    nodeList=G.nodes()

    subsets=list(chain.from_iterable(combinations(range(len(nodeList)), size) for size in range(0,len(range(len(nodeList))))))#subsetCreator(range(len(nodeList)))
    subsets=[frozenset(e) for e in subsets]+[frozenset(nodeList)]
    initVarList = LpVariable.dicts("subsets",range(len(subsets)),lowBound=0)
    # print(subsets)
    subCond2=set()
    varSet2=[]
    for each in (nodeList):
        changed=len(subCond2)
        n=frozenset(G.neighbors(each))
        neach=frozenset(list(n)+[each])
        subCond2.add(frozenset([neach,n]))
        if changed!=len(subCond2):
            varSet2.append([initVarList[subsets.index(neach)],initVarList[subsets.index(n)]])

    # cond2=subCond2

    if len(nodeList)>=8:
        c2=time.time()
        print("condition 2 finished:",round(c2-starting,3),"sec")
        print()


    # subCond3=set()#del
    # varSet3=[]#del
    #subCond4=set()
    varSet4=[]

    # print("len of subs",len(subsets))
    for eachS in range(1,len(subsets)-1):#S
        # print(eachS)
        for eachT in range(eachS+1,len(subsets)-1):#T
            s=subsets[eachS]
            t=subsets[eachT]
            # query=frozenset([t,s])#del---
            # if s.issubset(t) and not query in subCond2 and len(query)>1:
            #     changed=len(subCond3)
            #     subCond3.add(query)
            #     if changed!=len(subCond3):
            #         varSet3.append([initVarList[subsets.index(t)],initVarList[subsets.index(s)]])#del----
            # ???????????????????????????????????????????????????

            # if s.issubset(t):
            #     query=frozenset([t,s])
            #     if not query in cond2 and len(query)>1:
            #         changed=len(subCond3)
            #         subCond3.add(query)
            #         if changed!=len(subCondr3):
            #             varSet3.append([initVarList[subsets.index(t)],initVarList[subsets.index(s)]])

            ##4th cond
            if not s.issubset(t):
                u=s.union(t)
                inter=s.intersection(t)
                #query=frozenset([s,t,u,inter])
                #if not len(query)<=2:
                    #changed=len(subCond4)
                #subCond4.add(query)
                    #if changed!=len(subCond4):
                varSet4.append([initVarList[subsets.index(s)],initVarList[subsets.index(t)],initVarList[subsets.index(u)],initVarList[subsets.index(inter)]])

    if len(nodeList)>=8:
        c34=time.time()
        print("condition 4 finished in:",round(c34-c2,3),"sec")
        print()
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
    # for each in varSet3:#del
    #     prob+= each[0]-each[1]>=0#del

    #cond3
    for each in varSet4:
        prob+= each[0]+each[1]-each[2]-each[3]>=0

    if len(nodeList)>=8:
        print("LP problem was created in",round(time.time()-c34,3),"sec")
        print()
    # print("cond done")


    # print(prob)
    status = prob.solve()

    print("status:",LpStatus[prob.status])
    print()
    # print(Fraction(1/(Fraction(str(round(1/(lpSum(varSet).value()),5))))))

    resultLP=initVarList[len(initVarList)-1].value()

    if fulRes=="Y":
        for variable in prob.variables():
            print("{} = {}".format(list(subsets[int(variable.name[8:])]), Fraction(variable.varValue).limit_denominator(100)))

    print("result: ",Fraction(resultLP).limit_denominator(100))
    print()
    print("overall fin in",round(time.time()-starting,3),"secs")
    print()

    return resultLP


def clique(G,fulRes):
    print()
    print("solving clique problem")
    starting=time.time()
    cliques=[set(s) for s in nx.enumerate_all_cliques(G)]
    totsubset=set(frozenset(list(G.neighbors(each))+[each]) for each in range(0,len(G)))

    initVarList = LpVariable.dicts("cliques",range(len(cliques)),lowBound=0)

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
    print()
    print("status:",LpStatus[prob.status])

    resultLP=lpSum(varSet).value()

    if fulRes=="Y":
        for variable in prob.variables():
            print("{} = {}".format(list(cliques[int(variable.name[8:])]), Fraction(variable.varValue).limit_denominator(100)))

    print()
    print("result: ",Fraction(resultLP).limit_denominator(100))
    print()
    print("finished in",round(time.time()-starting,3),"secs")

    return resultLP


print("Welcome to Optimisation Coursework!")
print("This program can let you calculate Shannon Entropy, Fractional clique cover number and etc.")


help="""
help:


type:

`quit` to quit the program.

`clique NAME -ld` OR `clique N p` OR `clique N -m` calculates the Fractional Clique Cover (FCC) [1] number of:

-> a graph named `NAME` to load the graph (without extention (.graph will be added)).
-> a random graph with `N` amount of nodes and `p` probability of edge.
-> `-m` is to create graph manually instead of randomly.

`shannon NAME -ld` OR `shannon N p` OR `shannon N -m` calculates the Shannon Entropy (SE) [1] of

-> a graph named `NAME` to load the graph (without extention (.graph will be added)).
-> a random graph with `N` amount of nodes and `p` probability of edge.
-> `-m` is to create graph manually instead of randomly.

`check NAME -ld` OR `check N p` OR `check N -m` calculates the SE and FCC of

-> a graph named `NAME` to load the graph (without extention (.graph will be added)).
-> a random graph with `N` amount of nodes and `p` probability of edge.
-> `-m` is to create graph manually instead of randomly.

and tells if its correct according to

shannon(G) + pi*(G)>= n  (where pi* is FCC, shannon is SE and n is node count) rule [1]

PS: An acceptable graph input:
g1.graph:
[0,1,2,3,4]
[(0,1),(2,3),(3,4)]

so it is advisable that you create graphs manually first, save it, then load it with the command line here.

References:

[1] Maximilien Gadouleau. On the possible values of the entropy of undirected graphs. Journal of Graph Theory, 82:302–311, 2018.

you can type `help` anytime to call this. or type `q` to quit

"""

print(help)
def main():

    try:

        answer=input("what would you like to do? [help, shannon .. , clique .., check .., q] ").split(" ")
        while answer!="q":
            if answer[0].lower()=="shannon":
                while len(answer)!=3:
                    answer=input("Incorrect shannon commandline, please try `shannon NAME.graph -ld` OR `shannon N p` OR `shannon N -m`").split(" ")
                fulRes=input("Do you want full variable's result?[Y/n] ")
                G=AddGraph(answer)#randomGraph(5,0.4)
                shannon(G,fulRes)
            elif answer[0].lower()=="clique":
                while len(answer)!=3:
                    answer=input("Incorrect clique commandline, please try `clique NAME.graph -ld` OR `clique N p` OR `clique N -m`").split(" ")
                fulRes=input("Do you want full variable's result?[Y/n] ")
                G=AddGraph(answer)#randomGraph(5,0.4)
                clique(G,fulRes)
            elif answer[0].lower()=="check":
                while len(answer)!=3:
                    answer=input("Incorrect check commandline, please try `check NAME.graph -ld` OR `check N p` OR `check N -m`").split(" ")
                fulRes=input("Do you want full variable's result?[Y/n] ")
                G=AddGraph(answer)#randomGraph(5,0.4)
                pi=clique(G,fulRes)
                n=shannon(G,fulRes)

                print("shannon + clique* >= nodeAmount")
                print(Fraction(n).limit_denominator(100),"+",Fraction(pi).limit_denominator(100),">=",len(G.nodes()),"satisfies:",Fraction(pi+n).limit_denominator(100)>=(len(G.nodes())))
            elif answer[0].lower()=="help":
                print(help)
            elif answer[0].lower()=="q":
                break
            answer=input("what would you like to do? [help, shannon .. , clique .., check .., q] ").split(" ")
    except: #e
        # print(e)
        print("Incorrect sequence, please refer `help`. Check if any typos or the graph name entered correctly.")
        main()

main()
