import numpy as np
import math 


def jackKnifeSamples(data, b=1):
  N=len(data)
  if not (N/b).is_integer():
    print('Binning data error, len(data)={} and bin size ={}'.format(N,b))
    raise ValueError

  indices=np.arange(N)
  bins=np.split(indices, N/b)
#  print(bins) 
  jackKnifeSamples=[]
  for b in bins:
    jackKnifeSamples.append([e for i,e in enumerate(data) if i not in b])

  return jackKnifeSamples


def jackKnife(func, data, b=1):
  samples=jackKnifeSamples(data,b)
  vals=[func(s) for s in samples]
  N=len(vals)
  var=np.var(vals, axis=0)

  return (np.mean(vals, axis=0), np.sqrt(var*(N-1.)))


def jackKnifeCov(func, data, b=1):
  samples=[jackKnifeSamples(d,b) for d in data]
  vals=[[func(s) for s in var] for var in samples]
  
  # adding bias is true and a factor of (N-1) 
  # has cov match regular jckknife variance
  return [[np.mean(v) for v in vals], np.cov(vals,bias=True)*(len(vals[0])-1)]



#data1=[1.1,1.0,1.2,1.5,1.2,1.3]
#data2=[2.4,2.3,2.6,2.9,2.4,2.4]


#print(jackKnife(np.mean, data1, 1))
#print(jackKnife(np.mean, data1, 2))
#print(jackKnife(np.mean, data1, 3))
#print()
#cov1=jackKnifeCov(np.mean, [data1, data2], 1)
#cov2=jackKnifeCov(np.mean, [data1, data2], 2)
#cov3=jackKnifeCov(np.mean, [data1, data2], 3)

#print(cov1)
#print(math.sqrt(cov1[1][0,0]),"  ", math.sqrt(cov1[1][1,1]))
#print()
#print(cov2)
#print(math.sqrt(cov2[1][0,0]),"  ", math.sqrt(cov2[1][1,1]))
#print()
#print(cov3)
#print(math.sqrt(cov3[1][0,0]),"  ", math.sqrt(cov3[1][1,1]))


  
  
