*** Simple amplifier ***

vcc 1 0 dc {vcc}
i1 2 0 dc 0

r1 1 3 r={r1}
r2 2 3 r={r2}

q1 3 2 0 2n3510

.model 2n3510 npn
+ bf=100 br=1.35e-4 xtb=1.5 is=8.35e-14 eg=1.11 cjc=9.63e-12
+ cje=9.47e-12 rb=16.7 rc=1.66 vaf=90 tf=1e-10 tr=1.27e-4
+ cjs=1e-15 vjs=0.8 mjs=0.5 var=100 ise=4.77e-11 isc=1e-16
+ ikf=0.18 ikr=1000 irb=1 rbm=0 vtf=1000
