CC=gcc
INCLUDES=-I/usr/include/python3.4 -I../libf2c
CCOPTS=-fPIC -DLINUX -g
LINKER=gcc
LINKOPTS=-shared
LINKLIBS=-lm
LIBNAME=_cec13
OBJECTS=test_func.o cec13.o 
INSTALLDIR=../../pyopus/problems

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
