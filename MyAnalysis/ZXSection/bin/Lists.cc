
struct FGIntList
{
  Int_t Value;
  FGIntList *Next;
};

struct FGFloatList
{
  Double_t Value;
  FGFloatList *Next;
};

struct FGStringList
{
  TString Value;
  FGStringList *Next;
};

void IntListAdd(FGIntList **Lista, Int_t Valore)
{
  FGIntList *Entry = new FGIntList;

  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void IntListOrderedAdd(FGIntList **Lista, Int_t Valore)
{
  FGIntList *Entry = new FGIntList;
  
  while (*Lista != 0 && (**Lista).Value < Valore) Lista = &((**Lista).Next);
  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void IntListEntry(FGIntList **Lista)
{
  FGIntList *Hook, *DelHook;

  Hook = *Lista;
  while (Hook != 0)
  {
    DelHook = Hook;
    Hook = Hook -> Next;
    delete DelHook;
  }
  *Lista = 0;
}

void FloatListAdd(FGFloatList **Lista, Double_t Valore)
{
  FGFloatList *Entry = new FGFloatList;

  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void FloatListOrderedAdd(FGFloatList **Lista, Float_t Valore)
{
  FGFloatList *Entry = new FGFloatList;
  
  while (*Lista != 0 && (**Lista).Value < Valore) Lista = &((**Lista).Next);
  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void FloatListEmpty(FGFloatList **Lista)
{
  FGFloatList *Hook, *DelHook;

  Hook = *Lista;
  while (Hook != 0)
  {
    DelHook = Hook;
    Hook = Hook -> Next;
    delete DelHook;
  }
  *Lista = 0;
}

void StringListAdd(FGStringList **Lista, TString Valore)
{
  FGStringList *Entry = new FGStringList;

  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void StringListOrderedAdd(FGStringList **Lista, TString Valore)
{
  FGStringList *Entry = new FGStringList;
  
  while (*Lista != 0 && (**Lista).Value.CompareTo(Valore) <= 0) Lista = &((**Lista).Next);
  Entry -> Next = *Lista;
  Entry -> Value = Valore;
  *Lista = Entry;
}

void StringListEmpty(FGStringList **Lista)
{
  FGStringList *Hook, *DelHook;

  Hook = *Lista;
  while (Hook != 0)
  {
    DelHook = Hook;
    Hook = Hook -> Next;
    delete DelHook;
  }
  *Lista = 0;
}

Int_t IntListCount(FGIntList **Lista)
{
  Int_t TempRes = 0;
  FGIntList *Hook = *Lista;

  while (Hook != 0)
  {
    Hook = Hook -> Next;
    TempRes++;
  }

  return TempRes;
}

Int_t FloatListCount(FGFloatList **Lista)
{
  Int_t TempRes = 0;
  FGFloatList *Hook = *Lista;

  while (Hook != 0)
  {
    Hook = Hook -> Next;
    TempRes++;
  }

  return TempRes;
}

Int_t StringListCount(FGStringList **Lista)
{
  Int_t TempRes = 0;
  FGStringList *Hook = *Lista;

  while (Hook != 0)
  {
    Hook = Hook -> Next;
    TempRes++;
  }

  return TempRes;
}

FGStringList *CharSplit(TString *Stringa, char Separator)
{
  FGStringList *TempRes = new FGStringList;
  FGStringList *Tail = TempRes;

  Tail -> Next = 0;
  for (Int_t i = 0; i < Stringa -> Length(); i++)
  {
    if (Stringa -> Data()[i] == Separator)
    {
      Tail -> Next = new FGStringList();
      Tail = Tail -> Next;
      Tail -> Next = 0;
    } else Tail -> Value.Append(Stringa -> Data()[i]);
  }

  return TempRes;
}

FGStringList *CharSplitNoParent(TString *Stringa, char Separator)
{
  FGStringList *TempRes = new FGStringList;
  FGStringList *Tail = TempRes;
  Int_t ParNo = 0;

  Tail -> Next = 0;
  for (Int_t i = 0; i < Stringa -> Length(); i++)
  {
    if (Stringa -> Data()[i] == Separator && ParNo == 0)
    {
      Tail -> Next = new FGStringList();
      Tail = Tail -> Next;
      Tail -> Next = 0;
    } else Tail -> Value.Append(Stringa -> Data()[i]);
    if (Stringa -> Data()[i] == '(') ParNo++;
    if (Stringa -> Data()[i] == ')') ParNo--;
  }

  return TempRes;
}

FGIntList *StringListToIntList(FGStringList *Lista)
{
  FGIntList *TempRes = 0;
  FGStringList *Hook = Lista;

  while (Hook != 0)
  {
    IntListAdd(&TempRes, Hook -> Value.Atoi());
    Hook = Hook -> Next;
  }

  return TempRes;
}

void PrintIntList(FGIntList *Lista)
{
  FGIntList *Hook = Lista;
  while (Hook != 0)
  {
    cout << Hook -> Value << " ";
    Hook = Hook -> Next;
  }
}

Bool_t PartOfIntList(FGIntList *Lista, Int_t Valore)
{
  FGIntList *Hook = Lista;
  while (Hook != 0 && Hook -> Value != Valore)
  {
    Hook = Hook -> Next;
  }

  return (Hook != 0);
}
