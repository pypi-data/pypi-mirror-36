* Test topology - dc, ac, and tran with feedback
* HSPICE

x1 inp inn out vdd 0 bias 0 vdd amp
vdd vdd 0 dc=vdd
ibias vdd bias dc=ibias
rfb out1 inn r=rfb
efb out1 0 out 0 1
rin in inn r=rin
vcom inp 0 dc='vdd/2'
vin in inp dc=0 ac=1 pulse lev1 lev2 tstart tr tf pw
rload out 0 rload
cload out 0 cload
