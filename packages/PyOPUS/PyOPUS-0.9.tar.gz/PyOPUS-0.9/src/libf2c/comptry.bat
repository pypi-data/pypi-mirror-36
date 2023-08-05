rem Fixed a problem caused of more than 9 parameters passed to cl
rem A. Buermen
rem %1 %2 %3 %4 %5 %6 %7 %8 %9
%*
if errorlevel 1 goto nolonglong
exit 0
:nolonglong
rem %1 -DNO_LONG_LONG %2 %3 %4 %5 %6 %7 %8 %9
set cmdx=%1
shift
%cmdx% -DNO_LONG_LONG %*
