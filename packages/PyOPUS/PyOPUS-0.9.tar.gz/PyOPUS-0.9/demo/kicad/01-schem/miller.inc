*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : default used
* Source    : /home/arpadb/pytest/demo/kicad/01-schem/miller.sch
* XML input : /home/arpadb/pytest/demo/kicad/01-schem/miller.xml
* Output    : /home/arpadb/pytest/demo/kicad/01-schem/miller.inc
* Date      : Thu 09 Nov 2017 05:58:57 PM CET
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- miller.sch
*********

.subckt miller inp inn out vdd vss

* Sheet: /
m2 (net004 net002 vss vss) nmosmod w=79.46u l=1.91u m=1 
m1 (net002 net002 vss vss) nmosmod w=20.80u l=0.32u m=1 
m3 (out net002 vss vss) nmosmod w=60.23u l=0.32u m=1 
m6 (net005 net005 vdd vdd) pmosmod w=90.43u l=3.92u m=1 
m7 (net003 net005 vdd vdd) pmosmod w=90.43u l=3.92u m=1 
m8 (out net003 vdd vdd) pmosmod w=83.01u l=0.20u m=2 
i1 (vdd net002)  dc=100u
r1 (out net001) r=67.6k 
c1 (net001 net003) c=13.5p 
m4 (net005 inn net004 vss) nmosmod w=67.29u l=3.97u m=1 
m5 (net003 inp net004 vss) nmosmod w=67.29u l=3.97u m=1 

.ends

