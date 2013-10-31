# Makefile for rroot
# The MIX Group

# NOTE: this is now fully automatic. You are not supposed to modify it,
# providing that you use the usual file naming rules.


ObjSuf        = o
SrcSuf        = cxx
ExeSuf        =
DllSuf        = so
EVENTLIB      = $(EVENTO)
OutPutOpt     = -o

ROOTCFLAGS    = $(shell root-config --cflags) 
ROOTLIBS      = $(shell root-config --libs)
ROOTGLIBS     = $(shell root-config --glibs)

ROOFITINCL    =  -I $(shell scram tool info roofitcore | grep "INCLUDE=" | sed s/"INCLUDE="//)
ROOFITLIBS    =  -L $(shell scram tool info roofitcore | grep "LIBDIR=" | sed s/"LIBDIR="//) -l RooFit -l RooFitCore


CXX		= $(shell scram tool info gcc-cxxcompiler | grep "CXX=" | sed s/"CXX="//)

CXXFLAGS      = -O -Wall -fPIC $(ROOTCFLAGS) $(ROOFITINCL)
LD	 	= $(CXX)
LDFLAGS       = 
SONAME	      = libEvent.so
SOFLAGS       = $(shell root-config --ldflags --libs) -shared -Wl,-soname,$(SONAME)
LIBS          = $(ROOTLIBS) $(ROOFITLIBS) -lm -ldl -rdynamic
GLIBS         = $(ROOTGLIBS) -L/usr/X11R6/lib \
                -lXpm -lX11 -lm -ldl -rdynamic

HDRS          = $(patsubst mydict.h,,$(wildcard *.h))

SRCS          = $(patsubst mydict.cc,,$(wildcard *.cc) $(wildcard *.C)) 

OBJ_TMP       = $(patsubst main.o,,$(SRCS:.cc=.o)  mydict.o)
OBJS	      = $(OBJ_TMP:.C=.o)

ICCS          = $(wildcard *.icc)

PROGRAM       = rroot

#all:            $(PROGRAM)
all:		$(SONAME)

$(PROGRAM):     $(OBJS) main.o
	          @echo "Linking $(PROGRAM):"
		$(LD) $(LDFLAGS) $(OBJS) main.o $(GLIBS) -o $(PROGRAM)

$(SONAME):	$(OBJS)
		@echo "Linking $(SONAME):"
		$(LD) $(LIBS) $(OBJS) $(SOFLAGS) -o $(SONAME) 

#-L/afs/cern.ch/cms/slc5_ia32_gcc434/lcg/root/5.22.00d-cms16/lib  -lPhysics /afs/cern.ch/cms/slc5_ia32_gcc434/lcg/roofit/5.26.00-cms3/lib/libRooFit.so /afs/cern.ch/cms/slc5_ia32_gcc434/lcg/roofit/5.26.00-cms3/lib/libRooFitCore.so

clean:          cleandict
		rm -f $(OBJS) main.o core

cleandict:	
		rm -f mydict.*

test:
		@echo   "LinkDef file: $(LINKDEF)"
		@echo   "Header files: $(HDRS)"
		@echo   "Source files: $(SRCS)"
		@echo 	"Object files: $(OBJS)"


# Generic dependencies (add dependency on .h)
%.o : %.cc %.h
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) $< -o $@

%.o : %.C %.h
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) $< -o $@


LINKDEF		= $(wildcard *LinkDef.h)
#Put the LinkDef.h at the end of the list.
DICTHDRS        = $(patsubst $(LINKDEF),,$(HDRS)) $(LINKDEF)

mydict.cc: $(DICTHDRS)
	    @echo "Generating dictionary ..."
	    rootcint -f mydict.cc -c -p -I${ROOTSYS}/include $(DICTHDRS)  

