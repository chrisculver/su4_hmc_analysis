import numpy as np
import math

def log_effective_mass(corr):
    avg=np.mean(corr, axis=0)
    res=[]

    for t in range(len(avg)-1):
        try:
            res.append(math.log(avg[t]/avg[t+1]))
        except ValueError:
            res.append(-1j*math.pi + math.log(-avg[t]/avg[t+1]))
        except: 
            raise
    
    return res


def cosh_effective_mass(corr):
    avg=np.mean(corr, axis=0)
    res=[]

    for t in range(len(avg)-1):
        try: 
            res.append(np.cosh()