#! /usr/bin/env python

import sys, os, string, re
from multiprocessing import Process
from array import array
from LoadData import *
from ROOT import *
from math import *
from tdrStyle import *
from selection import build_selection

setTDRStyle()
gROOT.Macro('functions.C')

print "Starting Plotting Be Patient!"

lumi = 19.72

def get_ratio(channel, Variable,added, data, bin):
    sf = []
    #Compute all MC except the Zll or Wln
    added.Add(Variable,-1)
    #Subtract all background from data
    data.Add(added,-1)
    #Divide remaining data with Z
    data.Divide(Variable)
    for i in range(bin):
        i+=1
        sf.append(data.GetBinContent(i))
    return sf

def plot_ratio(pull,data,mc,bin,xlabel):

    Pull = data
    #Pull.Add(mc,-1)
    Pull.GetXaxis().SetTitle(xlabel)
    Pull.GetYaxis().SetTitleSize(0.04)
    Pull.GetYaxis().SetNdivisions(5)
    Pull.SetMarkerStyle(20)
    Pull.SetMarkerSize(0.8)

    if pull:
        print 'Plotting the pulls'
        for i in range(bin):
            i += 1
            if data.GetBinContent(i) != 0 :
                Pull.SetBinContent(i,Pull.GetBinContent(i)/Pull.GetBinError(i))
            else: Pull.SetBinContent(i,0)

        Pull.SetMaximum(5.0 )
        Pull.SetMinimum(-5.0)
        Pull.SetFillColor(2)
        Pull.GetYaxis().SetTitle('#sigma(Data-MC)')
        Pull.Draw("HIST")

    else:
        print 'Plotting the ratio'
        Pull.Divide(mc)
        Pull.SetMaximum(2)
        Pull.SetMinimum(0)
        Pull.GetYaxis().SetTitle('Data/Bkg.')
        Pull.SetMarkerColor(1)
        Pull.SetLineColor(1)
        Pull.Draw("e")


def plot_cms(preliminary,lumi):
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.035)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.87, 0.95, str(lumi)+" fb^{-1} (8 TeV)");

    latex3 = TLatex()
    latex3.SetNDC()
    latex3.SetTextSize(0.75*c4.GetTopMargin())
    latex3.SetTextFont(62)
    latex3.SetTextAlign(11) # align right
    latex3.DrawLatex(0.22, 0.85, "CMS");
    latex3.SetTextSize(0.5*c4.GetTopMargin())
    latex3.SetTextFont(52)
    latex3.SetTextAlign(11)
    if(preliminary):
        latex3.DrawLatex(0.20, 0.8, "Preliminary");

def update_var(ch,var):
    return {
        'signal':  var,
        'Zll'   :  var+'CorZ',
        'Wln'   :  var+'CorW',
    }[ch]

