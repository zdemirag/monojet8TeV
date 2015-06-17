def build_selection(selection,bin0):

    selections = ['signal','Zll','Wln']

    snippets = {
        #** monojet
        'met filter':['(metFiltersWord==1023||metFiltersWord==511)',selections],
        'jet cleaning':['jet1CHF>0.2&&jet1NHF<0.7&&jet1NEMF<0.7',selections],
        'trigger':['((trigger&1)==1 || (trigger&2)==2)',selections],
        'lepton veto':['nlep==0',['signal']],
        'extra stuff veto':['nphotons==0&&ntaus==0',selections], 
        'jet multiplicity':['njets<3',selections],
        'leading jet pT':['jet1.pt()>150.',selections],
        'leading jet eta':['abs(jet1.eta())<2.0',selections],
        'trailing jet':['(jet2.pt() <30 || deltaPhi(jet1.Phi(),jet2.Phi())<2)',selections],

        #** Control Regions
        'leading muon ID': ['lep1IsTightMuon',['Wln','Zll']],
        'leading muon Iso': ['lep1IsIsolated',['Wln']],
        'Zmm':['nlep==2 && lid1+lid2==0 && abs(lid1)==13 && abs(vectorSumMass(lep1.px(),lep1.py(),lep1.pz(),lep2.px(),lep2.py(),lep2.pz())-91)<30',['Zll']],
        'dilepPt':['vectorSumPt(lep1.pt(),lep1.Phi(),lep2.pt(),lep2.Phi())>100',['Zll']],
        'Wln':['nlep==1 && abs(lid1)==13 && lep1.pt()>15 && abs(transverseMass(lep1.pt(),lep1.phi(),met,metPhi)-75)<25',['Wln']],
        }

    selectionString = ''
    for cut in snippets:
        if selection in snippets[cut][1]: 
            selectionString += snippets[cut][0]+'&&'

    met  = 'met'
    metZ = 'metCorZ'
    metW = 'metCorW'

    analysis_bin = {}
    analysis_bin[0] = bin0

    if selection.find('Zll')>-1: selectionString+='deltaPhi(jet1.Phi(),'+metZ+'Phi)>2 && '+metZ+'>'+str(analysis_bin[0])
    elif selection.find('Wln')>-1: selectionString+='deltaPhi(jet1.Phi(),'+metW+'Phi)>2 && '+metW+'>'+str(analysis_bin[0])
    else: selectionString+='deltaPhi(jet1.Phi(),'+met+'Phi)>2 && '+met+'>'+str(analysis_bin[0])

    return selectionString

