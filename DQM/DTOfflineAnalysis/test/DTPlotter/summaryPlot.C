#include <TH1F.h>

class SummaryPlot {
  
 public:
  SummaryPlot(TString name){
    hsumm = new TH1F(name,name, 250, 0,250);

    hsumm->SetMarkerColor(6);
    hsumm->SetMarkerStyle(23);  
    
    TAxis* xaxis = hsumm->GetXaxis();
    xaxis->SetBinLabel(bin(-2,1,6),"W-2 MB1");
    xaxis->SetBinLabel(bin(-1,1,6),"W-1");
    xaxis->SetBinLabel(bin(0,1,6),"W0");
    xaxis->SetBinLabel(bin(1,1,6),"W1");
    xaxis->SetBinLabel(bin(2,1,6),"W2");   
    xaxis->SetBinLabel(bin(-2,2,6),"W-2 MB2");
    xaxis->SetBinLabel(bin(-1,2,6),"W-1");
    xaxis->SetBinLabel(bin(0,2,6),"W0");
    xaxis->SetBinLabel(bin(1,2,6),"W1");
    xaxis->SetBinLabel(bin(2,2,6),"W2");
    xaxis->SetBinLabel(bin(-2,3,6),"W-2 MB3");
    xaxis->SetBinLabel(bin(-1,3,6),"W-1");
    xaxis->SetBinLabel(bin(0,3,6),"W0");
    xaxis->SetBinLabel(bin(1,3,6),"W1");
    xaxis->SetBinLabel(bin(2,3,6),"W2"); 
    xaxis->SetBinLabel(bin(-2,4,7),"W-2 MB4");
    xaxis->SetBinLabel(bin(-1,4,7),"W-1");
    xaxis->SetBinLabel(bin(0,4,7),"W0");
    xaxis->SetBinLabel(bin(1,4,7),"W1");
    xaxis->SetBinLabel(bin(2,4,7),"W2");

    xaxis->SetTicks("0");
  }
  
  void Fill(int wheel, int station, int sector, float value) {
    hsumm->SetBinContent(bin(wheel,station,sector), value);
  }


  


  int bin(int wheel, int station, int sector) {
    if (sector==0) sector=6;
    int nSectors = 12;
    if (station == 4) nSectors = 14;
    return(station - 1)*60 + (wheel + 2)*nSectors + sector;

  }

  TH1F* hsumm;

};
