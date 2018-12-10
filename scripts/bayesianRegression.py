from imports import *

def BBSR(X, Y, clrMat, nS, noPrVal, weightsMat, priorMat, verbose, demo):
    genes = Y.index
    tfs = X.index
    weightsMat = weightsMat.loc[genes, tfs]
    clrMat = clrMat.loc[genes, tfs]
    priorMat = priorMat.loc[genes, tfs]

    pp = pd.DataFrame(False, genes, tfs)
    pp[(weightsMat != noPrVal) & clrMat.notna()] = True
    pp[(priorMat != 0) & clrMat.notna()] = True

    clrMat[clrMat == 0] = np.nan
    ind = 0
    for ind in range(len(Y.index)):
        clrOrder = clrMat.iloc[ind, :].nlargest(len(clrMat.iloc[ind, :].dropna())).index
        pp.loc[genes[ind], clrOrder[0:min(len(X.index), nS, len(clrOrder))].values] = True

    betas = pd.DataFrame()
    if demo:
        pp = pd.read_csv(os.path.join('TestData', 'pp.csv'), index_col=0)
    for i in range(len(pp)):
        Xtemp = X[pp.iloc[:,i]].T
        Ytemp = Y.iloc[i, :].T
        Ytemp.columns = Y.index[i]
        if len(Xtemp.columns) > 0:
            model = BayesianRidge(compute_score=True)
            model.fit(Xtemp, Ytemp)
            b_vector = list(zip(Xtemp.columns, model.coef_))
            newBeta = pd.DataFrame({Ytemp.columns + '_Betas':model.coef_})
            betas = pd.concat([betas, newBeta], ignore_index=True, axis=1)
            if verbose:
                print('----------------------------------------------------')
                print('PP Index {0}, Expression of {1}'.format(i, Ytemp.columns))
                for b in b_vector:
                    print(b)
                print('--------------------')
        else:
            if verbose:
                print('No predictors for regression at PP index {0}, Expression of {1}'.format(i, Ytemp.columns))

    return betas