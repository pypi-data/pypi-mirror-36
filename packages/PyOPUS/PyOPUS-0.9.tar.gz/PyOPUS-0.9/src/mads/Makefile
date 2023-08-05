CC=gcc
CPP=g++
INCLUDES=-I/usr/include/python3.4 
CCOPTS=-fPIC -DLINUX -O3 
LINKER=g++
LINKOPTS=-shared
LINKLIBS=styrene/sty.a -lc -lm 
LIBNAME=_mads
OBJECTS=mads.o mdo.o
INSTALLDIR=../../pyopus/problems

all: library 

library: $(LIBNAME).so

%.o: %.c
	$(CC) $(CCOPTS) $(INCLUDES) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CCOPTS) $(INCLUDES) -c $< -o $@

styrene/sty.a:
	cd styrene && $(MAKE)

$(LIBNAME).so: $(OBJECTS) styrene/sty.a
	$(LINKER) $(LINKOPTS) -o $@ $(OBJECTS) $(LINKLIBS)
	cp $@ $(INSTALLDIR)

clean:
	cd styrene && $(MAKE) clean
	rm -f *.o *.so
	