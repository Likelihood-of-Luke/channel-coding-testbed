#initialize
import numpy as np
from abc import ABC, abstractmethod

#Tanner Graph class
class TannerGraph:
    
    decodeDone = False
    checkNodes = []
    variableNodes = []
    data = []
    checkEdges = dict()
    variableEdges = dict()
    
    def __init__(self, pcMat, func):
        self.pcMat = pcMat
        self.decisionVector = np.empty(shape=(1, self.pcMat.shape[1]), dtype=int) # hard bit decision vector

        for i in range(pcMat.shape[0]):
            for j in range(pcMat.shape[1]):
                if pcMat[i][j] == 1:
                    if str(i) in self.checkEdges:
                        self.checkEdges["{}".format(i)].append(j)
                    else:
                        self.checkEdges["{}".format(i)] = [j]
                    
                    if str(j) in self.variableEdges:
                        self.variableEdges["{}".format(j)].append(i)
                    else:
                        self.variableEdges["{}".format(j)] = [i]
        
        for n in np.sort([key for key in self.variableEdges]):
            self.variableNodes.append(VariableNode())
        
        for m in np.sort([key for key in self.checkEdges]):
            self.checkNodes.append(CheckNode())
        return
        
    def sayEdges(self) -> str:
        print("checkEdges:" + str(self.checkEdges) + " variableEdges:" + str(self.variableEdges))
        return
    
    def sayNodes(self) -> str:
        print("checkNodes:" + str(self.checkNodes) + " variableNodes:" + str(self.variableNodes))
        return

    def draw():
        ...
        #networkX?

    def checkDoneSoft(self, func) -> bool:
        return func(self)
     
#Node (super)class
class Node(ABC):
    nodeType = 'genericNode'
    nodeId = 0
    
    @abstractmethod
    def sayNodeId(self) -> None:
        pass
    
    @abstractmethod
    def getNodeId(self) -> str:
        pass
    
    @abstractmethod    
    def sayNodeType(self) -> None:
        pass
    
    @abstractmethod    
    def getNodeType(self) -> str:
        pass
    
    def __init__(self):
        self.nodeId = Node.nodeId
        Node.nodeId += 1
    
#Node subclass
class VariableNode(Node):
    
    nodeType = 'variableNode'
    dataIn = 0
    beliefIn = []
    # probOut = []
    variableNodeId = 0
    
    def __init__(self):
        super().__init__()
        self.variableNodeId = VariableNode.variableNodeId
        VariableNode.variableNodeId += 1
    
    def setDataIn(self, d: float) -> None:
        self.dataIn = d # float
        return

    def getDataIn(self) -> float:
        return self.dataIn # float
        
    def sayNodeId(self) -> None:
        print(self.nodeId)
        return
    
    def getNodeId(self) -> str:
        return self.nodeId

    def getVariableNodeId(self) -> str:
        return self.variableNodeId
    
    def sayNodeType(self) -> None:
        print(self.nodeType)
        return
    
    def getNodeType(self) -> str:
        return self.nodeType
    
    def sayVariableNodeId(self) -> None:
        print(self.variableNodeId)

    def setBeliefIn(self, p: list) -> None:
        self.beliefIn = p
        return

    def getProbOut(self, func, askingCheckNode) -> float:
        return func(self, askingCheckNode) # Depends who's asking...

    def setProbOut(self, prob) -> None:
        self.probOut = prob
        return
    
        
#Node subclass
class CheckNode(Node):
    
    nodeType = 'checkNode'
    probIn = []
    beliefOut = 0
    checkNodeId = 0
    
    def __init__(self):
        super().__init__()
        self.checkNodeId = CheckNode.checkNodeId
        CheckNode.checkNodeId += 1
        
    def sayNodeId(self):
        print(self.nodeId)
        
    def sayNodeType(self):
        print(self.nodeType)
        
    def getNodeId(self):
        return self.nodeId
    
    def getNodeType(self):
        return self.nodeType
    
    def sayCheckNodeId(self):
        print(self.checkNodeId)

    def getCheckNodeId(self):
        return self.checkNodeId

    def setProbIn(self, p: list) -> None:
        self.probIn = p
        return

    def getBeliefOut(self, func) -> float:
        return func(self)
    
    def setBeliefOut(self, newBelief) -> None:
        self.beliefOut = newBelief
        return

