    @ECHO OFF
    SET PROG=
    if NOT %2A == A                        GOTO USAGE
    if %1A == A                            GOTO DEFULT
    if %1  == cynpy.csp OR %1  == rapy.csp GOTO START
    if %1  == cynpy.isp OR %1  == rapy.isp GOTO START
    GOTO USAGE

:DEFULT
    SET PROG=cynpy.csp

:START
   SET PROG=-m%PROG%%1

rem prepare the bin file for temporary
rem ===============================================================================
rem python -B c:\Python27\Scripts\hex2bin.py ..\fw\cy2311r3\Objects\cy2311r3_x004.hex temp.bin
    python -B c:\Python27\Scripts\hex2bin.py z:\RD\Project\CAN1112\Ray\fw\cy2332r0_20180907_019.hex temp.bin


rem stop MCU
rem ===============================================================================
    python %PROG% stop


rem ES may be not fully trimmed but OSC. Complete the row of CP trim
rem ===============================================================================
rem python %PROG% prog_hex 1 940    ff 00 0a 00 00 ff
rem python %PROG% prog_hex 1 944 ff 4d 00 0a 00 00
    python %PROG% set_trim

rem python %PROG% prog_hex 1 94a    0f 02 f2 5a 0f ff

rem upload FW
rem ===============================================================================
    python %PROG% upload temp.bin 1
rem python %PROG% upload ..\fw\cy2311r3\Objects\cy2311r3_20180606.2.memh 1
rem python %PROG% upload ..\fw\scp\phy20180605a_prl0605\scp\Objects\scp_20180613.2.memh 1


rem compare
rem ===============================================================================
    python %PROG%   comp temp.bin ^
                        900=CAN1112A-000 ^
                        910=AP4377-14L ^
                        33=\90 34=\09 35=\40 36=\E4 37=\93 38=\F5 39=\A2 3A=\80 3B=\FE ^
                        940=\00 941=\FF 942=\FF 943=\FF 944=\FF


rem FT information
rem writer information
rem option table
rem PDO table
rem mapping table
rem ===============================================================================
rem python %PROG% prog_asc 1 910 CAN1112A28L_BIN1
    python %PROG% prog_str 1 930 PY187_%DATE:~2,2%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
    python %PROG% prog_hex 1 960 02 08 00 00
rem python %PROG% prog_hex 1 960 06 08 08 00
rem python %PROG% prog_hex 1 960 06 2B 08 00

rem 2-PDO (5V/3A, 3.3-5.9V/3A, 15W/17.7W)
rem python %PROG%   prog_hex 1 970 2C 91 01 0A  3C 21 76 C0

rem 3-PDO (5V/3A, 9V/3A, 3.3-11V/3A, 27/33W)
rem python %PROG% prog_hex 1 970 2C 91 01 0A  2C D1 02 00  3C 21 DC C0
rem python %PROG% prog_hex 1 a20    10 FA        51 C2     01 EE  13 E8  C1 F4  11 F4  B2 E4
rem python %PROG% prog_hex 1 a20    10 FA        51 C2     01 EE  13 E8  C1 F4  21 F4  12 E4

rem 4-PDO (5V/3A, 9V/2A, 3.3-5.9V/3A, 3.3-11V/2A, 18W/22W)
rem python %PROG% prog_hex 1 970 2C 91 01 0A  C8 D0 02 00  3C 21 76 C0  28 21 DC C0
rem python %PROG% prog_hex 1 A20    10 FA        51 C2     01 EE        13 E8  C1 F4  11 F4  22 E4
rem python %PROG% prog_hex 1 A20    10 FA        51 C2     01 EE        13 E8  C1 F4  11 F4  62 E4

rem 6-PDO (5V/3A, 6V/3A, 7V/3A, 8V/2.75A, 9V/2.44A, 10V/2.2A, 22W)
rem python %PROG% prog_hex 1 970 2C 91 01 0A  2C E1 01 00  2C 31 02 00  13 81 02 00  F4 D0 02 00  DC 20 03 00
rem python %PROG% prog_hex 1 A20    10 FA        51 2C        01 5E        11 90        C1 C2        11 F4  62 E4


rem 3-PDO (5V/3A, 9V/2A, 3.3-21V/2A, ??W)
    python %PROG%   prog_hex 1 970 2C 91 01 0A  C8 D0 02 00  28 21 A4 C1
rem python %PROG% 1 prog_hex 1 98C 2C 91 01 0A  C8 D0 02 00  28 21 A4 C1

rem 3+PDO (3V/3A, 5V/3A, 9V/3A, 3.3-11V/3A, 33W)
rem python %PROG% 1 prog_hex 1 98C 2C F1 00 0A  2C 91 01 00  2C D1 02 00  3C 21 DC C0
rem python %PROG% 1 prog_hex 1 A2E    10 96        50 FA        01 C2     13 E8  C1 F4  21 F4  12 E4


rem fine-tune table
rem ===============================================================================
rem python %PROG% prog_hex 1 a58 FF FF
rem python %PROG% prog_hex 1 a58 80 20
    python %PROG% prog_hex 1 a58 80 60


rem reset MCU
rem ===============================================================================
rem python %PROG% wrx F7 01 01 01
rem python %PROG% reset

    del temp.bin

GOTO EXIT

:USAGE
echo NOTE:
echo 1. power-on the I2C-to-CC bridge
echo 2. try the bridge
echo 3. try the target (DUT)
echo ===============================================================================
echo python -mcynpy.aardv sw
echo python -mcynpy.isp   rev
echo python -mcynpy.isp   dump
echo python -mcynpy.csp   query
echo python -mcynpy.csp   rev
echo python -mcynpy.csp   dump
echo python -mcynpy.csp 1 dump b0 30
echo python -mcynpy.csp   stop
echo python -mcynpy.csp   nvm
echo python -mcynpy.csp   dnload otp.bin

:EXIT
