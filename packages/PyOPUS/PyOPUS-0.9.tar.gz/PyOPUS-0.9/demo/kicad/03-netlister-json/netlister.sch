EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:pyopus
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L OUTPUT_FILE A1
U 1 1 59E3511E
P 4350 2450
F 0 "A1" H 3950 2500 50  0000 L CNN
F 1 "OUTPUT_FILE" H 4350 2350 50  0000 C CNN
F 2 "" H 4350 2450 60  0001 C CNN
F 3 "" H 4350 2450 60  0001 C CNN
F 4 "netlister.cir" H 3950 2200 50  0000 L CNN "Name"
	1    4350 2450
	1    0    0    -1  
$EndComp
$Comp
L Q_NPN_BEC Q4
U 1 1 59E35B39
P 4600 3400
F 0 "Q4" H 4800 3450 50  0000 L CNN
F 1 "T2N2222" H 4800 3350 50  0000 L CNN
F 2 "" H 4800 3500 50  0000 C CNN
F 3 "" H 4600 3400 50  0000 C CNN
F 4 "4" H 4600 3400 60  0001 C CNN "m"
F 5 "8" H 4600 3400 60  0001 C CNN "area"
	1    4600 3400
	1    0    0    -1  
$EndComp
$Comp
L VSRC Vbe4
U 1 1 59E35B40
P 4100 3550
F 0 "Vbe4" V 3950 3550 50  0000 C CNN
F 1 "VSRC" V 3850 3550 50  0001 C CNN
F 2 "" V 3830 2800 50  0000 C CNN
F 3 "" V 3900 2800 50  0000 C CNN
F 4 "dc=0" V 4250 3550 50  0000 C CNN "Specification"
	1    4100 3550
	1    0    0    -1  
$EndComp
$Comp
L VSRC Vce4
U 1 1 59E35B47
P 5550 3350
F 0 "Vce4" V 5400 3350 50  0000 C CNN
F 1 "VSRC" V 5300 3350 50  0001 C CNN
F 2 "" V 5280 2600 50  0000 C CNN
F 3 "" V 5350 2600 50  0000 C CNN
F 4 "dc=0" V 5700 3350 50  0000 C CNN "Specification"
	1    5550 3350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59E35B4D
P 4100 3700
F 0 "#PWR?" H 4100 3450 50  0001 C CNN
F 1 "GND" H 4100 3550 50  0000 C CNN
F 2 "" H 4100 3700 50  0000 C CNN
F 3 "" H 4100 3700 50  0000 C CNN
	1    4100 3700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59E35B53
P 5550 3500
F 0 "#PWR?" H 5550 3250 50  0001 C CNN
F 1 "GND" H 5550 3350 50  0000 C CNN
F 2 "" H 5550 3500 50  0000 C CNN
F 3 "" H 5550 3500 50  0000 C CNN
	1    5550 3500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59E35B59
P 4700 3600
F 0 "#PWR?" H 4700 3350 50  0001 C CNN
F 1 "GND" H 4700 3450 50  0000 C CNN
F 2 "" H 4700 3600 50  0000 C CNN
F 3 "" H 4700 3600 50  0000 C CNN
	1    4700 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 3400 4400 3400
Wire Wire Line
	4700 3200 5550 3200
Text GLabel 4100 3300 1    60   Input ~ 0
b4
Text GLabel 4700 3100 1    60   Input ~ 0
c4
Wire Wire Line
	4700 3100 4700 3200
Wire Wire Line
	4100 3300 4100 3400
$EndSCHEMATC
