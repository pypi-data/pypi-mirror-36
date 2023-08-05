CC=gcc
INCLUDES=-I/usr/include/python3.4 
CCOPTS=-fPIC -DLINUX $(INCLUDES) -g
LINKER=gcc
LINKOPTS=-shared
LINKLIBS=-lm
LIBNAME=_sobol
OBJECTS=sobol.o
INSTALLDIR=../../pyopus/misc

all: library 

library: $(LIBNAME).so

%.o: %.c
	$(CC) $(CCOPTS) $(INCLUDES) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CCOPTS) $(INCLUDES) -c $< -o $@

$(LIBNAME).so: $(OBJECTS)
	$(LINKER) $(LINKOPTS) -o $@ $(OBJECTS) $(LINKLIBS)
	cp $@ $(INSTALLDIR)

clean:
	rm -f *.o *.so
