#! /usr/bin/env python

from ROOT import *
from colors import *
colors = defineColors()

lumi = 1.0

######################################################

dataDir = "/data/blue/mzanetti/data/DM/032/current/FLAT/"

physics_processes = {
    'Zll': { 'label':'Z#rightarrow ll',
	     'color' : colors.keys()[0],
	     #'color':ROOT.kBlue-5,
             'ordering': 1,                  
             'files':[dataDir+'s12-zll-ptz100-v7c_0.root', 
                      dataDir+'s12-zll-ptz100-v7c_1.root',
                      dataDir+'s12-zll-ptz100-v7c_2.root',],
             },
   'Zvv': { 'label':'Z#rightarrow#nu#nu',
	    'color' : colors.keys()[4],
            #'color': ROOT.kAzure+4,
            'ordering': 4,                  
            'files': [dataDir+'s12-zjets-ptz100-v7a.root']
            },
   'Wlv': { 'label':'W#rightarrow  l#nu',
            'color' : colors.keys()[2],
	    #'color': ROOT.kYellow+2,
            'ordering': 3,                  
            'files': [dataDir+'s12-wjets-ptw100-v7c_0.root', 
                      dataDir+'s12-wjets-ptw100-v7c_1.root',
                      dataDir+'s12-wjets-ptw100-v7c_2.root',
                      dataDir+'s12-wjets-ptw100-v7c_3.root',
                      dataDir+'s12-wjets-ptw100-v7c_4.root',]
            },
   'others': { 'label':'top+EWK',
               'color' : colors.keys()[1],
	       #'color': ROOT.kGray,
               'ordering': 2,                  
               'files': [dataDir+'s12-ttj-v1-v7a.root',
                         dataDir+'s12-wtop-dr-v7a.root',
                         dataDir+'s12-wtopb-dr-v7a.root',
                         dataDir+'s12-sch-v7a.root',
                         dataDir+'s12-schb-v7a.root',
                         dataDir+'s12-tch-v7a.root',
                         dataDir+'s12-tchb-v7a.root',
                         dataDir+'s12-ww-v7a.root',
                         dataDir+'s12-wz-v7a.root',
                         dataDir+'s12-zz-v7a.root',
                         ]},
   'QCD': { 'label':'QCD',
	    'color' : colors.keys()[3],
            #'color': ROOT.kAzure+3,
            'ordering': 0,                  
            'files': [dataDir+'s12-qcdht250-500-v7a.root',
                      dataDir+'s12-qcdht500-1000-v7a.root',
                      dataDir+'s12-qcdht1000-v7a.root',
		      ]},
   'signal_higgs': { 'label':'Higgs',
		     'color' : 1,
		     'ordering': 6,                  
		     'files': [dataDir+'s12-h125inv-gf-v7a.root',
			       ]},
   'data': { 'label':'data',
             'color': 1,
             'ordering': 5,                  
             'files': [dataDir+'r12a-met-j22-v1.root',
                       dataDir+'r12b-met-j22-v1.root',
                       dataDir+'r12c-met-j22-v1.root',
                       dataDir+'r12d-met-j22-v1.root',
                       ]},
    }

tmp = {}
for p in physics_processes: 
	if physics_processes[p]['ordering']>-1: tmp[p] = physics_processes[p]['ordering']
ordered_physics_processes = []

for key, value in sorted(tmp.iteritems(), key=lambda (k,v): (v,k)):
	ordered_physics_processes.append(key)

def makeTrees(process,Channel):
	Trees={}
	if Channel == 'signal': Channel = ''
	Trees[process] = TChain("tree"+Channel)
	for sample in  physics_processes[process]['files']:
		#print "Process: ", process, " Sample: ", sample
		Trees[process].Add(sample)
	return Trees[process]

######################################################

Weights = {}
