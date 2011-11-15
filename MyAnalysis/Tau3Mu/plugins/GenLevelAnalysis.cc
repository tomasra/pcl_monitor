

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

// #include "DataFormats/VertexReco/interface/Vertex.h"
// #include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/Candidate/interface/Particle.h"

#include "MyAnalysis/Tau3Mu/src/Histograms.h"


#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <TMath.h>
#include <iostream>

using namespace std;


// #include "CLHEP/Units/GlobalPhysicalConstants.h"

// #include "Hgg/ClusteringWithPU/interface/SCwithPUhistos.h"
// #include "Hgg/ClusteringWithPU/interface/Utils.h"

// pdg particle numbering : higgs->25, Z0->23
// http://pdg.lbl.gov/mc_particle_id_contents.html



class GenLevelAnalysis : public edm::EDAnalyzer {
public:
  explicit GenLevelAnalysis(const edm::ParameterSet&);
  ~GenLevelAnalysis();

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;


  
  HistoKin *hKinDs;
  HistoKin *hKinTau;
  HistoKin *hKinMu;
  
  int counter;
  int countInAccept;
  int counterMoreThan3Muons;
  int counterMoreThanOneds;
  int counterTaus;

};



//
// constants, enums and typedefs
//


//////////////////////////////////////////////////////////////////
// generically maximum
template <class T> const T& max ( const T& a, const T& b ) {
  return (b<a)?a:b;     // or: return comp(b,a)?a:b; for the comp version
}


//


GenLevelAnalysis::GenLevelAnalysis(const edm::ParameterSet& iConfig) {
  counter = 0;
  countInAccept = 0;
  counterMoreThan3Muons = 0;
  counterMoreThanOneds = 0;
  counterTaus = 0;
}

GenLevelAnalysis::~GenLevelAnalysis() {}


//
// member functions
//

