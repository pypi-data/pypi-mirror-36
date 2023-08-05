SUBDIRS=cec13 ghalton hspicefile karmitsa lvns lvu mads mwbm rawfile sobol

all:
	@for dir in $(SUBDIRS); do (cd $$dir; $(MAKE) ); done
	
clean:
	@for dir in $(SUBDIRS); do (cd $$dir; $(MAKE) clean ); done
	