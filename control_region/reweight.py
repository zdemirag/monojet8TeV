#! /usr/bin/env python
import os.path, pickle, math
from ROOT import RooArgSet, RooRealVar

'''
Reweight a given process (args.sample) in a given phase space region
by means of a reweighting function computed by comparing data and MC 
in the corresponding control region.
Notes:
- the phase space region where the normalization is applied is chosen by 
the args.isClosureTest switch
- the variable of the dataset (weighted and unweighted) is taken automatically 
from the dataset
- the name of the weighting function's variable is deduced from the 
control_region (args.control_region)
'''

def reweightSample(w, args):
    from auxiliar import variables
    from manageDatasets import getUnnormalizedDataSets
    unweighted_sample=getUnnormalizedDataSets(args.control_region if args.isClosureTest else 'signal',args.label, args.metType)[args.sample]
    weighted_sample = unweighted_sample.emptyClone('normalized'+args.sample)
    weight = RooRealVar('weight','',1)
    for i in range(0,unweighted_sample.numEntries()):
        # get the argset (needed for addFast)
        argSet = unweighted_sample.get(i)
        # Need to compute f(x); x is the variable whose spectrum I want to reweight
        # f(x) in the workspace is defined for the x of that given control region (i.e. either mvametCorZ or mvametCorW)
        # the actual value of x is however either mvamet (reweighing in the signal region) or closureTest
        w.var(variables[args.control_region][args.metType]).setVal(argSet.getRealValue(variables[args.control_region if args.isClosureTest else 'signal'][args.metType]))
        weight.setVal(unweighted_sample.weight()*w.function('ratio').getVal()) 
        weighted_sample.addFast(argSet, weight.getVal())
    return weighted_sample


