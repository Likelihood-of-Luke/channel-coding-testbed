import methods
from models.graphModel import *
import methods
import numpy as np
import math

MAX_ITERS = 25

def _getLLR(x) -> float:
    px0 =  (1.0 + math.erf((x - 0.5) / math.sqrt(2.0))) / 2.0
    px1 = 1 - px0
    print("px0: " + str(px0) + " px1: " + str(px1))
    llrOut = math.log(px0/px1)
    return llrOut

def _updateVariableNodes(g, func):
    for v in g.variableNodes:
        v.beliefIn = []
        for cInd in g.variableEdges[str(v.getVariableNodeId())]:
            v.beliefIn.append(g.checkNodes[cInd].getBeliefOut(func))
        


def _updateCheckNodes(g, func):
    for c in g.checkNodes:
        c.probIn = []
        for vInd in g.checkEdges[str(c.getCheckNodeId())]:
            # print("checkNodeId" + str(c.getCheckNodeId()))
            # print("vInd" + str(vInd))qfunc vs error func
            c.probIn.append(g.variableNodes[vInd].getProbOut(func, vInd))

#Run message passing
def runLDPC(inVec, nodeFunc, checkFunc, soft):

    #Graph instance
    g = TannerGraph(pcMat = np.array([
                            [1, 1, 1, 0, 1, 0, 0], 
                            [0, 1, 1, 1, 0, 1, 0],
                            [1, 0, 1, 1, 0, 0, 1]
    ], dtype=int), func = methods.sumProductPerNode)

    #list/draw graph edges
    g.sayEdges()
    print(str(inVec))
    print(str(nodeFunc))
    iterations = 0

    #Initialise variable node probabilities to soft data inputs
    for idx, inRaw in enumerate(inVec):
        # VariableNode.setDataIn(g.variableNodes[idx], _getLLR(inRaw))
        g.variableNodes[idx].setDataIn(_getLLR(inRaw))

    #before the first iteration, set probOut to dataIn for all variableNodes
    for cN in g.checkNodes: 
        cN.setProbIn([g.variableNodes[i].getDataIn() for i in g.checkEdges[str(cN.getCheckNodeId())]])

    while iterations < MAX_ITERS:
        iterations += 1
        print("iteration: " + str(iterations) + "\n")

        #update LLRs
        _updateCheckNodes(g, nodeFunc)

        #check if done
        #prints decision vector
        done = g.checkDoneSoft(checkFunc)

        if done:
            g.decodeDone = True
            print("Decode done")
            return g.decisionVector
            break
        else:
            pass #If not done, iterate again
        #Finish decode
        if g.decodeDone:
            print("Decoding complete in %d iterations", iterations)

        #update exterior probablilities
        _updateVariableNodes(g, nodeFunc)


        #put some logic in here to track convergence
        ######

    return #did not decode within maxIters



