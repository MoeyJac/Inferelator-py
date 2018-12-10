import utils

def load():
	p = utils.getParams()

	p['inputDir'] = 'input/dream4'

	p['metaDataFile'] = 'meta_data.tsv'
	p['priorsFile'] = 'gold_standard.tsv'
	p['goldStandardFile'] = 'gold_standard.tsv'

	p['numBoots'] = 2
	p['cores'] = 1

	p['delTMax'] = 110
	p['delTMin'] = 0
	p['tau'] = 45

	p['percTp'] = [50]*4
	p['permTp'] = [1]*4
	p['percFp'] = [0, 100, 250, 500]
	p['permFp'] = [1, 5, 5, 5]

	p['evalOnSubset'] = False

	p['method'] = 'BBSR'
	p['priorWeight'] = 1.26

	p['saveToDir'] = 'output/dream4_BBSR_1'

	p['verbose'] = False
	p['demo'] = True
	p['exportCLRMatrix'] = True
	p['exportBSDR'] = True
    
	utils.setParams(p)
