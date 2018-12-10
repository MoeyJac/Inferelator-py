from imports import *

def getPriors(expMat, tfNames, priorsMat, gsMat, evalOnSubset, jobSeed, percTp, permTp, percFp, permFp, selMode):

    if priorsMat is None:
        priorsMat = pd.DataFrame(index=range(1,len(expMat.index)+1), columns=range(1,len(expMat.columns)+1), data=0)
    
    priorsPars = []
    for pos in range(len(percTp)):
        priorsPars += [[percTp[pos], i+1, percFp[pos], j+1] for i in range(permTp[pos]) for j in range(permFp[pos])]

    priors = {}
    for i in range(len(priorsPars)):
        pp = priorsPars[i]
        priorName = 'frac_tp_' + str(pp[0]) + '_perm_' + str(pp[1]) + '--frac_fp_' + str(pp[2]) + '_perm_' + str(pp[3])

        if pp[0] is 100 and pp[2] is 0:
            priors[priorName] = priorsMat
        elif pp[0] > 0 or pp[2] > 0:
            priors[priorName] = getPriorMatrix(priorsMat, pp, gsMat, evalOnSubset, jobSeed, selMode)
        else:
            priors[priorName] = pd.DataFrame(0, priorsMat.index, priorsMat.columns)
  
    return priors

def getPriorMatrix(priors, priorPars, gs, fromSubset, seed, selMode):
    percTp, permTp, percFp, permFp  = priorPars[0], priorPars[1], priorPars[2], priorPars[3]

    # NOTE: Assume fromSubset = False and selMode = 'random'
    return makePriorMat(priors, percTp, permTp + seed) + makePriorMat(priors, percFp, permFp + seed, falsePriors = True)

def makePriorMat(priors, perc, perm, falsePriors = False):
    rngState = random.getstate()

    nPriors = math.floor(priors.values.sum() * perc / 100)
    pMat = pd.DataFrame(0, priors.index, priors.columns)

    # NOTE: This part is a little messy. Want to clean it up but don't know best way
    if nPriors > 0:
        if falsePriors:
            zeroIndicies = np.where(priors == 0)
            zips = list(zip(zeroIndicies[0], zeroIndicies[1]))
            priorOrder = np.random.choice(len(zips), nPriors, replace=True)
            for i in range(nPriors):
                row = zips[priorOrder[i]][0]
                col = zips[priorOrder[i]][1]
                pMat.iloc[row, col] = priors.iloc[row, col]
        else:
            nonZeroIndicies = np.where(priors != 0)
            zips = list(zip(nonZeroIndicies[0], nonZeroIndicies[1]))
            priorOrder = np.random.choice(len(zips), len(zips), replace=False)
            for i in range(nPriors):
                row = zips[priorOrder[i]][0]
                col = zips[priorOrder[i]][1]
                pMat.iloc[row, col] = priors.iloc[row, col]

    random.setstate(rngState)

    return pMat