@echo off
rem �ߑO04��55���`�ߑO22��05���̂݋N���\
set start=0455
set end=2205
set now=%time: =0%
set nowstr=%now:~0,2%%now:~3,2%
echo ���[���p���|�[�e�B���O�c�[���͌ߑO04��55���`�ߑO22��05���̂݋N���\�ł��B
echo ���݂̎������N���\���ԓ������肵�܂��B
echo ���݂̎���
echo %nowstr%

if 1%nowstr% LSS 1%start% goto err
if 1%end% LSS 1%nowstr% goto err

echo ���̎��Ԃ͓���\���Ԃł��B
echo ���s���܂��B
cd C:\python-path
python.exe ..\tools\MailReporting.py
goto end

:err
echo ���쎞�ԊO�ł�
:end
