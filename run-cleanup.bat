@echo off
chcp 65001 > nul
echo ================================
echo QClaw Skills 自动清理工具
echo ================================
echo.

set SKILLS_PATH=D:\QClawX\data\.qclaw\skills
set BACKUP_PATH=D:\QClawX\data\.qclaw\skills-backup-%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%
set BACKUP_PATH=%BACKUP_PATH: =0%

echo [1/3] 创建备份目录...
mkdir "%BACKUP_PATH%" 2>nul
echo 备份到: %BACKUP_PATH%
echo.

echo [2/3] 备份并删除不常用的skills...
echo.

REM 备份并删除不核心的skills
for /d %%i in ("%SKILLS_PATH%\*") do (
    set "SKILL_NAME=%%~nxi"
    call :check_skill "%%i" "%%~nxi"
)

echo.
echo [3/3] 清理完成！
echo.
dir "%SKILLS_PATH%" /b /ad | find /c /v ""
echo 个skills保留
echo.
echo 备份位置: %BACKUP_PATH%
echo.
echo 请重启QClaw使配置生效
echo ================================
pause
exit

:check_skill
set "FULL_PATH=%~1"
set "NAME=%~2"

REM 检查是否为核心skill (保留)
if "%NAME%"=="1688-sourcing-agent" exit /b
if "%NAME%"=="1688-product-search" exit /b
if "%NAME%"=="1688-product-analysis" exit /b
if "%NAME%"=="search-1688-supplier" exit /b
if "%NAME%"=="inquiry-1688" exit /b
if "%NAME%"=="tencent-docs" exit /b
if "%NAME%"=="mcporter" exit /b
if "%NAME%"=="ima" exit /b
if "%NAME%"=="pdf" exit /b
if "%NAME%"=="docx" exit /b
if "%NAME%"=="xlsx" exit /b
if "%NAME%"=="pptx" exit /b
if "%NAME%"=="online-search" exit /b
if "%NAME%"=="multi-search-engine" exit /b
if "%NAME%"=="skillhub-install" exit /b
if "%NAME%"=="qclaw-env" exit /b
if "%NAME%"=="email-skill" exit /b
if "%NAME%"=="imap-smtp-email" exit /b
if "%NAME%"=="file-manager" exit /b
if "%NAME%"=="web-fetch" exit /b
if "%NAME%"=="browser" exit /b
if "%NAME%"=="ai-engineer" exit /b
if "%NAME%"=="playwright" exit /b
if "%NAME%"=="mcp-builder" exit /b
if "%NAME%"=="token-optimization" exit /b
if "%NAME%"=="context-compression" exit /b
if "%NAME%"=="memory-system" exit /b
if "%NAME%"=="persona-switch" exit /b
if "%NAME%"=="openclaw-evolution-researcher" exit /b

REM 不是核心skill，执行备份和删除
echo 移除: %NAME%
xcopy "%FULL_PATH%" "%BACKUP_PATH%\%NAME%\" /E /I /H /Y > nul 2>&1
rmdir /s /q "%FULL_PATH%"

exit /b
