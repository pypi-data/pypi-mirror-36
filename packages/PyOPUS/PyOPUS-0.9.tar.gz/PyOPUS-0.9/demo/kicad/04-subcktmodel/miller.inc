*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : /home/arpadb/pytest/demo/kicad/04-subcktmodel/netlister.json
* Source    : /home/arpadb/pytest/demo/kicad/04-subcktmodel/miller.sch
* XML input : /home/arpadb/pytest/demo/kicad/04-subcktmodel/miller.xml
* Output    : /home/arpadb/pytest/demo/kicad/04-subcktmodel/miller.inc
* Date      : Thu 09 Nov 2017 06:12:27 PM CET
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- miller.sch
*********

.subckt miller inp inn out vdd vss

* Sheet: /
xm2 (net001 net004 vss vss) nmosmod param: w=79.46u l=1.91u m=1 
xm1 (net004 net004 vss vss) nmosmod param: w=20.80u l=0.32u m=1 
xm3 (out net004 vss vss) nmosmod param: w=60.23u l=0.32u m=1 
xm6 (net002 net002 vdd vdd) pmosmod param: w=90.43u l=3.92u m=1 
xm7 (net003 net002 vdd vdd) pmosmod param: w=90.43u l=3.92u m=1 
xm8 (out net003 vdd vdd) pmosmod param: w=83.01u l=0.20u m=2 
i1 (vdd net004)  dc=100u
r1 (out net005) r=67.6k 
c1 (net005 net003) c=13.5p 
xm4 (net002 inn net001 vss) nmosmod param: w=67.29u l=3.97u m=1 
xm5 (net003 inp net001 vss) nmosmod param: w=67.29u l=3.97u m=1 

.ends

