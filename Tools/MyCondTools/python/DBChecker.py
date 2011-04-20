#!/usr/bin/env python
import os, sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)
import pluginCondDBPyInterface as condDB

class DBChecker(object):
    def __init__(self, dbName, authPath = "."):
        self.dbName = dbName
        self.authPath = authPath
        self.a = condDB.FWIncantation()
        self.initDB()

    def initDB(self, authPath = None, dbName = None):
        if(authPath == None):
            authPath = self.authPath
        else:
            self.authPath = authPath
        if(dbName == None):
            dbName = self.dbName
        else:
            self.dbName = dbName
        try:
            self.rdbms = condDB.RDBMS(self.authPath)
            self.db = self.rdbms.getDB(self.dbName)
        except:
            raise TypeError("Cannot connect to \""+self.dbName+"\" for RDBMS in \""+self.authPath+"\"")
    
    def getAllTags(self):
        try:
            return self.db.allTags().strip().split()
        except:
            raise TypeError("Cannot retrieve tags from \""+self.dbName+"\" for RDBMS in \""+self.authPath+"\"")

    def checkTag(self, tag):
        try:
            tags = self.getAllTags()
            index = next((i for i in xrange(len(tags)) if tags[i] == tag), None)
            if index == None:
                return False
            else:
                return True
        except TypeError:
            return False
        ##alternative 1:
        #try:
            #return reduce(lambda x,y: x | y, map(lambda x: x == tag, self.getAllTags()))
        #except TypeError:
            #return False
        ##alternative 2:
        #try:
            #return [True for x in self.getAllTags() if x==tag][0]
        #except IndexError:
            #return False
        #alternative 3:
        #try:
            #check = tag in self.getAllTags()
            #return check
        #except TypeError:
            #return False
    
    def iovSequence(self, tag):
        try:
            return self.db.iov(tag)
        except:
            raise

    def payloadContainer(self, tag):
        try:
            iov = self.iovSequence(tag)
            return iov.payloadContainerName()
        except:
            #should we raise ValueError?
            return None
    
    def firstSince(self, tag):
        try:
            iov = self.iovSequence(tag)
            iov.head(1)
            for elem in iov.elements:
                firstSince = elem.since()
            return firstSince
        except:
            raise ValueError("Cannot retrieve first since for tag \"" + tag + "\" in \"" +self.dbName+"\" for RDBMS in \""+self.authPath+"\"")
    
    def lastSince(self, tag):
        try:
            iov = self.iovSequence(tag)
            iov.tail(1)
            for elem in iov.elements:
                lastSince = elem.since()
            return lastSince
        except:
            raise ValueError("Cannot retrieve last since for tag \"" + tag + "\" in \"" +self.dbName+"\" for RDBMS in \""+self.authPath+"\"")

if __name__ == "__main__":
    d = DBChecker("oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO", "/afs/cern.ch/cms/DB/conddb")
    print d.authPath, d.dbName
    li = d.getAllTags()
    print li
    print d.checkTag("runinfo_start_31X_hlt")
    print d.checkTag("runinfo_start_31X_dummy")
    cont = d.payloadContainer("runinfo_start_31X_hlt")
    print cont
    cont = d.payloadContainer("runinfo_start_31X_dummy")
    print cont
    first = d.firstSince("runinfo_start_31X_hlt")
    last = d.lastSince("runinfo_start_31X_hlt")
    print first, last
    #now failing on a dummy sqlite
    d = DBChecker("sqlite_file:/tmp/dummy.db", ".")
    print d.authPath, d.dbName
    try:
        li = d.getAllTags()
        print li
    except TypeError, e:
        print "KNOWN ERROR", str(e)
    except:
        print "UNKNOWN ERROR"
    try:
        print d.checkTag("test")
    except:
        print "UNKNOWN ERROR"
    try:
        print d.payloadContainer("test")
    except:
        print "UNKNOWN ERROR"
    try:
        first = d.firstSince("test")
    except ValueError, e:
        print "KNOWN ERROR", str(e)
    except:
        print "UNKNOWN ERROR"
    try:
        last = d.lastSince("test")
    except ValueError, e:
        print "KNOWN ERROR", str(e)
    except:
        print "UNKNOWN ERROR"
