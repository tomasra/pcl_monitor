#include "CondCore/Utilities/interface/Utilities.h"

#include "CondCore/DBCommon/interface/DbScopedTransaction.h"
#include "CondCore/DBCommon/interface/Exception.h"
#include "CondCore/MetaDataService/interface/MetaData.h"

#include "CondCore/DBCommon/interface/Time.h"
#include "CondFormats/Common/interface/TimeConversions.h"

#include "CondCore/IOVService/interface/IOVProxy.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"

#include <boost/program_options.hpp>
#include <iterator>
#include <iostream>

#include "TFile.h"
#include "TGraphErrors.h"
#include "TVectorD.h"

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
	// <<"\nPayloadContainerName "<<payloadContainer<<"\n"
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

      for (cond::IOVProxy::const_iterator ioviterator=iov.begin(); ioviterator!=iov.end(); ioviterator++) {
        std::cout<<ioviterator->since() << " \t "<<ioviterator->till() <<" \t "<<ioviterator->token();



	RunNumber_t run_since = static_cast<RunNumber_t>(ioviterator->since() >> shift);
	LuminosityBlockNumber_t lumi_since = static_cast<LuminosityBlockNumber_t>(std::numeric_limits<unsigned int>::max() & ioviterator->since());

	RunNumber_t run_till = static_cast<RunNumber_t>(ioviterator->till() >> shift);
	LuminosityBlockNumber_t lumi_till = static_cast<LuminosityBlockNumber_t>(std::numeric_limits<unsigned int>::max() & ioviterator->till());

	std::cout << "\nrun:lumi = " << run_since << ":" << lumi_since << " -> " << run_till << ":" << lumi_till << std::endl;
	if(theRun == 0) { // save the first run #
	  theRun = run_since;
	}
	
        if (details) {
//           pool::RefBase wrapper =
//             session.getObject(ioviterator->wrapperToken());
//           std::cout << " \t "<< wrapper.summary();

	  //pool::Ref<BeamSpotObjects> bs =
          //  session.getTypedObject<BeamSpotObjects>(ioviterator->wrapperToken());

	  boost::shared_ptr<BeamSpotObjects> bs =
            session.getTypedObject<BeamSpotObjects>(ioviterator->token());

 	  if (bs) {
	    const BeamSpotObjects mybs = *bs;
	    std::cout << std::endl << mybs << std::endl;


	    // fill the plots
	    x0[counter] = mybs.GetX();
	    x0_err[counter] = mybs.GetBeamWidthX();// FIXME: check
	    y0[counter] = mybs.GetY();
	    y0_err[counter] = mybs.GetBeamWidthY();// FIXME: check
	    sigmaZ[counter] = mybs.GetSigmaZ();
	    sigmaZ_err[counter] = mybs.GetSigmaZError();


	    if (lumi_till == 4294967295) {
	      lumi_till = lumi_since + 1;
	    }

	    iovs[counter] = lumi_since + ((lumi_till - lumi_since)/2.);
	    iovs_err[counter] = (lumi_till  - lumi_since)/2.; 
	    cout << " new point: " << iovs[counter] << " +/- " << iovs_err[counter] << " " << x0[counter] << endl;
	    
// 	    if(previousSince == 0) {
// 	      previousSince = lumi_since;
// 	      prevX0 = mybs.GetX();
// 	      prevY0 = mybs.GetY();
// 	    } else {
	      
// 	    }


 	  }
        }
        std::cout<<std::endl;
        ++counter;
      }
      bool doPlot = hasOptionValue("doPlot");
      if(doPlot) {
	stringstream fileName; fileName << tag << "_" << theRun << ".root";
	TFile file(fileName.str().c_str(),"RECREATE");

	file.cd();

	

	TGraphErrors graph_x0(iovs, x0, iovs_err, x0_err);
	graph_x0.SetName("gX0");
	stringstream streamX; streamX << "run #: " << theRun << "  X0 (cm)";
	graph_x0.SetTitle(streamX.str().c_str());

	cout << " # of points: " << graph_x0.GetN() << endl;
	graph_x0.Write();

	TGraphErrors graph_y0(iovs, y0, iovs_err, y0_err);
	graph_y0.SetName("gY0");
	stringstream streamY; streamY << "run #: " << theRun << "  Y0 (cm)";
	graph_y0.SetTitle(streamY.str().c_str());
	cout << " # of points: " << graph_y0.GetN() << endl;
	graph_y0.Write();

	TGraphErrors graph_sigmaZ(iovs, sigmaZ, iovs_err, sigmaZ_err);
	graph_sigmaZ.SetName("gSIGMAZ");
	stringstream streamSigmaZ; streamSigmaZ << "run #: " << theRun << "  sigma-z (cm)";
	graph_sigmaZ.SetTitle(streamSigmaZ.str().c_str());

	cout << " # of points: " << graph_sigmaZ.GetN() << endl;
	graph_sigmaZ.Write();



	file.Close();
      }
      std::cout<<"Total # of payload objects: "<<counter<<std::endl;
    }
  }
  return 0;
}

  
int main( int argc, char** argv ){

  cond::ListIOVUtilities utilities;
  return utilities.run(argc,argv);
}

