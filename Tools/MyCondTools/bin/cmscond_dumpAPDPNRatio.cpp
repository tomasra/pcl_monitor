#include "CondCore/Utilities/interface/Utilities.h"

#include "CondCore/DBCommon/interface/DbScopedTransaction.h"
#include "CondCore/DBCommon/interface/Exception.h"
#include "CondCore/MetaDataService/interface/MetaData.h"

#include "CondCore/DBCommon/interface/Time.h"
#include "CondFormats/Common/interface/TimeConversions.h"

#include "CondCore/IOVService/interface/IOVProxy.h"
#include "CondFormats/EcalObjects/interface/EcalLaserAPDPNRatios.h"
#include "CondFormats/DataRecord/interface/EcalLaserAPDPNRatiosRcd.h"
#include "CondFormats/EcalObjects/interface/EcalLaserAPDPNRatiosRef.h"
#include "CondFormats/DataRecord/interface/EcalLaserAPDPNRatiosRefRcd.h"

#include <boost/program_options.hpp>
#include <iterator>
#include <iostream>

#include "TFile.h"
#include "TGraphErrors.h"
#include "TVectorD.h"
#include "TProfile2D.h"

using namespace std;

namespace cond {
  class ListIOVUtilities : public Utilities {
    public:
      ListIOVUtilities();
      ~ListIOVUtilities();
      int execute();
  };
}

cond::ListIOVUtilities::ListIOVUtilities():Utilities("cmscond_list_iov"){
  addConnectOption();
  addAuthenticationOptions();
  addOption<bool>("verbose","v","verbose");
  addOption<bool>("all","a","list all tags(default mode)");
  addOption<bool>("summary","s","stprint also the summary for each payload");
  addOption<cond::Time_t>("beginTime","b","begin time (first since) (optional)");
  addOption<cond::Time_t>("endTime","e","end time (last till) (optional)");
  addOption<bool>("doPlot","p","Produce some plots for the selected interval(optional)");

  addOption<std::string>("tag","t","list info of the specified tag");
}

cond::ListIOVUtilities::~ListIOVUtilities(){
}

