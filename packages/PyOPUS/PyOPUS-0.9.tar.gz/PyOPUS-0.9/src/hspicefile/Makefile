CC=gcc
CCOPTS=-fPIC -DLINUX
INCLUDES=-I/usr/include/python3.5
LINKER=ld
LINKOPTS=-shared
LINKLIBS=-lm
LIBNAME=_hspice_read
OBJECTS=hspice_read.o
INSTALLDIR=../../pyopus/simulator

all: library 

library: $(LIBNAME).so

%.o: %.c
	$(CC) $(CCOPTS) $(INCLUDES) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CCOPTS) $(INCLUDES) -c $< -o $@

$(LIBNAME).so: $(OBJECTS)
	$(LINKER) $(LINKOPTS) -o $@ $(OBJECTS) $(LINKLIBS)
	# cp $@ $(INSTALLDIR)
	cp $@ $(INSTALLDIR)/_hspice_read.cpython-35m-x86_64-linux-gnu.so

clean:
	rm -f *.o *.so
