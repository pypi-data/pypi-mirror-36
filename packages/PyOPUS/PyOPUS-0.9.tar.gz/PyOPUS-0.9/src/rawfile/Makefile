CC=gcc
CCOPTS=-fPIC -DLINUX
INCLUDES=-I/usr/include/python3.4
LINKER=ld
LINKOPTS=-shared
LINKLIBS=
LIBNAME=_rawfile
OBJECTS=rawfile.o
INSTALLDIR=../../pyopus/simulator

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
