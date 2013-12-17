/*
 *  See header file for a description of this class.
 *
 *  $Date: 2013/11/13 11:18:41 $
 *  $Revision: 1.19 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TTreeReader.h"

#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "DTSegmentObject.h"
#include "DTHitObject.h"
#include "DTMuObject.h"
#include "Histograms.h"
#include "Utils.h"
#include "TMath.h"
#include "DTCalibrationMap.h"

#include <iostream>
#include <sstream>
#include <vector>
#include <cmath>

using namespace std;

bool patchVd = true; // Apply corrections to the measured vd

TH1S* hRun=new TH1S("hRun","hRun", 1000, 130000, 150000);

// ---> Muon quality distributions

TH1F* hMuonQualityChi2Sta=new TH1F("hMuonQualityChi2Sta","hChi2Sta", 100, 0, 10);
TH1F* hMuonQualityNHitsGlb=new TH1F("hMuonQualityNHitsGlb","hHitsGlb", 60, 0, 60);
TH1F* hMuonQualityNVHitsGlb=new TH1F("hMuonQualityNVHitsGlb","hVHitsGlb", 60, 0, 60);
TH1F* hMuonQualityChi2Glb=new TH1F("hMuonQualityChi2Glb","hChi2Glb", 100, 0, 10);
TH1F* hMuonQualityNHitsSta=new TH1F("hMuonQualityNHitsSta","hHitsSta", 60, 0, 60);
TH1F* hMuonQualityNVHitsSta=new TH1F("hMuonQualityNVHitsSta","hVHitsSta", 60, 0, 60);
// <---

// ---> Study of theta eff.
TH2F* hThetaEffNum1;
TH2F* hThetaEffDen;
TH2F* hThetaEffNum2;
TH2F* hThetaEffNum3;
TH2F* hThetaEffNum4;
TH1F* hNAvThetaHits;

TH1F* hThetaHitsPosition1= new TH1F ("hThetaHitsPosition1", "0 Theta Hits", 10,0,10) ;
TH1F* hThetaHitsPosition2=new TH1F ("hThetaHitsPosition2", "# Theta Hits >=3, outside window ", 10,0,10);
TH1F* hThetaHitsPosition3=new TH1F ("hThetaHitsPosition3", "# Theta Hits>=3, in window", 10,0,10);
TH1F* hThetaHitsPosition4=new TH1F ("hThetaHitsPosition4", "# Theta Hits >=4, outside window ", 10,0,10) ;
TH1F* hThetaHitsPosition5=new TH1F ("hThetaHitsPosition5", "# Theta Hits >= 4, in window", 10,0,10) ;
TH1F* hDistAv=new TH1F ("hDistAv","Distance in wire",10,0,10);
TH1F* hDistHits=new TH1F ("hDistHits","Distance in wire",10,0,10);

TH1F* hDistHits2L=new TH1F ("hDistHits2L","Distance in wire",10,0,10);

bool insideThetaWindow(float theta, int wheel, int station);
// <---


vector<DTDetId> badSLs;

bool skipBadSL(const DTDetId& id) {

  if (badSLs.size()==0) {
    badSLs.push_back(DTDetId(-2, 2, 3, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 4, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 5, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 6, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 9, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 11, 2, 0, 0));
    badSLs.push_back(DTDetId(-2, 2, 12, 2, 0, 0));

    badSLs.push_back(DTDetId(-1, 2, 1, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 3, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 4, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 7, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 8, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 9, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 11, 2, 0, 0));
    badSLs.push_back(DTDetId(-1, 2, 12, 2, 0, 0));

    badSLs.push_back(DTDetId(0, 2, 5, 2, 0, 0));
    badSLs.push_back(DTDetId(0, 2, 6, 2, 0, 0));
    badSLs.push_back(DTDetId(0, 2, 7, 2, 0, 0));
    badSLs.push_back(DTDetId(0, 2, 8, 2, 0, 0));
    badSLs.push_back(DTDetId(0, 2, 9, 2, 0, 0));
    badSLs.push_back(DTDetId(0, 2, 12, 2, 0, 0));

    badSLs.push_back(DTDetId(1, 2, 1, 2, 0, 0));
    badSLs.push_back(DTDetId(1, 2, 4, 2, 0, 0));

    badSLs.push_back(DTDetId(2, 2, 11, 2, 0, 0));
    badSLs.push_back(DTDetId(2, 2, 7, 2, 0, 0));
  }

  //  cout << badSLs.size() << " " << id <<endl;

  for (vector<DTDetId>::const_iterator i=badSLs.begin();
       i!=badSLs.end(); ++i) {
    if (id==(*i)) return true;
  }
  return false;
}





TTreeReader::TTreeReader(const TString& fileName, const TString& outputFile) : 
  doStep1(false),
  detail(999),
  theOutFile(outputFile),
  theGranularity(-1),
  nevents(0),
  filterEvents(0),
  selectLR(0),
  filterSL(false),
  ptmin(0.),
  runmin(-1),
  runmax(-1),
  debug(0),
  readCalibTable(false),
  calibMap(0) {
  // open the file containing the tree
  TFile *file = new TFile(fileName.Data());
  if(file == 0) {
    cerr << "[TTreeReader]***Error: File: " << fileName << " does not exist!" << endl;
    return;
  }

  // Retrieve the TNtuple
  tree = (TTree *) file->Get("DTSegmentTree");

  
  cout << "Read File: " << fileName << endl;
  cout << "Opening tree: " << tree->GetName() << " with "
       << tree->GetEntries() << " entries" << endl;


  segments = new TClonesArray("DTSegmentObject");
  muons  = new TClonesArray("DTMuObject");

  setBranchAddresses();
  setGranularity("SL");
  
}


TTreeReader::TTreeReader(TTree* aTree, const TString& outputFile) :
  doStep1(false),
  detail(999),
  theOutFile(outputFile),
  tree(aTree),   
  theGranularity(-1),
  nevents(0),
  filterEvents(0),
  selectLR(0),
  filterSL(false),
  ptmin(0.),
  runmin(-1),
  runmax(-1),
  debug(0),
  readCalibTable(false),
  calibMap(0) {

   cout << "Opening tree: " << tree->GetName() << " ... ";
   cout << tree->GetEntries() << " entries" << endl;

  segments = new TClonesArray("DTSegmentObject");
  muons  = new TClonesArray("DTMuObject");

  setBranchAddresses();
  setGranularity("SL");
}



TTreeReader::~TTreeReader(){}



void TTreeReader::setBranchAddresses() {
  // set the addresses of the tree variables
  tree->SetBranchAddress("segments",&segments);
  tree->SetBranchAddress("muonCands",&muons);
  tree->SetBranchAddress("Run",&run);

}

void TTreeReader::begin() {
  cout << "Begin" << endl;


  hThetaEffNum1 =new TH2F ("hThetaEffNum1","hThetaEffNum1",12 ,0.5,12.5,15,0.5,15.5);
  hThetaEffDen = new TH2F("hThetaEffDen","hThetaEffDen",12,0.5,12.5,15,0.5,15.5);

  hThetaEffNum2 =new TH2F ("hThetaEffNum2","hThetaEffNum2",12 ,0.5,12.5,15,0.5,15.5);
  

  hThetaEffNum3 =new TH2F ("hThetaEffNum3","hThetaEffNum3",12 ,0.5,12.5,15,0.5,15.5);
  

  hThetaEffNum4 =new TH2F ("hThetaEffNum4","hThetaEffNum4",12 ,0.5,12.5,15,0.5,15.5);
  hNAvThetaHits=new TH1F("hNAvThetaHits"  ,"hTheta available Hits if non efficient with 3 or 4 Theta Hits",20,0,20. );

  // build the histos with the desired granularity
  for(int wheel = -2; wheel != 3; ++wheel) {   // loop over wheels
    for(int station = 1; station != 5; ++station) { // loop over stations

      for(int sector = 1; sector != 15; ++sector) { // loop over sectors
	if(station != 4 && (sector == 13 || sector == 14)) continue;

	// book the segment histos
	DTDetId chId = buildDetid(wheel, station, sector, 0, 0, 0);

// 	// One set for all segments with no cuts
// 	if(histosSeg["All"].find(chId) == histosSeg["All"].end()) {
// 	  histosSeg["All"][chId] = new HSegment(Utils::getHistoNameFromDetIdAndSet(chId, "All"), 1);
// 	}
	
	// One set of histograms for each specified set of cuts
	for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
	    set != cutSets.end();
	    ++set) {
	  TString setName = (*set).first;
	  if(histosSeg[setName].find(chId) == histosSeg[setName].end()) {
	    histosSeg[setName][chId] = new HSegment(Utils::getHistoNameFromDetIdAndSet(chId, setName), detail);
	  }
	}

	for(int sl = 1; sl != 4; ++sl) { // loop over SLs
	  if(station == 4 && sl == 2) continue;
	  for(int layer = 1; layer != 5; ++layer) {
	    DTDetId detId = buildDetid(wheel, station, sector, sl, layer, 0);
// 	    TString name = Utils::getHistoNameFromDetId(detId);
		
	    // loop over set of cuts
	    for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
		set != cutSets.end();
		++set) {
	      TString setName = (*set).first;
	      if(histosRes[setName].find(detId) == histosRes[setName].end()) {
		cout << "book histo for: " << Utils::getHistoNameFromDetIdAndSet(detId, setName) << endl;
		histosRes[setName][detId] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId, setName), detail);
		if(doStep1)
		  histosResS1[setName][detId] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId, setName) + "_S1", detail);
	      } 
	    }

	  }
	}
      }
    }
  }
}

void TTreeReader::processEvent(int entry) {


  hRun->Fill(run);

  //---> Muon quality plots
  
  for(int iMu=0; iMu < muons->GetEntriesFast(); iMu++) { // loop over events
    DTMuObject *oneMu = (DTMuObject *) muons->At(iMu);	
    
    // Barrel EWK muons (no isolation & dxy cut)
    if (fabs(oneMu->eta)<1.2 && 
	oneMu->type==1 && 
	TMath::Abs(oneMu->qpt)>=20 
	//	&& oneMu->normChi2glb < 10. //&& 
	//	oneMu->nGlbDTValidHits>0 &&
	//	oneMu->nPixHits>0
	) {
      hMuonQualityChi2Sta->Fill(oneMu->normChi2sta);
      hMuonQualityChi2Glb->Fill(oneMu->normChi2glb);
      hMuonQualityNHitsGlb->Fill(oneMu->nGlbDTHits);
      hMuonQualityNHitsSta->Fill(oneMu->nStaDTHits);
      hMuonQualityNVHitsGlb->Fill(oneMu->nGlbDTValidHits);
      hMuonQualityNVHitsSta->Fill(oneMu->nStaDTValidHits);

    }
  }

  //<----

  for(int iSegm=0; iSegm < segments->GetEntriesFast(); iSegm++) { // loop over segments 

    DTSegmentObject *oneSeg = (DTSegmentObject *) segments->At(iSegm);

    // <---- Theta efficiency plots
    if (false) {
      int thetaCase =0;
      if (oneSeg->station!=4 && 
	  oneSeg->nHitsPhi>=8 && 
	  oneSeg->phi>-25*TMath::DegToRad() && oneSeg->phi< 25*TMath::DegToRad()) {
	
	hThetaEffDen->Fill(oneSeg->sector,(5*oneSeg->station -2)+ oneSeg->wheel );
	if(oneSeg->nHitsTheta ==0)
	  {
	    thetaCase=1;
	  }      
    
	if (oneSeg->nHitsTheta >=3){
	  if( insideThetaWindow(oneSeg->theta,oneSeg->wheel,oneSeg->station)) {
	    hThetaEffNum2 -> Fill( oneSeg->sector,(5*oneSeg->station -2)+ oneSeg->wheel  );
	    thetaCase = 3 ;
	  }
	  else {
	    hThetaEffNum1 -> Fill( oneSeg->sector,(5*oneSeg->station -2)+ oneSeg->wheel  );
	    thetaCase = 2;
	  }
	}

	if (oneSeg->nHitsTheta >=4){
	  if ( insideThetaWindow(oneSeg->theta,oneSeg->wheel,oneSeg->station)){
	    hThetaEffNum4 -> Fill( oneSeg->sector,(5*oneSeg->station -2)+ oneSeg->wheel  );
	    thetaCase = 5;
	  } 
	  else {
	    hThetaEffNum3->Fill( oneSeg->sector,(5*oneSeg->station -2)+ oneSeg->wheel  );
	    thetaCase = 4;
	  }
	}
      
	int nAvTheta = 0;
	for(int iHit = 0; iHit != oneSeg->nAvailableHits; ++iHit) { // loop over the available hits 
	  DTHitObject * hitObj = (DTHitObject *) oneSeg->availableHits->At(iHit);

	  for (int jHit=iHit + 1; jHit != oneSeg->nAvailableHits;++jHit){//second loop over available hits
	    DTHitObject * hitObj1 = (DTHitObject *) oneSeg->availableHits->At(jHit);
	    // DTDetId detId1(oneSeg->wheel, oneSeg->station, oneSeg->sector,
	    //	 hitObj1->sl, hitObj1->layer, hitObj1->wire);
	
	    if ( (hitObj->sl-hitObj1->sl)==0 && fabs(hitObj->layer - hitObj1->layer) ==1    ){
	  
	      int distAv;
	      distAv =  fabs(hitObj->wire - hitObj1->wire);
	      hDistAv->Fill(distAv);
	    }
	  }
	  if (hitObj->sl==2) {
	    nAvTheta++;
	  } 
	} //end loop on available Theta-hits 

	for (int iHit = 0; iHit != oneSeg->nHits; ++iHit  ){//loop over hits
	
	  DTHitObject * hitObj3 = (DTHitObject *) oneSeg->hits->At(iHit);
	  for (int jHit = iHit + 1; jHit != oneSeg->nHits; ++jHit){ //second loop over hits
	    DTHitObject * hitObj4 = (DTHitObject *) oneSeg->hits->At(jHit);
		
	    if ( (hitObj3->sl-hitObj4->sl)==0 && fabs(hitObj3->layer - hitObj4->layer) ==1    ){
	  
	      int distHits ;
	      distHits=  fabs(hitObj3->wire - hitObj4->wire);
	      hDistHits->Fill(distHits);
	    }
	    if ( (hitObj3->sl-hitObj4->sl)==0 && fabs(hitObj3->layer - hitObj4->layer) ==2   ){
	  
	      int distHits ;
	      distHits=  fabs(hitObj3->wire - hitObj4->wire);
	      hDistHits2L->Fill(distHits);
	    }
	  }


	  hNAvThetaHits->Fill(nAvTheta);
	  if(thetaCase==1){hThetaHitsPosition1->Fill(nAvTheta);}
	  else if(thetaCase==2){hThetaHitsPosition2->Fill(nAvTheta);}
	  else if(thetaCase==3){hThetaHitsPosition3->Fill(nAvTheta);}
	  else if(thetaCase==4){hThetaHitsPosition4->Fill(nAvTheta);}
	  else if(thetaCase==5 ){hThetaHitsPosition5->Fill(nAvTheta);}
	}
      }
    } //< --- end of theta eff plots
    

    //-------------------- Segment plots 
    float dvdrift = -(oneSeg->dVDriftPhi); // change sign so that this is (Vcorr-Vold)/Vold
    float vdrift = oneSeg->vDriftCorrPhi;

    DTDetId segmDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector, 0, 0, 0);
    // Obsolete, oneSeg->vDriftCorrPhi is now already the corrected vdrift!
//     if(readCalibTable) {
//       DTDetId sl1Id = segmDetid;
//       sl1Id.sl = 1;
//       DTDetId sl3Id = segmDetid;
//       sl3Id.sl = 3;
//       // FIXME: assume that SL1 and 3 have the same  vdrift
//       if (vdrift != 0.) 
// 	vdrift = calibMap->meanVDrift(sl1Id)*(1. - oneSeg->vDriftCorrPhi);
//       if(debug > 5)
// 	cout << segmDetid << " vdrift: " << calibMap->meanVDrift(sl1Id) << endl;
//     }

    DTDetId chId = buildDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector, 0, 0, 0);
    // Plots for selected segments: loop over set of cuts
    bool passHqPhiV = false;
    vector<TString> passedCuts;
    for(map<TString, DTCut>::const_iterator set = cutSets.begin();   
	set != cutSets.end();
	++set) {
      if((*set).second.selectSegm(oneSeg)) {
	passedCuts.push_back((*set).first);
	// fill the segment related histos

	histosSeg[(*set).first][chId]->Fill(oneSeg->nHits,
					    oneSeg->nHitsPhi,
					    oneSeg->nHitsTheta,
					    oneSeg->proj,
					    oneSeg->phi,
					    oneSeg->theta,
					    -1,
					    oneSeg->chi2,
					    oneSeg->t0SegPhi,
					    oneSeg->t0SegTheta,
					    vdrift,
					    dvdrift,
					    oneSeg->Xsl,
					    oneSeg->Ysl);
	if((*set).first == "hqPhiV") passHqPhiV = true;
      }
    }
    if(passedCuts.size() == 0) continue;

//     passHqPhiV = true;
    if(passHqPhiV && debug > 5) {
      cout << "--- New Segment: " << endl;
      cout << chId << endl;
      cout << " pos: X: " << oneSeg->Xsl << " Y: " << oneSeg->Ysl << " Z: " << oneSeg->Zsl << endl;
      cout << " theta: " << oneSeg->theta << " phi: " << oneSeg->phi << endl;
      for(int i = 0; i != 3; ++i) {
	cout << " ttrig SL" << i+1 << ": "
	     << oneSeg->tTrigMean[i] + oneSeg->tTrigKfact[i] * oneSeg->tTrigSigma[i] << endl;
      }
    }



    //-------------------- Hit plots
     
    for(int iHit = 0; iHit != oneSeg->nHits; ++iHit) { // loop over the hits belonging to the segment
      DTHitObject * hitObj = (DTHitObject *) oneSeg->hits->At(iHit);
      DTDetId detId(oneSeg->wheel, oneSeg->station, oneSeg->sector,
		    hitObj->sl, hitObj->layer, hitObj->wire);

      if (filterSL && skipBadSL(detId)) {
	continue;
      }



      if(passHqPhiV && debug > 5) {
	cout << "  - Hit on wire: " << detId << endl;
	cout << "       pos X: " << hitObj->X << " Y: " << hitObj->Y << " Z: " << hitObj->Z << endl;
	cout << "       res dist: " << hitObj->resDist << endl;
	cout << "       digi time: " << hitObj->digiTime << endl;
      }
      int segSl = hitObj->sl;
      if((theGranularity == 3 || theGranularity == 4 || theGranularity==13) &&   hitObj->sl == 3) segSl = 1; // "byView"
      DTDetId detIdForPlot = buildDetid(oneSeg->wheel, oneSeg->station, oneSeg->sector,
					segSl, hitObj->layer, hitObj->wire);

      

      vector<TString>::const_iterator cut =  passedCuts.begin();      

      bool isLeft =  (hitObj->resDist*hitObj->resPos < 0);

      if (selectLR==1 && isLeft) continue;
      if (selectLR==-1 && !isLeft) continue;

      while(cut != passedCuts.end()) {

	if (cutSets[*cut].selectHit(hitObj)) {
	    histosRes[*cut][detIdForPlot]->Fill(hitObj->resDist, 
						hitObj->distFromWire, 
						hitObj->resPos,
						hitObj->X,
						hitObj->Y, 
						hitObj->angle, 
						hitObj->sigmaPos,
						oneSeg->theta,
						hitObj->wire);
	    if(doStep1)
	      histosResS1[*cut][detIdForPlot]->Fill(hitObj->resDistS1, 
						    hitObj->distFromWire, 
						    hitObj->resPos,
						    hitObj->X,
						    hitObj->Y, 
						    hitObj->angle, 
						    hitObj->sigmaPos,
						    oneSeg->theta,
						    hitObj->wire);

	    }
	++cut;
      }
    }
  }  
}



void TTreeReader::end() {
  cout << "End, # processed events: " << nevents << endl;

  // Create the root file
  TFile *theFile = new TFile(theOutFile.Data(), "RECREATE");
  theFile->cd();

  // Write the histos
  for(map<TString, DTCut>::const_iterator cut = cutSets.begin();
      cut != cutSets.end(); ++cut) {
    map<DTDetId, HRes1DHits *> theHistosRes = histosRes[(*cut).first];
    for(map<DTDetId, HRes1DHits *>::const_iterator hist =  theHistosRes.begin();
	hist != theHistosRes.end(); ++hist) {
      (*hist).second->Write();
    }
    map<DTDetId, HRes1DHits *> theHistosResS1 = histosResS1[(*cut).first];
    for(map<DTDetId, HRes1DHits *>::const_iterator hist =  theHistosResS1.begin();
	hist != theHistosResS1.end(); ++hist) {
      (*hist).second->Write();
    }

    map<DTDetId, HSegment *> theHistosSeg = histosSeg[(*cut).first];
    for(map<DTDetId, HSegment *>::const_iterator hist =  theHistosSeg.begin();
	hist != theHistosSeg.end(); ++hist) {
      (*hist).second->Write();
    }
  }

  hRun->Write();

  hMuonQualityChi2Sta ->Write();
  hMuonQualityChi2Glb ->Write();
  hMuonQualityNHitsGlb->Write ();
  hMuonQualityNHitsSta->Write();
  hMuonQualityNVHitsGlb->Write ();
  hMuonQualityNVHitsSta->Write();

  hThetaEffDen->Write();
  hThetaEffNum1->Write();
  hThetaEffNum2->Write();
  hThetaEffNum3->Write(); 
  hThetaEffNum4->Write();
  hNAvThetaHits->Write();  

  hThetaHitsPosition1->Write();
  hThetaHitsPosition2->Write();
  hThetaHitsPosition3->Write();
  hThetaHitsPosition4->Write();
  hThetaHitsPosition5->Write();
  hDistAv->Write();
  hDistHits->Write();
  hDistHits2L->Write();


  theFile->Close();
}

void TTreeReader::analyse(const int nEventMax) {
  int max = tree->GetEntries();
  if(nEventMax != -1) max = nEventMax;
  begin();
  for(int i = 0; i < max; i++) {

    tree->GetEntry(i);

      if(i%25000 == 0 ||  debug > 2) {
	cout << "-----  Process event " << i << endl;
      }
    
    if (filterEvents>=1) {
      if (run> 50000) { // if you happen to use this with MC...
	if (runmin>0 && run<runmin) continue;
	if (runmax>0 && run>=runmax) continue;
      }

      bool tagEvent=false;
      for(int iMu=0; iMu < muons->GetEntriesFast(); iMu++) { // loop over events
	DTMuObject *oneMu = (DTMuObject *) muons->At(iMu);	
	// type 5 = STA only
	if (fabs(oneMu->eta)<1.2 && oneMu->type!=5 && fabs(oneMu->qpt) >ptmin) tagEvent=true;	
      }
      if (!tagEvent) continue;
    }

    processEvent(i);
    nevents++;
  }
  end();
}




// build a detid depending on the wanted ganularity
DTDetId TTreeReader::buildDetid(int wheel, int station, int sector, int sl, int layer, int wire) const {
  if(theGranularity == 1) { // SL
    return DTDetId(wheel, station, sector, sl, 0, 0);
  } else if(theGranularity == 2) { // Station
    return DTDetId(wheel, station, 0, 0, 0, 0);
  } else if(theGranularity == 3) { // statByView : Sl3 is also merged with 1
    return DTDetId(wheel, station, 0, sl, 0, 0);
  } else if(theGranularity == 4) { // chamberByView : Sl3 is also merged with 1
    return DTDetId(wheel, station, sector, sl, 0, 0);
  } else if(theGranularity == 5) { // statBySL
    return DTDetId(wheel, station, 0, sl, 0, 0);
  } else if(theGranularity == 6) { // statByLayer
    return DTDetId(wheel, station, 0, sl, layer, 0);
  } else if(theGranularity == 7) { // chamberByLayer
    return DTDetId(wheel, station, sector, sl, layer, 0);
  } else if(theGranularity == 13) { // abs(W), statByView : Sl3 is also merged with 1
    return DTDetId(abs(wheel), station, 0, sl, 0, 0);
  }
  

  return DTDetId(0, 0, 0, 0, 0, 0);
  
}


void TTreeReader::setGranularity(const TString& granularity) {
  if(granularity == "SL" || granularity == "sl") {
    theGranularity = 1;
    cout << "Granularity: SL" << endl;
  } else if(granularity == "Station" || granularity == "station") {
    cout << "Granularity: Station" << endl;
    theGranularity = 2;
  } else if(granularity == "statByView") {
    cout << "Granularity: Station by view" << endl;
    theGranularity = 3;
  }  else if(granularity == "chamberByView") {
    cout << "Granularity: Chamber by view" << endl;
    theGranularity = 4;
  } else if(granularity == "statBySL") {
    cout << "Granularity: Station by SL" << endl;
    theGranularity = 5;
  } else if(granularity == "statByLayer") {
    cout << "Granularity: Station by Layer" << endl;
    theGranularity = 6;
  } else if(granularity == "chamberByLayer") {
    cout << "Granularity: Chamber by Layer" << endl;
    theGranularity = 7;
  } else if(granularity == "absWStatByView") {
    cout << "Granularity: Station by view, |W|" << endl;
    theGranularity = 13;
  }

}
// TString TTreeReader::getNameFromDetId(const DTDetId& detId) const {
//   stringstream wheelStr; 
//   if(detId.wheel == 0) wheelStr << "all";
//   else wheelStr << detId.wheel;

//   stringstream stationStr; 
//   if(detId.station == 0) stationStr << "all";
//   else stationStr << detId.station;

//   stringstream sectorStr; 
//   if(detId.sector == 0) sectorStr << "all";
//   else sectorStr << detId.sector;

//   stringstream slStr; 
//   if(detId.sl == 0) slStr << "all";
//   else slStr << detId.sl;

//   stringstream layerStr; 
//   if(detId.layer == 0) layerStr << "all";
//   else layerStr << detId.layer;

//   string namestr = "Wh" + wheelStr.str() +
//     "_St" + stationStr.str() + 
//     "_Se" + sectorStr.str();
    
//   if(detId.sl != 0) {
//     namestr = namestr + "_SL" + slStr.str();
//   }
//   if(detId.layer != 0) {
//     namestr = namestr + "_L" + layerStr.str();
//   }

//   return TString(namestr.c_str());
// }





void TTreeReader::setDebug(int dbg) {
  debug = dbg;
}



void TTreeReader::setCuts(const TString& set, const DTCut& cut) {
  cutSets[set] = cut;
  cout << "--- Set cut: " << set << endl;
  cout << cut << endl;
}




bool insideThetaWindow(float theta, int wheel, int station) {
  
  double zMax=-1;
  double zMin=-1;
  double r=-1;

  if( station==1){
    r=4.44; 
  }
  else if(station==2){
    r=5.23;
  }
  else if(station==3){
    r=6.30;
  }

  if ( wheel==0){   
    zMin=0    ;
    zMax=1.199; 
  }
  else if ( TMath::Abs(wheel)==1 ){
    zMin=1.4785;
    zMax=3.8765;
  }
  else if (TMath::Abs(wheel)==2){
    zMin=4.1345;
    zMax=6.5325;
  } 
    
  float thetaMax =TMath::ATan(zMax/r);
  float thetaMin =TMath::ATan(zMin/r);


  if (wheel==0) {
    //  cout<<thetaMax<<endl; 
    return (TMath::Abs(theta)<thetaMax);
  }

  //    cout << -thetaMax << " " << theta << -thetaMin << " " << (theta>-thetaMax && theta < -thetaMin) << endl;
  return (theta>-thetaMax && theta < -thetaMin);
}




void  TTreeReader::setCalibrationMap(const std::string& filename,
				     const std::string& granularity,
				     unsigned int fields) {
  readCalibTable = true;
  calibMap = new DTCalibrationMap(filename, granularity, fields);
}
