
Color_t FGColor(Int_t IdCol)
{
  Color_t TempRes = 0;
  switch(IdCol % 12)
  {
  case 0: TempRes = kRed; break;
  case 1: TempRes =  kGreen; break;
  case 2: TempRes = kBlue; break;
  case 3: TempRes = kYellow; break;
  case 4: TempRes =  kMagenta; break;
  case 5: TempRes = kCyan; break;
  case 6: TempRes = kOrange; break;
  case 7: TempRes =  kSpring; break;
  case 8: TempRes = kTeal; break;
  case 9: TempRes = kAzure; break;
  case 10: TempRes =  kViolet; break;
  case 11: TempRes = kPink; break;
  }

  TempRes += (IdCol / 12);
  return TempRes;
}

Color_t FGColor2(Int_t IdCol)
{
  Color_t TempRes = 0;
  switch(IdCol % 6)
  {
  case 0: TempRes = kBlack; break;
  case 1: TempRes =  kGray + 3; break;
  case 2: TempRes = kGray + 2; break;
  case 3: TempRes = kGray + 1; break;
  case 4: TempRes =  kGray; break;
  case 5: TempRes = kWhite; break;
  }

  return TempRes;
}
