{

  TFile *f = new TFile("histo_t0.root");
  f->cd();


  


  //qui ci metti il tuo cazzo di loop che ti fa sentire figo

  {

    //posto che il tuo histo del cazzo di chiama myhisto ed e' un puntatore
    TH1F* myhisto = (TH1F*)f->Get("Wh-1_St1_Se10_SL2_hResDist");

    RooDataHist hdata("hdata","Binned data",RooArgList(x),myhisto);

    RooFitResult *fitRes = myg.fitTo(hdata,RooFit::Minos(0),RooFit::Range(-0.1,0.1),RooFit::Save(1));

    res_mean = mean.getVal();
    res_sigma = sigma1.getVal();

    RooPlot *xplot = x.frame();
    hdata->plotOn(xplot);
    myg->plotOn(xplot);
    
    cout << "sigma mean: " << sigmaAM.getVal() << endl;

    chi2 = xplot->chiSquare();

    res_tree->Fill();

  }

  TFile out("gianluca_merda.root","RECREATE");
  out.cd();
  res_tree->Write();
  out.Close();


}