def plot_stack(channel, name,var, bin, low, high, ylabel, xlabel, setLog = False):

    if var.startswith('met'):
        var = update_var(channel,var)

    folder = 'test'
    yields = {}
    stack = THStack('a', 'a')
    added = TH1D('a', 'a',bin,low,high)
    added.Sumw2()

    Variables = {}    
    cut_standard= build_selection(channel,200)
    print "Channel is: ", channel, " variable is: ", var, " Selection is: ", cut_standard,"\n"

    reordered_physics_processes = []
    if channel == 'Zll': reordered_physics_processes = reversed(ordered_physics_processes)
    else: reordered_physics_processes = ordered_physics_processes
 
    for Type in reordered_physics_processes:
        # Create the Histograms
        histName = Type+name+channel
        Variables[Type] = TH1F(histName, histName, bin, low, high)
        Variables[Type].Sumw2()

        if Type.startswith('QCD') or Type.startswith('Zll') or \
        Type.startswith('others') or Type.startswith('Wlv') or \
        Type.startswith('Zvv'):

            Variables[Type].SetFillColor(physics_processes[Type]['color'])
            Variables[Type].SetLineColor(physics_processes[Type]['color'])
            makeTrees(Type,channel).Draw(var + " >> " + histName,"(" + cut_standard + ")* weight","goff")
            Variables[Type].Scale(float(lumi)*1000)
            stack.Add(Variables[Type],"hist")
            added.Add(Variables[Type])

        #if Type.startswith('signal'):
        #    Variables[Type].SetLineColor(1)
        #    Variables[Type].SetLineWidth(3)
        #    Variables[Type].SetLineStyle(8)
        #    Trees[Type].Draw(var + " >> " + histName,  "(" + cut_standard + " ) *"+weight   , "goff")
        #    Variables[Type].Scale(float(lumi)*1000)
                        
        if Type.startswith("data"):
            Variables[Type].SetMarkerStyle(20)
            makeTrees(Type,channel).Draw(var + " >> " + histName,  "(" + cut_standard + " ) * weight"   , "goff")
        
        yields[(Type, channel)] = Variables[Type].Integral()
        #print "Type is: ",Type, " Channel is: ", channel, " Integral is: ",Variables[Type].Integral()
        
    legend = TLegend(.60,.60,.92,.92)
    for process in  ordered_physics_processes:
        if process is not 'data':
            legend . AddEntry(Variables[process],physics_processes[process]['label'] , "f")
        else:
            legend . AddEntry(Variables[process],physics_processes[process]['label'] , "p")

    c4 = TCanvas("c4","c4", 900, 1000)
    c4.SetBottomMargin(0.3)
    c4.SetRightMargin(0.06)

    stack.SetMinimum(0.1)

    if setLog:
        c4.SetLogy()
        stack.SetMaximum( stack.GetMaximum()  +  1000*stack.GetMaximum() )
    
    stack.Draw()
    stack.GetYaxis().SetTitle(ylabel)
    stack.GetYaxis().CenterTitle()
    stack.GetXaxis().SetTitle(xlabel)
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetTitle('')

    Variables['data'].Draw("Esame")
    #Variables['signal'].Draw("same")
    
    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);

    legend.Draw("same")
    plot_cms(True,lumi)

    Pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 1.0)
    Pad.SetTopMargin(0.7)
    Pad.SetFillColor(0)
    Pad.SetGridy(1)
    Pad.SetFillStyle(0)
    Pad.Draw()
    Pad.cd(0)
    Pad.SetRightMargin(0.06)
    
    data = Variables['data'].Clone()
    plot_ratio(False,data,added,bin,xlabel)

    f1 = TF1("f1","1",-5000,5000);
    f1.SetLineColor(4);
    f1.SetLineStyle(2);
    f1.SetLineWidth(2);
    f1.Draw("same")

    c4.SaveAs(folder+'/Histo_' + name + '_'+channel+'.pdf')

    del Variables
    del var
    c4.IsA().Destructor( c4 )
    stack.IsA().Destructor( stack )




arguments = {}
#                = [var, bin, low, high, yaxis, xaxis, setLog]
arguments['met']    = ['met','met',16,200,1000,'Events/50 GeV','E_{T}^{miss} [GeV]',True]
arguments['metRaw'] = ['metRaw','metRaw',16,200,1000,'Events/50 GeV','Raw E_{T}^{miss} [GeV]',True]
arguments['genmet'] = ['genmet','genmet',16,200,1000,'Events/50 GeV','Generated E_{T}^{miss} [GeV]',True]
arguments['jetpt']  = ['jetpt','jet1.pt()',17,150,1000,'Events/50 GeV','Leading Jet P_{T} [GeV]',True]
arguments['njets']  = ['njets','njets',3,1,4,'Events','Number of Jets',True]

channel_list  = ['signal','Wln','Zll']
#channel_list  = ['Wln']
#variable_list = ['met','jetpt','njets','metRaw','genmet']
processes     = []

variable_list = ['met']

for channel in channel_list:
    for var in variable_list:
        arguments[var].insert(0,channel)
        print  arguments[var]
        process = Process(target = plot_stack, args = arguments[var])
        process.start()
        processes.append(process)
        arguments[var].remove(channel)
for process in processes: 
    process.join()
