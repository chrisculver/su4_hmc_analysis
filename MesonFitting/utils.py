import matplotlib.pyplot as plt
import numpy as np
import math 
import jk
import os
import lsqfit


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
    res.append(np.log(avg[t]/avg[t+1]))
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



def cosh_fit(t,p,NT):
    return p['a']*np.cosh(p['E']*(t-(NT/2)))

def single_exp(t,p):
    return p['a0']*np.exp(-p['E0']*t)

def three_exp(t,p):
    return p['a0']*np.exp(-p['E0']*t)+p['a1']*np.exp(-p['E1']*t)+p['a2']*np.exp(-p['E2']*t)

def get_best_cosh_fit(fitData, NT):
    cosh_nt = lambda x,p : cosh_fit(x,p,NT)
    ts = np.array([t for t in range(int(NT/2))])

    bestFit =   fit=lsqfit.nonlinear_fit(
                    data=(ts[1:32+1],fitData[0][1:32+1],fitData[1][1:32+1,1:32+1]),
                    fcn=cosh_nt,
                    p0={'a': 1.0, 'E': 0.2}
                )
    bestFitTimes = [1,32]

    for ti in range(1,22):
        for tf in range(26,32):
            if tf-ti>2:

                fit=lsqfit.nonlinear_fit(
                        data=(ts[ti:tf+1],fitData[0][ti:tf+1],fitData[1][ti:tf+1,ti:tf+1]),
                        fcn=cosh_nt,
                        p0={'a': 1.0, 'E': 0.2} 
                    )
                if fit.chi2 < bestFit.chi2:
                    bestFit=fit
                    bestFitTimes=[ti,tf]
    
    return bestFit, bestFitTimes

def get_best_exp_fit(fitData, NT):
    ts = np.array([t for t in range(int(NT/2))])

    bestFit =   fit=lsqfit.nonlinear_fit(
                    data=(ts[1:32+1],fitData[0][1:32+1],fitData[1][1:32+1,1:32+1]),
                    fcn=three_exp,
                    p0={'a0': 1.0, 'E0': 0.2, 'a1': 0.001, 'E1': 0.05, 'a2': 0.1, 'E2': 2.2}
                )
    bestFitTimes = [1,32]

    for ti in range(1,12):
        for tf in range(22,32):
            if tf-ti>2:

                fit=lsqfit.nonlinear_fit(
                        data=(ts[ti:tf+1],fitData[0][ti:tf+1],fitData[1][ti:tf+1,ti:tf+1]),
                        fcn=three_exp,
                        p0={'a0': 1.0, 'E0': 0.2, 'a1': 0.001, 'E1': 0.05, 'a2': 0.1, 'E2': 2.2}
                    )
                if fit.chi2 < bestFit.chi2:
                    bestFit=fit
                    bestFitTimes=[ti,tf]
    
    return bestFit, bestFitTimes