int cond::ListIOVUtilities::execute(){
  initializePluginManager();
  
  bool listAll = hasOptionValue("all");
  cond::DbSession session = openDbSession( "connect", true );
  if( listAll ){
    cond::MetaData metadata_svc(session);
    std::vector<std::string> alltags;
    cond::DbScopedTransaction transaction(session);
    transaction.start(true);
    metadata_svc.listAllTags(alltags);
    transaction.commit();
    std::copy (alltags.begin(),
               alltags.end(),
               std::ostream_iterator<std::string>(std::cout,"\n")
	       );
  }else{
    std::string tag = getOptionValue<std::string>("tag");
    cond::MetaData metadata_svc(session);
    std::string token;
    cond::DbScopedTransaction transaction(session);
    transaction.start(true);
    token=metadata_svc.getToken(tag);
    transaction.commit();

    cond::Time_t since = std::numeric_limits<cond::Time_t>::min();
    if( hasOptionValue("beginTime" )) since = getOptionValue<cond::Time_t>("beginTime");
    cond::Time_t till = std::numeric_limits<cond::Time_t>::max();
    if( hasOptionValue("endTime" )) till = getOptionValue<cond::Time_t>("endTime");



    {
      bool verbose = hasOptionValue("verbose");
      bool details = hasOptionValue("summary");
      cond::IOVProxy iov( session, token);
      
      since = std::max(since, cond::timeTypeSpecs[iov.timetype()].beginValue);
      till  = std::min(till,  cond::timeTypeSpecs[iov.timetype()].endValue);
      iov.range(since,till);
 
      unsigned int counter=0;
      // std::string payloadContainer=iov.payloadContainerName();
      std::cout<<"Tag "<<tag;
      if (verbose) std::cout << "\nStamp: " << iov.iov().comment()
                             << "; time " <<  cond::time::to_boost(iov.iov().timestamp())
                             << "; revision " << iov.iov().revision();
      std::cout <<"\nTimeType " << cond::timeTypeSpecs[iov.timetype()].name
	//          <<"\nPayloadContainerName "<<payloadContainer<<"\n"
                <<"since \t till \t payloadToken"<<std::endl;

      static const unsigned int nIOVS = std::distance(iov.begin(), iov.end());

      // std::cout << "# of IOVs: " << nIOVS  << std::endl;
      
      TVectorD x0(nIOVS);
      TVectorD x0_err(nIOVS);
      TVectorD y0(nIOVS);
      TVectorD y0_err(nIOVS);
      TVectorD sigmaZ(nIOVS);
      TVectorD sigmaZ_err(nIOVS);

      TVectorD iovs(nIOVS);
      TVectorD iovs_err(nIOVS);

      typedef unsigned int LuminosityBlockNumber_t;
      typedef unsigned int RunNumber_t;
      static unsigned int const shift = 8 * sizeof(unsigned int);
//       LuminosityBlockNumber_t previousSince = 0;
//       double prevX0 = 0;
//       double prevY0 = 0;
//       double runningX0Mean = 0;
//       double runningY0Mean = 0;
//       double nPoints = 0;
      
      RunNumber_t theRun = 0;
      TFile file("pippo.root","recreate");
      file.cd();
      TProfile2D *ebMean = new TProfile2D("ebMean","Corrections EB", 360, 0, 360, 170,-85,85,"S");
      TProfile2D *eepMean = new TProfile2D("eepMean","Corrections EE+", 100, 0, 100, 100,0,100,"S");
      TProfile2D *eemMean = new TProfile2D("eemMean","Corrections EE-", 100, 0, 100, 100,0,100,"S");

      TProfile2D *ebRMS = new TProfile2D("ebRMS","Corrections EB", 360, 0, 360, 170,-85,85);
      TProfile2D *eepRMS = new TProfile2D("eepRMS","Corrections EE+", 100, 0, 100, 100,0,100);
      TProfile2D *eemRMS = new TProfile2D("eemRMS","Corrections EE-", 100, 0, 100, 100,0,100);

      TH2D *ebMax = new TH2D("ebMax","Corrections max EB", 360, 0, 360, 170,-85,85);
      TH2D *eepMax = new TH2D("eepMax","Corrections max EE+", 100, 0, 100, 100,0,100);
      TH2D *eemMax = new TH2D("eemMax","Corrections max EE-", 100, 0, 100, 100,0,100);

      //      map<uint32_t, 

      for (cond::IOVProxy::const_iterator ioviterator=iov.begin(); ioviterator!=iov.end(); ioviterator++) {
        std::cout<<ioviterator->since() << " \t "<<ioviterator->till() <<" \t "<<ioviterator->token();


	/*
	RunNumber_t run_since = static_cast<RunNumber_t>(ioviterator->since() >> shift);
	LuminosityBlockNumber_t lumi_since = static_cast<LuminosityBlockNumber_t>(std::numeric_limits<unsigned int>::max() & ioviterator->since());

	RunNumber_t run_till = static_cast<RunNumber_t>(ioviterator->till() >> shift);
	LuminosityBlockNumber_t lumi_till = static_cast<LuminosityBlockNumber_t>(std::numeric_limits<unsigned int>::max() & ioviterator->till());

	std::cout << "\nrun:lumi = " << run_since << ":" << lumi_since << " -> " << run_till << ":" << lumi_till << std::endl;
	if(theRun == 0) { // save the first run #
	  theRun = run_since;
	}
	*/
	
	
	double alpha = 1.5;

        if (details) {
//           pool::RefBase wrapper =
//             session.getObject(ioviterator->wrapperToken());
//           std::cout << " \t "<< wrapper.summary();

	  //pool::Ref<BeamSpotObjects> bs =
          //  session.getTypedObject<BeamSpotObjects>(ioviterator->wrapperToken());

	  boost::shared_ptr<EcalLaserAPDPNRatios> bs =
            session.getTypedObject<EcalLaserAPDPNRatios>(ioviterator->token());

	  
	  


 	  if (bs) {
	    const EcalLaserAPDPNRatios myRatios = *bs;
// 	    std::cout << std::endl << myRatios << std::endl;

	    const EcalLaserAPDPNRatios::EcalLaserAPDPNRatiosMap& laserRatiosMap = myRatios.getLaserMap(); 
	    const EcalLaserAPDPNRatios::EcalLaserTimeStampMap& laserTimeMap = myRatios.getTimeMap(); 


	    for (int cellid = 0; 
		 cellid < EBDetId::kSizeForDenseIndexing; 
		 ++cellid){// loop on EB cells
    
    
	      uint32_t rawid = EBDetId::unhashIndex(cellid);
	      EcalLaserAPDPNRatios::EcalLaserAPDPNpair corPair = laserRatiosMap[rawid];
	      //cout << rawid << " " << corPair.p1 << " " << corPair.p2 << endl;
	      EBDetId ebid(rawid);
	      int iEta = ebid.ieta();
	      int iphi = ebid.iphi();
	      double correctionFactor = 1/pow(corPair.p1, alpha);
	      double etafill = 0;
	      if(iEta < 0) {
		etafill = iEta;
	      } else if(iEta > 0) {
		etafill = iEta - 0.5;
	      }
	      ebMean->Fill(iphi-0.5, etafill, correctionFactor);
	      
	    }


	    for (int cellid = 0; 
		 cellid < EEDetId::kSizeForDenseIndexing; 
		 ++cellid){// loop on EB cells
    
    

	      if (EEDetId::validHashIndex(cellid)){  
		uint32_t rawid = EEDetId::unhashIndex(cellid);
		EcalLaserAPDPNRatios::EcalLaserAPDPNpair corPair = laserRatiosMap[rawid];
		//cout << rawid << " " << corPair.p1 << " " << corPair.p2 << endl;
		EEDetId ebid(rawid);
		int ix = ebid.ix();
		int iy = ebid.iy();
		int zside = ebid.zside();
	
		double correctionFactor = 1/pow(corPair.p1, alpha);
		if(corPair.p1 > 2 || corPair.p2 > 2 || correctionFactor > 2) {
		  cout << ix << " " << iy << " " << zside << " " << corPair.p1 << " " << corPair.p2 << " " << correctionFactor << endl;
		}
		
		if(zside > 0) {
		  eepMean->Fill(ix-0.5,iy-0.5,correctionFactor);
		} else {
		  eemMean->Fill(ix-0.5,iy-0.5,correctionFactor);
		}


	      }
	      
	    }


	    


	    // Barrel loop
// 	    cout << "All conditions: " << endl;
// 	    for(EcalLaserAPDPNRatios::EcalLaserAPDPNRatiosMap::const_iterator it = myRatios.getLaserMap().begin();
// 		it != myRatios.getLaserMap().end(); it++) {
// 	      cout << "DETID: " << (*it).first << " EcalAPDPnRatio: first " << (*it).second.p1 << " EcalAPDPnRatio: second " << (*it).second.p2 << endl;
// 	    }
	    EcalLaserAPDPNRatios::EcalLaserAPDPNRatiosMap::const_iterator apdPnRatiosit;
// 	    cout << "---- Barrel corrections" << endl;
// 	    for (apdPnRatiosit = laserRatiosMap.barrelItems().begin(); apdPnRatiosit != laserRatiosMap.barrelItems().end(); ++apdPnRatiosit) {
// 	      EcalLaserAPDPNRatios::EcalLaserAPDPNpair apdPnRatioPair = (*apdPnRatiosit);
	      
// 	      std::cout << "EcalAPDPnRatio: first " << apdPnRatioPair.p1 << " second " << apdPnRatioPair.p2 << std::endl;
// 	    } 
// 	    // Endcap loop
// 	    cout << "---- Endcap corrections" << endl;
// 	    for (apdPnRatiosit = laserRatiosMap.endcapItems().begin(); apdPnRatiosit != laserRatiosMap.endcapItems().end(); ++apdPnRatiosit) {
// 	      EcalLaserAPDPNRatios::EcalLaserAPDPNpair apdPnRatioPair = (*apdPnRatiosit);
// 	      std::cout << "EcalAPDPnRatio: first " << apdPnRatioPair.p1 << " second " << apdPnRatioPair.p2 << std::endl;
// 	    } 
// 	    //TimeStampLoop
// 	    for(unsigned int i=0; i<laserTimeMap.size(); ++i)
// 	      {
// 		EcalLaserAPDPNRatios::EcalLaserTimeStamp timestamp = laserTimeMap[i];  
// 		std::cout << "EcalAPDPnRatio: timestamp : "  
// 			  << i << " " << timestamp.t1.value() << " , " << timestamp.t2.value() << endl;
// 	      }
	    



 	  }
        }
        std::cout<<std::endl;
        ++counter;
      }
      std::cout<<"Total # of payload objects: "<<counter<<std::endl;

      for(int xbin = 1; xbin < 361; xbin++) {
	double xValue = ebMean->GetXaxis()->GetBinCenter(xbin);
	for(int ybin = 1; ybin < 171; ybin++) {
	double yValue = ebMean->GetYaxis()->GetBinCenter(ybin);
	  
	  ebRMS->Fill(xValue, yValue, ebMean->GetBinError(xbin, ybin));
// 	  cout << xbin << " " << ybin << endl;
	}
      }
      
      for(int xbin = 1; xbin < 101; xbin++) {
	double xValue = eepMean->GetXaxis()->GetBinCenter(xbin);
	for(int ybin = 1; ybin < 101; ybin++) {
	  double yValue = eepMean->GetYaxis()->GetBinCenter(ybin);
	  eepRMS->Fill(xValue, yValue, eepMean->GetBinError(xbin, ybin));
	  eemRMS->Fill(xValue, yValue, eemMean->GetBinError(xbin, ybin));
// 	  cout << xbin << " " << ybin << endl;
	}
      }
      cout << "done" << endl;

      ebRMS->Write();
      eepRMS->Write();
      eemRMS->Write();
      ebMean->Write();
      eepMean->Write();
      eemMean->Write();
      file.Close();
    }
  }
  return 0;
}

  
int main( int argc, char** argv ){

  cond::ListIOVUtilities utilities;
  return utilities.run(argc,argv);
}

