from ROOT import TH1D, TCanvas
import sys
fnames=sys.argv[1:]
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
    hhh[-1].GetXaxis().SetBinLabel(1,'Total')
    hhh[-1].GetXaxis().SetBinLabel(2,'L1DoubleMu0HQ')
    hhh[-1].GetXaxis().SetBinLabel(3,'L1DoubleMu0erHQ')
    hhh[-1].GetXaxis().SetBinLabel(4,'hltTauTo2MuL2PreFiltered0')
    hhh[-1].GetXaxis().SetBinLabel(5,'hltTauTo2MuL3Filtered')
    hhh[-1].GetXaxis().SetBinLabel(6,'hltDisplacedmumuFilterTauTo2Mu')
    hhh[-1].GetXaxis().SetBinLabel(7,'hltTauTo2MuTracFilter')
    hhh[-1].GetXaxis().SetBinLabel(8,'hltBoolEnd')
    hhh[-1].GetYaxis().SetName('Events')
    hhh[-1].GetXaxis().SetRangeUser(0.5,7.5)
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
                    hhh[-1].SetBinContent(2,value+hhh[-1].GetBinContent(2))
                if 'hltL1sL1DoubleMu0HighQ' in b:
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
    hhh[-1].Scale(1.0/hhh[-1].GetBinContent(3))
    hhh[-1].DrawCopy()
    ccc[-1].Update()
    ccc[-1].Print('norm_'+str(fname.split('.')[0])+'.png')

raw_input()



    
