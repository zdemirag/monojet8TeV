#! /usr/bin/env python
from ROOT import TFile
from parameters import *
if not sanityCheck(args): exit()
print args
output_file_name = '_'.join([args.sample,args.control_region if args.isClosureTest else 'signal',args.metType,args.label])+'.root' 

# deal with pdf files
if args.label.find('PDF')>-1:
    from systematics.adjustPDFDatasets import adjustPDFDatasets
    adjustPDFDatasets(args)

# (re)fit sample in the corresponding control region
from auxiliar import processWorkspace
w=processWorkspace(args)
output_file = TFile('workspaces/'+output_file_name,'recreate')
w.Write()

# reweight sample
from reweight import reweightSample
dataset = reweightSample(w,args) # need to do this in 2 steps 
output_file = TFile('data/normalized/'+output_file_name,'recreate')
#w.Write()
dataset.Write()


