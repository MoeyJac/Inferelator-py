import utils

def load():
	p = {}
	p['inputDir'] = None
	p['expMatFile'] = 'expression.tsv'
	p['tfNamesFile'] = 'tf_names.tsv'
	p['metaDataFile'] = None
	p['priorsFile'] = None
	p['goldStandardFile'] = None
	#p['leaveOutFile'] = None
	#p['randomizeExpression'] = False

	p['jobSeed'] = 42
	p['saveToDir'] = None
	p['numBoots'] = 20
	p['maxPreds'] = 10
	p['miBins'] = 10
	p['cores'] = 8

	p['delTMax'] = 110
	p['delTMin'] = 0
	p['tau'] = 45

	p['percTp'] = [0]
	p['permTp'] = [1]
	p['percFp'] = [0]
	p['permFp'] = [1]
	p['prSelMode'] = 'random'

	p['evalOnSubset'] = False

	p['method'] = 'BBSR'
	p['priorWeight'] = 1

	p['useTFA'] = False
	p['priorSS'] = False

	p['outputSummary'] = False
	p['outputReport'] = False
	p['outputTFPlots'] = False

	p['enetSparseModels'] = True
	p['enetNCV'] = 10
	p['enetLambda'] = [0, 1, 100]
	p['enetVerbose'] = False
	p['enetPlotIt'] = False
	p['enetPlotFileName'] = None

	p['verbose'] = False
	p['demo'] = False
	p['exportCLRMatrix'] = False
	p['exportBSDR'] = False

	utils.setParams(p)