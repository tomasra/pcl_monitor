
Bool_t AddJob(FGJob **ListBase, FGJob *Element)
{
  FGJob *Hook;
  Hook = *ListBase;
  while (Hook != 0)
  {
    if (Hook -> FileName == Element -> FileName)
    {
      //cout << "Eliminato doppione \n";
      return kFALSE;
    }
    Hook = Hook -> Next;
  };

  while (*ListBase != 0 &&
         ((float)(**ListBase).SampleCount * (**ListBase).Normalization) < ((float)(*Element).SampleCount * (*Element).Normalization))
  {
    ListBase = &((**ListBase).Next);
  }
  Element -> Next = *ListBase;
  *ListBase = Element;

  return kTRUE;
}

Bool_t LoadJobQueue(TString fPath)
{
  FILE *hFile;
  char Buffer[512];
  Int_t LineLen;
  string sss;
  TString ss1;
  Int_t ElabState, Progressive = 0;
  FGJob *Job;
  FGJob **Tail;

  //fPath.Remove(fPath.Length() - 1, 1);
  hFile = fopen(fPath.Data(), "r");
  if (hFile == 0) {cout << "Impossibile aprire il job file, operazione abortita.\n"; perror("Errore"); return kFALSE;};
  Tail = &JobQueue;

  while (!feof(hFile))
  {
    fgets (Buffer, 512, hFile);
    if (Buffer[0] != '#')
    {
      for (LineLen = 0; Buffer[LineLen] != ';'; LineLen++);
      sss = string(Buffer, LineLen);
      //cout << sss << "\n";

      Job = new FGJob;

      ss1.Clear();
      ElabState = 0;
      Job -> ProgressiveId = Progressive;
      Job -> Label = new TString("");
      Progressive++;

      for (UInt_t k = 0; k < sss.length(); k++)
      {
	if (sss.at(k) == ' ')
	{
	  if (ss1.Length() > 0)
	  {
            switch (ElabState)
	    {
	    case 0: Job -> FinalState = ss1; break;
	    case 1: Job -> FileName = ss1; break;
	    case 2: Job -> SampleCount = ss1.Atoi(); break;
	    case 3: Job -> XSection = ss1.Atof(); break;
	    case 4: Job -> BranchingRatio = ss1.Atof(); break;
            case 5: Job -> toSynopsis = ss1.Contains("Y"); break;
            case 6: Job -> isMC = ss1.Contains("Y"); break;
            case 7: {ss1.ReplaceAll("-", " "); Job -> Label -> Append(ss1);}; break;
	    case 8: Job -> Dataset = ss1.Atoi(); break;
	    }
	    ElabState++;
	    ss1.Clear();
	  }
       	} else ss1.Append(sss.at(k));
      }
      Job -> Normalization = (Job->XSection) * (Job->BranchingRatio) / (Job->SampleCount);
      Job -> ContentSum = 0;

      AddJob(&JobQueue, Job);
    }
  }
  fclose(hFile);
  return kTRUE;
}

Int_t CountJobs(FGJob *Job)
{
  Int_t TempRes = 0;
  while (Job != 0)
  {
    TempRes++;
    Job = Job -> Next;
  }

  return TempRes;
}

void PrintJobQueue()
{
  FGJob *Hook;

  Hook = JobQueue;
  while (Hook != 0)
  {
    cout << "Progressive id: " << (Hook -> ProgressiveId) << "\n";
    cout << "Final state: '" << (Hook -> FinalState) << "'\n";
    cout << "File name: '" << (Hook -> FileName) << "'\n";
    cout << "Sample count: " << (Hook -> SampleCount) << "\n";
    cout << "Cross section: " << (Hook -> XSection) << "\n";
    cout << "Branching ratio: " << (Hook -> BranchingRatio) << "\n";
    cout << "To synopsis: " << (Hook -> toSynopsis) << "\n";
    cout << "Dataset: " << (Hook -> Dataset) << "\n\n";

    Hook = Hook -> Next;
  }
}
