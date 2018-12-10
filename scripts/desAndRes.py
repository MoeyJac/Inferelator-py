from imports import *

def designAndResponse(metaData, expMat, delTMin, delTMax, tau):
	cond = metaData.condName
	prev = metaData.prevCol
	delt = metaData.delT

	metaData.loc[delt > delTMax, ['prevCol', 'delT']] = np.NaN

	steady = pd.isna(prev) & ~cond.isin(prev)
	
	desMat = expMat.loc[:, steady.values]
	resMat = expMat.loc[:, steady.values]

	
	for i in np.where(~steady)[0]:
		following = list(np.where(prev == cond[i])[0])
		followingDelt = delt.loc[following]
		off = list(np.where(followingDelt < delTMin)[0])

		cntr = 0
		for j in following:
			condName = cond[i] + '_dupl_' + str(ctr) if len(following) > 1 else cond[i]
			desMat[condName] = expMat[cond[i]]
			resMat[condName] = tau / followingDelt.values[cntr] * (expMat[cond[j]] - expMat[cond[i]])  + expMat[cond[i]]
			cntr += 1
		
		if len(following) is 0 and pd.isna(prev[i]):
			desMat[condName] = expMat[cond[i]]
			resMat[condName] = expMat[cond[i]]

	respIDX = pd.DataFrame(0, range(1,len(resMat.index)+1), range(1,len(resMat.columns)+1))
	respIDXNames = pd.DataFrame(0, range(1,len(resMat.index)+1), resMat.columns)
	for i in respIDX.columns: respIDX[i] = i
	for colName in respIDXNames.columns: respIDXNames[colName] = colName

	return {'respIDX': respIDX, 'respIDXNames': respIDXNames, 'finalDesMat': desMat, 'finalResMat': resMat}
	