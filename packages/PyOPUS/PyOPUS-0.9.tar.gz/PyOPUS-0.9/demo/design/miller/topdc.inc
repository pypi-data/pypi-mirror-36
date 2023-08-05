*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : /mnt/data/Data/pytest/demo/design/miller/netlister.json
* Source    : /mnt/data/Data/pytest/demo/design/miller/topdc.sch
* XML input : /mnt/data/Data/pytest/demo/design/miller/topdc.xml
* Output    : /mnt/data/Data/pytest/demo/design/miller/topdc.inc
* Date      : Fri 24 Aug 2018 10:18:43 AM CEST
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- topdc.sch
*********


* Sheet: /
x1 (inp inn net001 vdd vss) miller   
vdd1 (vdd 0)  dc={vdd/2}
r2 (out inn) r={rfb} 
r1 (inn in) r={rin} 
vcom1 (inp 0)  dc=0
vin1 (in inp)  dc=0 ac=1 pulse=({lev1} {lev2} {tstart} {tr} {tf} {pw})
cl1 (net001 0) c={cload} 
e1 (out 0 net001 0) gain=1 
rl1 (net001 0) r={rload} 
vss1 (vss 0)  dc={-vdd/2}

