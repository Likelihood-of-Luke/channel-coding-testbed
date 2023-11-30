import numpy as np
import galois
import math
import functools
import operator
from models.graphModel import *

GF2 = galois.GF(2**1)

## ------------------------------------------ ##
## Node methods
## ------------------------------------------ ##

def sumProductPerNode(node: Node, priorNodeId: int = None) -> None:
    if isinstance(node, CheckNode):
        prod = functools.reduce(operator.mul, [np.tanh(p / 2) for p in node.probIn], 1)
        newBelief = math.log(
            (1 + prod)
            /(1 - prod)
        )
        node.setBeliefOut(newBelief)
        return newBelief
    elif isinstance(node, VariableNode):
        newProb = node.getDataIn() + sum([node.beliefIn if node.getNodeId() != priorNodeId else 0])
        node.setProbOut(newProb)
        return newProb
    else:
        raise TypeError
    return

def normalisedMinSum(cNode: CheckNode):

    return

def layeredMinSum(cNode: CheckNode):
    
    pass

## ------------------------------------------ ##
## Graph methods
## ------------------------------------------ ##

def checkLLRSign(g: TannerGraph) -> bool:
        # decisionVector = np.empty(shape=(1, g.pcMat.shape[1]), dtype=int) # hard bit decision vector
        for j in g.variableNodes:
            eij=0
            for i in g.checkNodes:
                eij += i.getBeliefOut(sumProductPerNode)
            if eij > 0:
                g.decisionVector[0,i.getVariableNodeId()] = int(1)
            else:
                g.decisionVector[0,i.getVariableNodeId()] = int(0)

        print("g.decisionVector = [" + str(g.decisionVector) + "]\n")

        syndrome = np.matmul(GF2(g.decisionVector), GF2(np.transpose(g.pcMat)))

        print("syndrome = " + str(syndrome))

        if(not syndrome.any()):
            return True
        else:
            return False