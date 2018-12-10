import sys
sys.path.append('scripts/')
sys.path.append('jobs/')

from imports import *
import utils
from desAndRes import designAndResponse
from priors import getPriors
from groupPredictors import groupPredictors
from miAndClr import mi, mixedCLR
from bayesianRegression import BBSR

utils.loadJob('default')
utils.loadJob(sys.argv[1])
pars = utils.getParams()
random.seed(pars['jobSeed'])

# Read in data
data = utils.readInput(
    pars['inputDir'], pars['expMatFile'], 
    pars['tfNamesFile'], pars['metaDataFile'], 
    pars['priorsFile'], pars['goldStandardFile'])

# Generate design and response matricies
desResp = designAndResponse(
    data['metaData'], data['expMat'], 
    pars['delTMin'], pars['delTMax'], pars['tau'])

# Generate priors
priors = getPriors(
    data['expMat'], data['tfNames'], 
    data['priorsMat'], data['gsMat'], 
    pars['evalOnSubset'], pars['jobSeed'], 
    pars['percTp'], pars['permTp'], 
    pars['percFp'], pars['permFp'], pars['prSelMode']) 

# Generate bootstrap permutations
numBoots, respIDX, respIDXNames = pars['numBoots'], desResp['respIDX'], desResp['respIDXNames']
bsPI = pd.DataFrame(0, range(1, numBoots+1), respIDX.columns)

# NOTE: Currently does not work using 1 bootstrap. Please use 2 or more
if numBoots is 1:
    bsPI.loc[1, :] + respIDXNames.loc[1, :]
else:
    for bootstrap in range(1, numBoots+1):
        # NOTE: This was modified to use the list of respIDXNames instead of respIDX. 
        bsPI.loc[bootstrap, :] = list(np.random.choice(respIDXNames.columns, len(respIDXNames.columns), replace=True))

if not os.path.exists(pars['saveToDir']):
            os.makedirs(pars['saveToDir'])

### Main Loop ###
for priorName in priors.keys():
    print('Method: {}\nWeight: {}\nPriors: {}\n'.format(pars['method'], pars['priorWeight'], priorName))

    prior = priors[priorName]

    # NOTE: Leaving out transcription factor activities for time being

    desMat = desResp['finalDesMat']
    gpOut = groupPredictors(desMat, prior, data['gsMat'], bsPI)

    bootstrapBetas = []
    ### Bootstrap Loop ###
    for bootstrap in range(1, numBoots+1):
        print('Bootstrap {} of {}'.format(bootstrap, numBoots))

        noPrWeight = 1
        if (prior != 0).values.sum() > 0:
            if pars['method'] is 'BBSR':
                noPrWeight = pars['priorWeight']**-1

        weightsMat = gpOut['priorMat']*0 + noPrWeight
        weightsMat[gpOut['priorMat'] != 0] = pars['priorWeight']

        X = gpOut['desMat'].loc[:, bsPI.loc[bootstrap, :]]
        Y = desResp['finalResMat'].loc[:, bsPI.loc[bootstrap, :]]

        if pars['exportBSDR']:
            X.to_csv(os.path.join(pars['saveToDir'], priorName + '_bootstrap_' + str(bootstrap) + '_BSDR_X' + '.csv'))
            Y.to_csv(os.path.join(pars['saveToDir'], priorName + '_bootstrap_' + str(bootstrap) + '_BSDR_Y' + '.csv'))

        if len(X.index) > 6000:
            X = X.loc[gpOut['tfNames'], :]

        print('Calculating MI')
        Ms = mi(Y.T, X.T, pars['miBins'])
        Ms.values[[np.arange(len(Ms.columns))]*2] = 0
        print('Calculating Background MI')
        Ms_bg = mi(X.T, Y.T, pars['miBins'])
        Ms_bg.values[[np.arange(len(Ms_bg.columns))]*2] = 0

        print('Calculating CLR Matrix')
        clrMat = mixedCLR(Ms_bg, Ms)
        clrMat.index = Y.index
        clrMat.columns = X.index
        clrMat = clrMat.loc[:, gpOut['tfNames']]

        if pars['exportCLRMatrix']:
            clrMat.to_csv(os.path.join(pars['saveToDir'], priorName + '_bootstrap_' + str(bootstrap) + '_CLR_Matrix' '.csv'))

        # Get the spares ODE models
        X = X.loc[gpOut['tfNames'], :]
        print('Calculating sparse ODE models')

        # NOTE: Only implementing BBSR model
        xSmall = BBSR(X, Y, clrMat, pars['maxPreds'], noPrWeight, weightsMat, gpOut['priorMat'], pars['verbose'], pars['demo'])
        bootstrapBetas.append(xSmall)
        print('')

        xSmall.to_csv(os.path.join(pars['saveToDir'], priorName + '_bootstrap_' + str(bootstrap) + '_betas' + '.csv'))
