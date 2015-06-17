#! /usr/bin/env python
import os.path
from ROOT import TFile

def getUnnormalizedDataSets(phase_space_region, label='std', met_type='mva'):
    input_file_name = '/home/mzanetti/cms/ntupleAnalysis/DM/shapeAnalysis/data/'+'_'.join([phase_space_region,met_type,label])+'.root'
    print input_file_name
    if not os.path.isfile(input_file_name):
        print 'File with rooDataSets ('+input_file_name+') not found, quitting'
        return
    input_file = TFile(input_file_name)
    rooDataSets = {}
    for i in input_file.GetListOfKeys(): 
        rooDataSet = input_file.Get(i.GetName())
        if rooDataSet.ClassName()!='RooDataSet': continue
        process_name = i.GetName().replace('roo','')
        # do not deal with any signal
        if process_name=='signal': continue
        # data or MC
        if process_name=='data': rooDataSets['data'] = rooDataSet.Clone('data')
        else:
            # all MCs
            try: rooDataSets['MC'].append(rooDataSet)
            except: rooDataSets['MC'] = rooDataSet.Clone('MC')
            # V+jets
            if process_name=='Zll' or process_name=='Zvv' or process_name=='Wlv':
                rooDataSets[process_name] = rooDataSet.Clone(process_name)
            # everything else
            else: 
                try: rooDataSets['others'].append(rooDataSet)
                except: rooDataSets['others'] = rooDataSet.Clone('others')

    return rooDataSets


def getNormalizedDatasets(sample,phase_space_region,label='std', met_type='mva'):
    input_file_name = '/home/mzanetti/cms/ntupleAnalysis/DM/shapeAnalysis/data/normalized/'+'_'.join([sample,phase_space_region,met_type,label])+'.root'
    input_file = TFile(input_file_name)
    if not os.path.isfile(input_file_name):
        print 'File with rooDataSet ('+input_file_name+') not found, quitting'
        return
    for i in input_file.GetListOfKeys(): 
        rooDataSet = input_file.Get(i.GetName())
        if rooDataSet.ClassName()!='RooDataSet': continue
        return rooDataSet
