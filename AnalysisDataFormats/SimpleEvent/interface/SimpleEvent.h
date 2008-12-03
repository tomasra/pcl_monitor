#ifndef SimpleEvent_H
#define SimpleEvent_H

/** \class SimpleEvent
 *  No description available.
 *
 *  $Date: $
 *  $Revision: $
 *  \author G. Cerminara - INFN Torino
 */

#include <vector>

class SimpleEvent {
public:
  /// Constructor
  SimpleEvent() : theEventid(0),
		  theOrbitId(0), 
		  theBxId(0) {}

  /// Constructor
  SimpleEvent(int eventId, int orbitId, int bxId) : theEventid(eventId),
						    theOrbitId(orbitId), 
						    theBxId(bxId) {}

  /// Destructor
  virtual ~SimpleEvent() {}

  // Operations
  int eventId() const {
    return theEventid;
  }
  
  int orbitId() const {
    return theOrbitId;
  }

  int bxId() const {
    return theBxId;
  }
  
  int bxDist(const SimpleEvent& otherEvent) const {
    return abs(((otherEvent.orbitId()*3564)+otherEvent.bxId())-((theOrbitId*3564)+theBxId));
  }
  
  int evtDist(const SimpleEvent& otherEvent) const {
    return abs(theEventid-otherEvent.eventId());
  }
  
protected:

private:

  int theEventid;
  int theOrbitId;
  int theBxId;

};


class SimpleEventCollection : public  std::vector<SimpleEvent> {

public:
  bool mergeProduct(const SimpleEventCollection &newCollection) {
    copy(newCollection.begin(), newCollection.end(), back_inserter(*this));
    return true;
  }

};


// typedef std::vector<SimpleEvent> SimpleEventCollection;


#endif

