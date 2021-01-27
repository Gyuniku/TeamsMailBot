@echo off
rem 午前04時55分～午前22時05分のみ起動可能
set start=0455
set end=2205
set now=%time: =0%
set nowstr=%now:~0,2%%now:~3,2%
echo メール用レポーティングツールは午前04時55分～午前22時05分のみ起動可能です。
echo 現在の時刻が起動可能時間内か判定します。
echo 現在の時刻
echo %nowstr%

if 1%nowstr% LSS 1%start% goto err
if 1%end% LSS 1%nowstr% goto err

echo この時間は動作可能時間です。
echo 実行します。
cd C:\python-path
python.exe ..\tools\MailReporting.py
goto end

:err
echo 動作時間外です
:end
