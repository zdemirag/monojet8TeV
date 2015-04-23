#! /usr/bin/env python

import sys, os, string, re
from multiprocessing import Process
from array import array
#from LoadData import *
from ROOT import *
from math import *
from tdrStyle import *
#from selection import build_selection

setTDRStyle()
gROOT.Macro('functions.C')

chain={}

c4 = TCanvas("c4","c4", 900, 1000)

chain['Zll'] = TChain("treeZll");
chain['Zll'].Add("/data/blue/mzanetti/data/DM/032/current/FLAT/s12-zll-ptz100-v7c_0.root");
chain['Zll'].Add("/data/blue/mzanetti/data/DM/032/current/FLAT/s12-zll-ptz100-v7c_1.root");
chain['Zll'].Add("/data/blue/mzanetti/data/DM/032/current/FLAT/s12-zll-ptz100-v7c_2.root");

histo1 = TH1F('hist1', 'hist1', 100, 0, 10000)
chain['Zll'].Draw("met>>hist1")

#chain['Zll'].Draw("met>>hist1","lep1IsTightMuon&&abs(jet1.eta())<2.0&&nlep==2 && lid1+lid2==0 && abs(lid1)==13 && abs(vectorSumMass(lep1.px(),lep1.py(),lep1.pz(),lep2.px(),lep2.py(),lep2.pz())-91)<30&&nphotons==0&&ntaus==0&&(jet2.pt() <30 || deltaPhi(jet1.Phi(),jet2.Phi())<2)&&jet1CHF>0.2&&jet1NHF<0.7&&jet1NEMF<0.7&&(metFiltersWord==1023||metFiltersWord==511)&&jet1.pt()>150.&&((trigger&1)==1 || (trigger&2)==2)&&vectorSumPt(lep1.pt(),lep1.Phi(),lep2.pt(),lep2.Phi())>100&&njets<3&&deltaPhi(jet1.Phi(),metCorZPhi)>2 && metCorZ>200","goff");

print histo1.Integral()
#histo1.Draw();

#c4.SaveAs("Hist.pdf")
