from imports import *

def mi(x, y, bins=10):
    ret = pd.DataFrame(0, x.columns, y.columns)
    for i in range(len(x.columns)):
        for j in range(len(x.columns)):
            ret.iloc[i, j] = calcMi(x.iloc[:, i], y.iloc[:, j], bins)
    return ret

def calcMi(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    return mutual_info_score(None, None, contingency=c_xy)

def mixedCLR(miStat, miDyn):
    zrDyn = miDyn.apply(toZscore, 0)
    zrDyn[zrDyn < 0] = 0
    zcMix = miDyn
    for j in range(len(miStat.columns)):
        zcMix.iloc[:, j] = (zcMix.iloc[:, j] - miStat.iloc[:, j].mean()) / miStat.iloc[:, j].std()
    zcMix[zcMix < 0] = 0
    return np.sqrt(zrDyn**2 + zcMix**2)

def toZscore(x):
    return (x - x.mean()) / x.std()