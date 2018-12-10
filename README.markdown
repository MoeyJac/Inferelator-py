![Inferelator](https://slideplayer.com/slide/14033886/86/images/64/Local+regulatory+network+reconstruction%3A+the+Inferelator.jpg)

This is a python re-implementation of the algorithm described in [The Inferelator](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2006-7-5-r36), by Bonneau Labs, NYU.

It provides a method for deriving genome-wide transcriptional regulatory interactions, and predicts a large portion of regulatory networks using L2 Bayesian Regression.

## Documentation

The Inferelator should be run using [python3](https://www.python.org/downloads/) with the following structure:

`python3 inferelator.py [JOB_NAME]`

The `JOB_NAME` is the name of the configuration script that should be used, and should be located in the `jobs/` directory.

## Configuration Highlights
# NOTE: Some configuration specification are listed in the default configuration file but have not yet been implemented.
```
p['inputDir'] = 'input/dream4' - Directory in which input files will be search
p['metaDataFile'] = 'meta_data.tsv' - Meta data file to be used from the specified inpurDir
p['priorsFile'] = 'gold_standard.tsv' - Priors data file to be used from the specified inpurDir
p['goldStandardFile'] = 'gold_standard.tsv' - Gold Standard data file to be used from the specified inpurDir
p['jobSeed'] = 42 - Random Seed to be used by the application
p['saveToDir'] = None - Directory in which to save outputted files

p['verbose'] = False - Option to print computed Betas at each bootstrap
p['demo'] = False - Option to use precomputed clean data (makes beta output cleaner)
p['exportCLRMatrix'] = False - Option to write computed CLR matrices to output directory
p['exportBSDR'] = False - Option to write computed bootstrap specific design and response matricies to outpur directory
```

## Help

Any questions concerning running the code or creating the job script can be directed to joseph.macaluso@stonybrook.edu