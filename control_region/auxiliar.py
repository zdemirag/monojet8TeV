#! /usr/bin/env python
from ROOT import RooWorkspace, RooFit, RooArgSet

variables = {'Zmm':{'raw':'metRawCorZ','corrected':'metCorZ','mva':'mvametCorZ'},
             'Wmn':{'raw':'metRawCorW','corrected':'metCorW','mva':'mvametCorW'},
             'signal':{'raw':'metRaw','corrected':'met','mva':'mvamet'}}

analysis_ranges = {'inc200':[200,1000],'inc220':[220,1000],'inc250':[250,1000],'inc300':[300,1000],
                   'inc350':[350,1000],'inc400':[400,1000],'inc450':[450,1000],'inc500':[500,1000],}

def roundFloat(number,digits):
    stringedNumber = str(number)[:str(number).find('.')+1+digits]
    if number - float(stringedNumber) >= float('0.'+'0'*digits+'5'):
        stringedNumber = str(float(stringedNumber)+float('0.'+'0'*(digits-1)+'1'))
    return stringedNumber

def initWorkspace(args):
    w=RooWorkspace('normalization')
    # import the datasets
    from manageDatasets import getUnnormalizedDataSets
    datasets=getUnnormalizedDataSets(args.control_region,args.label, args.metType)
    getattr(w,'import')(datasets['data'])
    if args.control_region=='Zmm':
        datasets['others'].append(datasets['Wlv'])
        getattr(w,'import')(datasets['Zll'].Clone('mc'))
    elif args.control_region=='Wmn':
        datasets['others'].append(datasets['Zll'])
        getattr(w,'import')(datasets['Wlv'].Clone('mc'))
    else: print 'pippaccia'
    getattr(w,'import')(datasets['others'].Clone('bkgr'))
    # set the (fit) range
    variable = variables[args.control_region][args.metType]
    w.var(variable).setRange(analysis_ranges[args.binning][0],analysis_ranges[args.binning][1])
    # signal models
    w.factory("EXPR::doubleExp_data('f_data*exp(m1_data*%s)+(1-f_data)*exp(m2_data*%s)',%s,f_data[0.01,0.995],m1_data[-0.02,-0.05,0],m2_data[-0.01,-0.05,0])"%(variable,variable,variable))
    w.factory("EXPR::doubleExp_MC('f_MC*exp(m1_MC*%s)+(1-f_MC)*exp(m2_MC*%s)',%s,f_MC[0.01,0.99],m1_MC[-0.02,-0.05,0],m2_MC[-0.01,-0.05,0])"%(variable,variable,variable))
    #w.factory("EXPR::modifiedExp_data('exp(%s*tauInf_data-%s*tauSlope_data/(%s+tauOffset_data))',%s,tauInf_data[],tauSlope_data[],tauOffset_data[])"%(variable,variable,variable))
    # background model
    #w.factory("Exponential::bkgrModel(%s,mu_bkgr[-0.05,0])"%variable)
    w.factory("EXPR::bkgrModel('f_bkgr*exp(m1_bkgr*%s)+(1-f_bkgr)*exp(m2_bkgr*%s)',%s,f_bkgr[0.01,0.99],m1_bkgr[-0.02,-0.05,0],m2_bkgr[-0.01,-0.05,0])"%(variable,variable,variable))
    return w

def fitBackground(w): 
    w.pdf('bkgrModel').fitTo(w.data('bkgr'),RooFit.SumW2Error(True),RooFit.Save())
    w.factory('bkgrYields['+str(w.data('bkgr').sumEntries())+']')
    for par in ['f_bkgr','m1_bkgr','m2_bkgr']: w.var(par).setConstant()

def fitData(w):
    w.factory('dataYields['+str(w.data('data').sumEntries())+']')
    #w.factory('dataYields['+str(w.data('data').numEntries()-w.data('bkgr').sumEntries())+']')
    w.factory("SUM::dataModel(bkgrYields*bkgrModel,dataYields*doubleExp_data)")
    results=w.pdf('dataModel').fitTo(w.data('data'),RooFit.SumW2Error(True),RooFit.Save(), RooFit.Extended(True),RooFit.Minos(True))#, 
                                     #RooFit.Strategy(2), RooFit.Minimizer('Minuit2','minimize'))
    results.Print('v')
    getattr(w,'import')(results)


def fitMC(w):
    results=w.pdf('doubleExp_MC').fitTo(w.data('mc'),RooFit.SumW2Error(True),RooFit.Save())
    results.Print('v')
    getattr(w,'import')(results)

def computeRatio(w,args):
    x=w.var(variables[args.control_region][args.metType])
    norm_data = (w.data('data').sumEntries()-w.data('bkgr').sumEntries())/w.pdf('doubleExp_data').createIntegral(RooArgSet(x),RooFit.NormSet(RooArgSet(x))).getVal()
    norm_MC = w.data('mc').sumEntries()/w.pdf('doubleExp_MC').createIntegral(RooArgSet(x),RooFit.NormSet(RooArgSet(x))).getVal()
    w.factory("FormulaVar::ratio('r*doubleExp_data/doubleExp_MC', {doubleExp_data, doubleExp_MC, r["+str(norm_data/norm_MC)+"]})")

def closureTest(w):
    w.factory('GenericPdf::closure("ratio*doubleExp_MC", {ratio, doubleExp_MC})')

def processWorkspace(args):
    w=initWorkspace(args)
    fitBackground(w)
    fitData(w)
    fitMC(w)
    computeRatio(w,args)
    return w
