

#include <map>
#include <cmath>
#include "../root_lib/DTDetId.h"

using namespace std;

void rangeAngle(DTDetId id, float& min, float& max) {
//   abs(id.wheel)
//   id.station
//   id.sl  
  
  //   W       St
  map<int, map<int, float> > m_min;
  map<int, map<int, float> > m_max;

// map<float, map<float, float> > m_min;
//  map<float, map<float, float> > m_max;

  if (id.sl !=2 ) { // phi
    m_min[2][3] = -0.2;
    m_min[2][2] = -0.3;
    m_min[2][1] = -0.15;
    m_min[1][3] = m_min[2][3];
    m_min[1][2] = m_min[2][2];
    m_min[1][1] = m_min[2][1];
    m_min[0][3] = -0.25;
    m_min[0][2] = -0.25;
    m_min[0][1] = -0.2;
   

    m_max[2][3] = 0.25;
    m_max[2][2] = 0.2;
    m_max[2][1] = 0.3;
    m_max[1][3] = m_max[2][3];
    m_max[1][2] = m_max[2][2] ;
    m_max[1][1] = m_max[2][1];
    m_max[0][3] = 0.25;
    m_max[0][2] = 0.25;
    m_max[0][1] = 0.2;
   

  } else { //theta
    
    m_min[0][1] = -0.25;
    m_min[0][2] = -0.2;
    m_min[0][3] = -0.15;
    m_min[1][1] = -0.7;
    m_min[1][2] = -0.65;
    m_min[1][3] = -0.55;
    m_min[2][1] = -0.97;
    m_min[2][2] = -0.9;
    m_min[2][3] = -0.8;

    m_max[0][1] = 0.25;
    m_max[0][2] = 0.2;
    m_max[0][3] = 0.15;
    m_max[1][1] = -0.35;
    m_max[1][2] = -0.3;
    m_max[1][3] = -0.35;
    m_max[2][1] = -0.8;
    m_max[2][2] = -0.7;
    m_max[2][3] = -0.6;

 
 }

  min = m_min[abs(id.wheel)][id.station];
  max = m_max[abs(id.wheel)][id.station];
  
  //  min = m_min[id.wheel][id.station];
  //max = m_max[id.wheel][id.station];
  
  //  std::cout << "min" << min << endl;
  //std::cout << "max" << max << endl;

  if (id.sl!=2&&id.wheel<0) { // phi
    std::swap(min,max);
    min*=-1.;
    max*=-1;
  }

}

