#!/usr/bin/env python

from ROOT import TH1D, TCanvas, gStyle
import sys

gStyle.SetCanvasColor(0)
gStyle.SetPalette(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPaintTextFormat("5.2f")


gStyle.SetLineWidth(2)
gStyle.SetTextSize(1.1)
gStyle.SetLabelSize(0.06,"xy")
gStyle.SetTitleSize(0.06,"xy")
gStyle.SetTitleOffset(1.2,"x")
gStyle.SetTitleOffset(1.0,"y")
gStyle.SetPadTopMargin(0.1)
gStyle.SetPadRightMargin(0.1)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.12)


if len(sys.argv)<2:
    print 'Usage: parseTrigReport.py <data|mc> file1 file2 file...'
    sys.exit()
fnames=sys.argv[2:]
mode=sys.argv[1]
ccc=[]
hhh=[]
for fname in fnames:
    ffn=open(fname,'r')
    filename=[a.rstrip('\n') for a in ffn.readlines()]
    ccc.append(TCanvas())
    ccc[-1].SetLogy()
    ccc[-1].SetGridy()
    ccc[-1].SetGridx()
    hhh.append(TH1D(fname,fname,10,0.5,10.5))
    if (mode=='data'):
        hhh[-1].GetXaxis().SetBinLabel(1,'Total')
        hhh[-1].GetXaxis().SetBinLabel(2,'L1DoubleMu0HQ')
    if (mode=='mc'):
        hhh[-1].GetXaxis().SetBinLabel(1,'')
        hhh[-1].GetXaxis().SetBinLabel(2,'Total')
    hhh[-1].GetXaxis().SetBinLabel(3,'L1DoubleMu0erHQ')
    hhh[-1].GetXaxis().SetBinLabel(4,'hltTauTo2MuL2PreFiltered0')
    hhh[-1].GetXaxis().SetBinLabel(5,'hltTauTo2MuL3Filtered')
    hhh[-1].GetXaxis().SetBinLabel(6,'hltDisplacedmumuFilterTauTo2Mu')
    hhh[-1].GetXaxis().SetBinLabel(7,'hltTauTo2MuTracFilter')
    hhh[-1].GetXaxis().SetBinLabel(8,'hltBoolEnd')
    hhh[-1].GetYaxis().SetName('Events')
    if (mode=='data'):
        hhh[-1].GetXaxis().SetRangeUser(0.5,7.5)
    if (mode=='mc'):
        hhh[-1].GetXaxis().SetRangeUser(1.5,7.5)
  
    for ff in filename:
        rf = open(ff,'r')
        a=rf.readlines()
        for b in a:
            if ('TrigReport' in b) \
                   and len(' '.join(b.split()).split(' '))==7 \
                   and not ('----' in b) \
                   and not ('Visited' in b):
                value=int(' '.join(b.split()).split(' ')[3])
                if ('HLTfilter' in b):
                    value2=int(' '.join(b.split()).split(' ')[1])
                    hhh[-1].SetBinContent(1,value2+hhh[-1].GetBinContent(1))
                    if (mode=='data'):
                        hhh[-1].SetBinContent(2,value+hhh[-1].GetBinContent(2))

                if 'hltL1sL1DoubleMu0HighQ' in b:
                    value2=int(' '.join(b.split()).split(' ')[1])
                    if (mode=='mc'):
                        hhh[-1].SetBinContent(2,value2+hhh[-1].GetBinContent(2))
                    hhh[-1].SetBinContent(3,value+hhh[-1].GetBinContent(3))
                if 'hltTauTo2MuL2PreFiltered0' in b:
                    hhh[-1].SetBinContent(4,value+hhh[-1].GetBinContent(4))
                if 'hltTauTo2MuL3Filtered' in b:
                    hhh[-1].SetBinContent(5,value+hhh[-1].GetBinContent(5))
                if 'hltDisplacedmumuFilterTauTo2Mu' in b:
                    hhh[-1].SetBinContent(6,value+hhh[-1].GetBinContent(6))
                if 'hltTauTo2MuTracFilter' in b:
                    hhh[-1].SetBinContent(7,value+hhh[-1].GetBinContent(7))
                if 'hltBoolEnd' in b:
                    hhh[-1].SetBinContent(8,value+hhh[-1].GetBinContent(8))

  
    hhh[-1].DrawCopy()
    ccc[-1].Update()
    ccc[-1].Print('count_'+str(fname.split('.')[0])+'.png')
    ccc.append(TCanvas())
    ccc[-1].SetLogy()
    ccc[-1].SetGridy()
    ccc[-1].SetGridx()
    if (mode=='data'):
        hhh[-1].Scale(7089*1.0/hhh[-1].GetBinContent(3))
    if (mode=='mc'):
        hhh[-1].Scale(1.0/hhh[-1].GetBinContent(2))
    hhh[-1].DrawCopy()
    ccc[-1].Update()
    ccc[-1].Print('norm_'+str(fname.split('.')[0])+'.png')

raw_input()



    
