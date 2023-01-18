@echo off
REG ADD HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x1 /f
pause