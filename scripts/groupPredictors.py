from imports import *
import utils

def groupPredictors(desMat, priorMat, gsMat, bsPI, corTH=0.99, grpPre='predGroup'):
    tfs = desMat.index
    haveNa = desMat.isnull().any(axis=1)

    # NOTE: Going to ignore this for now. For most cases this check is unneccesary
    #const = [False]*len(desMat.index)
    #const.loc[(~haveNa).index, :] = desMat.loc[(~haveNa).index, :]
    #keep = ~haveNa & ~const
    #tfsKeep = tfs[keep]

    keep = ~haveNa
    tfsKeep = tfs[keep]
    
    corMat = pd.DataFrame(0, range(1, keep.values.sum() + 1), range(1, keep.values.sum() + 1))
    for i in range(len(bsPI.index)):
        bsCorMat = desMat.loc[keep, bsPI.loc[i+1, ]].T.corr()
        corMat += (bsCorMat > corTH).values
    
    cc = getAllCC(corMat)
    cc = [[[y-1 for y in x]] for x in cc]
    groups = [tfsKeep[x] for x in cc]

    groupNames = [grpPre + str(x) for x in range(1, len(groups)+1)]
    desMatGrp = pd.DataFrame(0, range(1,len(groups)+1), range(1, len(desMat.columns)+1))
    
    # NOTE: Have not tested anything where groups != []. 
    # Therefore all for loops that index over groups have not been tested, incuding in the groupPrior function
    for index, group in enumerate(groups):
        exemplar = group[np.argmax([np.std(row)/np.mean(row) for row in desMat[group]])]
        desMatGrp.loc[index+1, :] = desMat.loc[exemplar, :]

    newDesMat = desMat.loc[sorted(set(tfsKeep)-set(utils.flatten(groups))), :]
    newGsMat = desMat.loc[sorted(set(tfsKeep)-set(utils.flatten(groups))), :]
    
    newPriorMat = groupPrior(groups, priorMat, tfsKeep)
    newGsMat = groupPrior(groups, gsMat, tfsKeep)

    if sorted(desMat.index) == sorted(newDesMat.index):
        newDesMat = desMat
        newPriorMat = priorMat
        newGsMat = gsMat
    
    # NOTE: Dont have const defined for this return statement yet
    # return {'predHasNa':tfs[haveNa], 'predIsConst':tfs[const], 'predGroups':groups, 'desMat':newDesMat, 'priorMat':newPriorMat, 'gsMat':newGsMat, 'tfNames':newDesMat.index}

    return {'predHasNa':tfs[haveNa], 'predGroups':groups, 'desMat':newDesMat, 'priorMat':newPriorMat, 'gsMat':newGsMat, 'tfNames':newDesMat.index}

def groupPrior(groups, priorMat, tfsKeep):
    if priorMat is None:
        return priorMat
    priorMatGrp = pd.DataFrame(0, priorMat.index, priorMat.columns)

    for index, group in enumerate(groups):
        tempPMat = priorMat.iloc[:, group]
        tempPMatIncons = any([any(row > 0) and any(row < 0) for row in tempPMat])
        if tempPMatIncons:
            print('ERROR: Inconsistency when consolidating the prior/GS in group.predictors for group {}'.format(index+1))
        priorMatGrp.iloc[:, index+1] = np.sign([row.sum() for row in tempPMat])

    newPriorMat = priorMat.loc[:, sorted(set(tfsKeep)-set([y for x in groups for y in x]))]
    return newPriorMat

def getAllCC(adjMat):
    n = len(adjMat.index)
    inList = pd.Series(False, range(1, n+1))
    ccList = []
    for i in range(1, n + 1):
        if not inList[i]:
            cc = getCC(i, adjMat, [])
            if len(cc) > 1:
                ccList += cc
            inList[cc] = True
    return ccList

def getCC(curNode, adjMat, visited):
    visited += [curNode]
    indicies = np.where(adjMat.loc[curNode, :] > 0)[0]
    newAdjNodes = set([x+1 for x in indicies]) - set(visited)
    for aNode in newAdjNodes:
        visited += [getCC(aNode, adjMat, visited)]
    return visited