@echo off
rem �ߑO00��00���`�ߌ�23��59���̂݋N���\
set start=0000
set end=2359
set now=%time: =0%
set nowstr=%now:~0,2%%now:~3,2%
echo Teams�p���|�[�e�B���O�c�[���͌ߑO00��00���`�ߌ�23��59���̂݋N���\�ł��B
echo ���݂̎������N���\���ԓ������肵�܂��B
echo ���݂̎���
echo %nowstr%

if 1%nowstr% LSS 1%start% goto err
if 1%end% LSS 1%nowstr% goto err

echo ���̎��Ԃ͓���\���Ԃł��B
echo ���s���܂��B
cd C:\python-path\
python.exe ..\tools\TeamsReporting.py
goto end

:err
echo ���쎞�ԊO�ł�
:end
