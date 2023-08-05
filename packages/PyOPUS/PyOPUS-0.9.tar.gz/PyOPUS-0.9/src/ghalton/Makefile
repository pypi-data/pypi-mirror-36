CC=gcc
INCLUDES=-I/usr/include/python3.4
CCOPTS=-fPIC -DLINUX 
LINKER=gcc
LINKOPTS=-shared
LINKLIBS=-lm -lstdc++
LIBNAME=_ghalton
OBJECTS=Halton.o Halton_wrap.o
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