// ------------ method called to for each event  ------------
void GenLevelAnalysis::analyze(const edm::Event& ev, const edm::EventSetup& iSetup) {

  using namespace edm;
  using namespace reco;
  using namespace std;
  
  // get the gen level particles
  Handle<HepMCProduct> hepProd ;
  ev.getByLabel("generator",hepProd) ;
  const HepMC::GenEvent * myGenEvent = hepProd->GetEvent();

//   HepMC::GenParticle* theZ=0;
//   HepMC::GenParticle* theGamma=0;
  
  // TODO:
  // 1. plot the mother of all Ds
  // 2. plot the kinematics of all Ds
  // 3. plot the kinematics of all Taus
  
  // DOCUMENTS:
  // https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate#GenPCand
  // http://pdg.lbl.gov/mc_particle_id_contents.html


  vector<HepMC::GenParticle *> muonsFromTau;
  vector<HepMC::GenParticle *> particlesDs;
  vector<HepMC::GenParticle *> particlesTau;


  cout << "--- new event ---" << endl;
  // loop over MC-truth particles
  for ( HepMC::GenEvent::particle_const_iterator part = myGenEvent->particles_begin();
	part != myGenEvent->particles_end(); ++part ) {

    HistoKin *histo = 0;

    if(abs((*part)->pdg_id()) == 431) { //D_s
      if(particlesDs.size() != 0) cout << "More than one Ds in this event" << endl;
      particlesDs.push_back(*part);
      histo = hKinDs;
    } else if(abs((*part)->pdg_id()) == 15) {//tau
      particlesTau.push_back(*part);
      histo = hKinTau;
    } else if(abs((*part)->pdg_id()) == 13) {//muon
      histo = hKinMu;
    } else continue;
    
    std::cout << "initial  particle with pdg is: " << (*part)->pdg_id() << " with status: " << (*part)->status() << std::endl;

    HepMC::GenParticle* mother1  = 0;
    HepMC::GenParticle* mother2  = 0;

    
    
    // get the other mothers from the vertex
    if((*part)->production_vertex()) {
      if((*part)->production_vertex()->particles_begin(HepMC::parents) !=  (*part)->production_vertex()->particles_end(HepMC::parents))
	mother1 = *((*part)->production_vertex()->particles_begin(HepMC::parents));
    }

    if(mother1 !=0 && mother1->production_vertex()) {
      mother2 = *( mother1->production_vertex()->particles_begin(HepMC::parents));
    }

    cout << " mother1: " << mother1->pdg_id()
	 << " mother2: " << mother2->pdg_id() << endl;

    if(abs(mother1->pdg_id()) == 15 || abs(mother2->pdg_id()) == 15) {
	if(abs((*part)->pdg_id()) == 13) {
	  cout << "Muon from tau, pt: " << (*part)->momentum().perp() << " eta: " << (*part)->momentum().pseudoRapidity() << endl;
// 	  if(fabs((*part)->momentum().pseudoRapidity()) < 2.4 && (*part)->momentum().perp() > 1) {
	    muonsFromTau.push_back(*part);
// 	  }
	}
      }


    histo->Fill((*part)->momentum().perp(), (*part)->momentum().pseudoRapidity(), (*part)->momentum().phi(), (*part)->momentum().m(), 1);



//     // require that higgs is the mother
//     if (!    	(mother == 0 || (mother2!=0 && mother2->pdg_id()==25) ) 	) continue;

//     std::cout << "found a particle with higgs as a mother. Its pdg is: " << (*part)->pdg_id() << std::endl; 

//     if      ( (*part)->pdg_id()==22 ) theGamma = (*part);
//     else if ( (*part)->pdg_id()==23 ) theZ     = (*part);

  }// loop over all MC-truth particles  - keep only electrons or photons 
  
//  math::XYZTLorentzVector momentumGamma(theGamma->momentum().px(),
//					theGamma->momentum().py(),
//					theGamma->momentum().pz(),
//					theGamma->momentum().e() );
//  math::XYZTLorentzVector momentumZ(theZ->momentum().px(),
//				    theZ->momentum().py(),
//				    theZ->momentum().pz(),
//				    theZ->momentum().e() );
  
  
//   TLorentzVector momentumGamma(theGamma->momentum().px(),
// 			       theGamma->momentum().py(),
// 			       theGamma->momentum().pz(),
// 			       theGamma->momentum().e() );
//   TLorentzVector momentumZ(theZ->momentum().px(),
// 			   theZ->momentum().py(),
// 			   theZ->momentum().pz(),
// 			   theZ->momentum().e() );
  
//   h_ZGammaMass -> Fill( (momentumGamma + momentumZ).Mag()  );
  
//   TVector3 Zp3     = momentumZ.Vect();
//   TVector3 Gammap3 = momentumGamma.Vect();
  
//   float    cosTheta = (Zp3 * Gammap3) / Zp3.Mag() / Gammap3.Mag();
//   h_CosTheta -> Fill(cosTheta);

  counter++;
  if(muonsFromTau.size() > 2) {
    countInAccept++;
    if(muonsFromTau.size() > 3) {
      counterMoreThan3Muons++;
    }
  }  
    
  if(particlesTau.size() > 1) counterTaus++;
  if(particlesDs.size() > 1) counterMoreThanOneds++;
    
    
}

// ------------ method called once each job just before starting event loop  ------------
void GenLevelAnalysis::beginJob() {
  edm::Service<TFileService> fs;

  hKinDs  = new HistoKin("Ds",*fs);
  hKinTau = new HistoKin("Tau",*fs);
  hKinMu  = new HistoKin("Mu",*fs);
  
}


// ------------ method called once each job just after ending the event loop  ------------
void 
GenLevelAnalysis::endJob() {
  cout << "Total # events: " << counter << endl;
  cout << "   # events with muons in acceptance: " << countInAccept << endl;
  cout << "   # events with more than 1 Ds: " << counterMoreThanOneds << endl;
  cout << "   # events with more than 3 muons: " << counterMoreThan3Muons << endl;
  cout << "   # events with more than 1 tau: " << counterTaus << endl;
}



#include "FWCore/Framework/interface/MakerMacros.h"  
DEFINE_FWK_MODULE( GenLevelAnalysis );
