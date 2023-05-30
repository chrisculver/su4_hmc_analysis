import matplotlib.pyplot as plt
import numpy as np
import math 
import jk
import os

#NT=48

def fold_corr(c, NT):
  hT=int(NT/2)
  res=[0 for t in range(hT)]
  for t in range(hT):
    if t==0 or t==NT/2:
      res[t]=c[t]
    else:
      res[t]=(c[t]+c[NT-t])/2.

  return res


def log_eff_mass(c):
  avg=np.mean(c, axis=0)
  res=[]
  for t in range(len(avg)-1):
    res.append(math.log(avg[t]/avg[t+1]))
  return res

def get_data(fileBase, gamma, NT):  
  data=[]
  with open(os.path.join(fileBase,'G{}.dat'.format(gamma))) as f:
    for line in f:
      cols=line.split()
      data.append(float(cols[1]))# we only need real part

  corrs=np.split(np.array(data),len(data)/NT)
  corrs=[fold_corr(c,NT) for c in corrs]

  return corrs

def plot_pion(fileBase,NT,cut=0,b=1):
  corrs=get_data(fileBase, 5, NT)
  corrs=corrs[cut+1:]
  # corrs is now a NT x NCFG array

  effMass=jk.jackKnife(log_eff_mass, corrs,b)
 # print(effMass)

  plt.errorbar([t for t in range(len(effMass[0]))], effMass[0], yerr=effMass[1], 
              linestyle="None", marker='o', markerfacecolor='None',
              label='G5')

def plot_rho(fileBase,NT,cut=0,b=1):
  idx=0
  for gamma in [1,2,3]:
    corrs=get_data(fileBase,gamma,NT)
    corrs=corrs[cut+1:]
    # corrs is now a NT x NCFG array

    effMass=jk.jackKnife(log_eff_mass, corrs, b)
   # print(effMass)

    plt.errorbar([t for t in range(len(effMass[0]))], effMass[0], yerr=effMass[1], 
                linestyle="None", marker='o', markerfacecolor='None',
                label='G{}'.format(idx))

    idx+=1
