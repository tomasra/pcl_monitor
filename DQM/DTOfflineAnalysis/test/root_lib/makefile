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


# CXX		= /usr/local/gcc-alt-2.95.2/bin/c++
CXX		= /usr/bin/c++
#CXX		= /usr/local/gcc-alt-3.2/bin/c++
CXXFLAGS      = -O -Wall -fPIC $(ROOTCFLAGS)
LD	 	= /usr/bin/c++
#LD	 	= /usr/local/gcc-alt-3.2/bin/c++\
LDFLAGS       = 
SONAME	      = libEvent.so
SOFLAGS       = -shared -Wl,-soname,$(SONAME)
LIBS          = $(ROOTLIBS) -lm -ldl -rdynamic
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
		$(LD) -rdynamic $(OBJS) $(SOFLAGS) -o $(SONAME)

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

#---------------------------------------------------
# DO NOT DELETE

DTCut.o: DTCut.h DTSegmentObject.h ../../src/DTSegmentObject.h DTHitObject.h
DTCut.o: ../../src/DTHitObject.h
DTDetId.o: DTDetId.h
DTHistoPlotter.o: DTHistoPlotter.h DTDetId.h /usr/include/stdio.h
DTHistoPlotter.o: /usr/include/features.h /usr/include/sys/cdefs.h
DTHistoPlotter.o: /usr/include/gnu/stubs.h
DTHistoPlotter.o: /usr/lib/gcc/i386-redhat-linux/3.4.6/include/stddef.h
DTHistoPlotter.o: /usr/include/bits/types.h /usr/include/bits/wordsize.h
DTHistoPlotter.o: /usr/include/bits/typesizes.h /usr/include/libio.h
DTHistoPlotter.o: /usr/include/_G_config.h /usr/include/wchar.h
DTHistoPlotter.o: /usr/include/bits/wchar.h /usr/include/gconv.h
DTHistoPlotter.o: /usr/lib/gcc/i386-redhat-linux/3.4.6/include/stdarg.h
DTHistoPlotter.o: /usr/include/bits/stdio_lim.h
DTHistoPlotter.o: /usr/include/bits/sys_errlist.h Histograms.h Utils.h
DTHitObject.o: ../../src/DTHitObject.cc DTHitObject.h ../../src/DTHitObject.h
DTSegmentObject.o: ../../src/DTSegmentObject.cc DTSegmentObject.h
DTSegmentObject.o: ../../src/DTSegmentObject.h DTHitObject.h
DTSegmentObject.o: ../../src/DTHitObject.h
mydict.o: mydict.h /usr/lib/gcc/i386-redhat-linux/3.4.6/include/stddef.h
mydict.o: /usr/include/stdio.h /usr/include/features.h
mydict.o: /usr/include/sys/cdefs.h /usr/include/gnu/stubs.h
mydict.o: /usr/include/bits/types.h /usr/include/bits/wordsize.h
mydict.o: /usr/include/bits/typesizes.h /usr/include/libio.h
mydict.o: /usr/include/_G_config.h /usr/include/wchar.h
mydict.o: /usr/include/bits/wchar.h /usr/include/gconv.h
mydict.o: /usr/lib/gcc/i386-redhat-linux/3.4.6/include/stdarg.h
mydict.o: /usr/include/bits/stdio_lim.h /usr/include/bits/sys_errlist.h
mydict.o: /usr/include/stdlib.h /usr/include/math.h
mydict.o: /usr/include/bits/huge_val.h /usr/include/bits/mathdef.h
mydict.o: /usr/include/bits/mathcalls.h /usr/include/string.h DTCut.h
mydict.o: DTDetId.h DTHistoPlotter.h DTHitObject.h ../../src/DTHitObject.h
mydict.o: DTSegmentObject.h ../../src/DTSegmentObject.h Histograms.h
mydict.o: TTreeReader.h Utils.h
TTreeReader.o: TTreeReader.h DTCut.h DTDetId.h DTSegmentObject.h
TTreeReader.o: ../../src/DTSegmentObject.h DTHitObject.h
TTreeReader.o: ../../src/DTHitObject.h Histograms.h Utils.h
Utils.o: Utils.h DTDetId.h
