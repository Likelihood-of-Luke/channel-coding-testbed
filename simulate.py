import runner
import methods
import numpy as np



inp = [-1, 1.4, 0.85, 0.6, 0, 0.8, -0.41]



runner.runLDPC(np.array([runner._getLLR(i) for i in inp]), methods.sumProductPerNode, methods.checkLLRSign, True)
    

