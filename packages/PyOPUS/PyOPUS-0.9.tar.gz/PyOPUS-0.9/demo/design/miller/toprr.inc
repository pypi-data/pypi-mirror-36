*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : /mnt/data/Data/pytest/demo/design/miller/netlister.json
* Source    : /mnt/data/Data/pytest/demo/design/miller/toprr.sch
* XML input : /mnt/data/Data/pytest/demo/design/miller/toprr.xml
* Output    : /mnt/data/Data/pytest/demo/design/miller/toprr.inc
* Date      : Fri 24 Aug 2018 01:54:04 PM CEST
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- toprr.sch
*********


* Sheet: /
x1 (inp inn net001 vdd vss) miller   
vdd1 (vdd 0)  dc={vdd/2} ac={acvdd}
r2 (out inn) r={rfb} 
vcom1 (com 0)  dc=0 ac={accom}
vdif1 (inp com)  dc=0 ac=0
cl1 (net001 0) c={cload} 
e1 (out 0 net001 0) gain=1 
rl1 (net001 0) r={rload} 
vss1 (vss 0)  dc={-vdd/2} ac={acvss}
cin1 (inn com) c={cin} 

