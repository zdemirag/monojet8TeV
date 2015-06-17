#! /usr/bin/env python

import ROOT
from ROOT import RooWorkspace, RooFit, RooArgSet, RooRealVar, RooDataSet
import os.path
from ROOT import TFile
from selection import build_selection
from LoadData import *

def buildRooDataset(Type,Channel,Var):

    tree         = makeTrees(Type,Channel)
    cut_standard = build_selection(Channel,200)
    my_tree       = tree.CopyTree("1");
    #full_list = RooArgSet(Var,'selection!!!!')
    full_list = RooArgSet(Var)

    #dh = RooDataSet("dh","dh",RooArgSet(reso,gen_diphotonmass),ROOT.RooFit.Import(tree),ROOT.RooFit.Cut("gen_diphotonmass < "+masses[i+1]+" && gen_diphotonma\
#ss >"+masses[i]));

    Type_Dataset = RooDataSet("test","test",RooArgSet(Var),ROOT.RooFit.Import(*my_tree))

    #Cut(cut_standard))
    return Type_Dataset

def buildRooFunctions():

    f  = RooRealVar("f" , "f" ,  0.5 ,  0.01, 0.99 )
    m1 = RooRealVar("m1", "m1", -0.02, -0.05, 0.0  )
    m2 = RooRealVar("m2", "m2", -0.01, -0.05, 0.0  )
    doubleExp = ROOT.RooGenericPdf("doubleExp","double exponential","f*exp(m1*x)+(1-f)*exp(m2*x)",RooArgSet(x,f,m1,m2))
    return doubleExp
    

def getFit(Type,Channel,Var):
    dist = RooRealVar("dist","dist",200,1000)
    xframe = dist.frame();

    my_data = buildRooDataset(Type,Channel,Var)
    my_pdf     = buildRooFunctions()

    my_pdf.fitTo(my_dataset,Save())
    my_dataset.plotOn(xframe);
    my_pdf.plotOn(xframe);

    xframe.Draw();


getFit('Zll','Zll','met')

