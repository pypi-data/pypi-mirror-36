*********
* SPICE OPUS netlister for KiCad
* (c)2017 EDA Lab FE Uni-Lj
*
* Netlister : KiCad -> Spice Opus
* Config    : /mnt/data/Data/pytest/demo/design/miller/netlister.json
* Source    : /mnt/data/Data/pytest/demo/design/miller/miller.sch
* XML input : /mnt/data/Data/pytest/demo/design/miller/miller.xml
* Output    : /mnt/data/Data/pytest/demo/design/miller/miller.inc
* Date      : Thu 23 Aug 2018 11:57:27 AM CEST
* Tool      : Eeschema 4.0.5+dfsg1-4
* Sheet 1   : / -- miller.sch
*********

.include mosmm.inc

.subckt miller inp inn out vdd vss

* Sheet: /
xmn4 (net001 net003 vss vss) submodn param: w={mirr_wd} l={mirr_ld} m=1 vtmm={mn4vt} u0mm={mn4u0} 
xmn3 (net003 net003 vss vss) submodn param: w={mirr_w} l={mirr_l} m=1 vtmm={mn3vt} u0mm={mn3u0} 
xmn5 (out net003 vss vss) submodn param: w={mirr_wo} l={mirr_l} m=1 vtmm={mn5vt} u0mm={mn5u0} 
xmp1 (net005 net005 vdd vdd) submodp param: w={load_w} l={load_l} m=1 vtmm={mp1vt} u0mm={mp1u0} 
xmp2 (net002 net005 vdd vdd) submodp param: w={load_w} l={load_l} m=1 vtmm={mp2vt} u0mm={mp2u0} 
xmp3 (out net002 vdd vdd) submodp param: w={out_w} l={out_l} m=2 vtmm={mp3vt} u0mm={mp3u0} 
i1 (vdd net003)  dc={ibias}
r1 (out net004) r={r_out} 
c1 (net004 net002) c={c_out} 
xmn1 (net005 inn net001 vss) submodn param: w={diff_w} l={diff_l} m=1 vtmm={mn1vt} u0mm={mn1u0} 
xmn2 (net002 inp net001 vss) submodn param: w={diff_w} l={diff_l} m=1 vtmm={mn2vt} u0mm={mn2u0} 

.ends

