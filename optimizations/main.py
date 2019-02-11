from pulp import *
import networkx as nx,copy
from networkx.algorithms.approximation import *
from itertools import *


print("Welcome to Optimisation Coursework!")
print("This program can let you calculate Shannon Entropy, Fractional clique cover number and etc.")


help="""
HELP:


type:

`quit` to quit the program.

`clique NAME.bin` OR `clique N p` calculates the Fractional Clique Cover (FCC) [1] number of:

-> a graph named `NAME`.
-> a random graph with `N` amount of nodes and `p` probability of edge.

`shannon NAME.bin` OR `shannon ` calculates the Shannon Entropy (SE) [1] of

-> a graph named `NAME`.
-> a random graph with `N` amount of nodes and `p` probability of edge.

`check NAME.bin` calculates the SE and FCC of

-> a graph named `NAME`.
-> a random graph with `N` amount of nodes and `p` probability of edge.

and tells if its correct according to

shannon(G) + pi*(G)>= n  (where pi* is FCC, shannon is SE and n is node count) rule [1]

References:

[1] Maximilien Gadouleau. On the possible values of the entropy of undirected graphs. Journal of Graph Theory, 82:302–311, 2018.

you can type HELP anytime to call this.

"""
print(help)


answer=input("what would you like to do? [HELP, shannon .. , clique .., check .., quit]")
# while answer!="quit":
#     if answer.find("shannon")!=-1:
#     elif answer.find("clique")!=-1:
#     elif answer.find("check")!=-1:
#     elif answer.find("help")!=-1:
#     answer=input("what would you like to do? [HELP, shannon .. , clique .., check ..]")
