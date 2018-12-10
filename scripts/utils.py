from imports import *

global params

def getParams():
    return params

def setParams(newParams):
	global params
	params = newParams

def loadJob(jobName):
	importlib.import_module(jobName).load()

def readInput(inputDir, expMatFile, tfNamesFile, metaDataFile, priorsFile=None, goldStandardFile=None):
	input = defaultdict(pd.DataFrame)
	input['expMat'] = pd.read_csv(os.path.join(inputDir, expMatFile), sep='\t')
	input['tfNames'] = pd.read_csv(os.path.join(inputDir, tfNamesFile), sep='\t', header=None, names = ['name'])
	input['tfWithExp'] = pd.read_csv(os.path.join(inputDir, tfNamesFile), sep='\t', header=None, names = ['name'])
	if metaDataFile is not None:
		input['metaData'] = pd.read_csv(os.path.join(inputDir, metaDataFile), sep='\t')
	if priorsFile is not None:
		input['priorsMat'] = pd.read_csv(os.path.join(inputDir, priorsFile), sep='\t')
	if goldStandardFile is not None:	
		input['gsMat'] = pd.read_csv(os.path.join(inputDir, goldStandardFile), sep='\t')
	return input

def flatten(l):
	return [y for x in l for y in x]