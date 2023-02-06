import matplotlib.pyplot as plt
import matplotlib as mpl

class EnsembleDatabase:
    def __init__(self, data):
        self.data=data

    def filter(self,s):
        return EnsembleDatabase({key: self.data[key] for key in self.data if s in key})



def meson_vs_kappa(db,mesonKey):
    lst={}
    for k,v in db.items():
        strTerms=k.split('/')
        kappa=float(strTerms[8][1:].replace('p','.'))
        if mesonKey in v:
            lst[kappa]={'avg': v[mesonKey]['avg'], 'err': v[mesonKey]['err']}
        else:
            lst[kappa]={'avg': 0, 'err': 0}
    return lst



def efm_trajectory(db, beta, fermion, pionKey, rhoKey, marker=None):
    betaDictionaries = db.filter(beta).filter(fermion).data

    pionData = meson_vs_kappa(betaDictionaries, pionKey)
    rhoData = meson_vs_kappa(betaDictionaries, rhoKey)

    getAvg = lambda data : [data[key]['avg'] for key in data]
    getErr = lambda data : [data[key]['err'] for key in data]

    if not marker:
        marker='o'

    plt.errorbar(pionData.keys(), getAvg(pionData), getErr(pionData),
        linestyle="None",marker=marker,markerfacecolor="None",
        label='pion'
    )
    plt.errorbar(rhoData.keys(), getAvg(rhoData), getErr(rhoData),
        linestyle="None",marker=marker,markerfacecolor="None",
        label='rho'
    )

    plt.ylabel('aE')
    plt.xlabel('kappa')
    plt.title('wilson fermions, beta={}'.format(beta))
    plt.legend()