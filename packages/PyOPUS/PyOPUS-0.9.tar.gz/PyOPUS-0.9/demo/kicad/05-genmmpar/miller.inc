*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : /home/arpadb/pytest/demo/kicad/05-genmmpar/netlister.json
* Source    : /home/arpadb/pytest/demo/kicad/05-genmmpar/miller.sch
* XML input : /home/arpadb/pytest/demo/kicad/05-genmmpar/cmos180n.xml
* Output    : /home/arpadb/pytest/demo/kicad/05-genmmpar/miller.inc
* Date      : Thu 09 Nov 2017 06:13:04 PM CET
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- miller.sch
*********

.subckt miller inp inn out vdd vss

* Sheet: /
xm2 (net003 net002 vss vss) nmosmod param: w=79.46u l=1.91u m=1 vtmm={m2vt} u0mm={m2u0} 
xm1 (net002 net002 vss vss) nmosmod param: w=20.80u l=0.32u m=1 vtmm={m1vt} u0mm={m1u0} 
xm3 (out net002 vss vss) nmosmod param: w=60.23u l=0.32u m=1 vtmm={m3vt} u0mm={m3u0} 
xm6 (net004 net004 vdd vdd) pmosmod param: w=90.43u l=3.92u m=1 vtmm={m6vt} u0mm={m6u0} 
xm7 (net001 net004 vdd vdd) pmosmod param: w=90.43u l=3.92u m=1 vtmm={m7vt} u0mm={m7u0} 
xm8 (out net001 vdd vdd) pmosmod param: w=83.01u l=0.20u m=2 vtmm={m8vt} u0mm={m8u0} 
i1 (vdd net002)  dc=100u
r1 (out net005) r=67.6k 
c1 (net005 net001) c=13.5p 
xm4 (net004 inn net003 vss) nmosmod param: w=67.29u l=3.97u m=1 vtmm={m4vt} u0mm={m4u0} 
xm5 (net001 inp net003 vss) nmosmod param: w=67.29u l=3.97u m=1 vtmm={m5vt} u0mm={m5u0} 

.ends

