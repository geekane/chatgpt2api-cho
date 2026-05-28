@echo off
REM ChatGPT2API Choreo 快速部署脚本 (Windows)

echo ========================================
echo ChatGPT2API Choreo 快速部署
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [信息] Python 已安装
echo.

REM 检查 Choreo CLI
wdp --version >nul 2>&1
if errorlevel 1 (
    echo [警告] Choreo CLI 未安装
    echo.
    echo 请访问以下链接安装 Choreo CLI:
    echo https://wso2.com/choreo/docs/develop-components/develop-services/develop-a-service/#use-the-choreo-cli
    echo.
    echo 或在 Linux/macOS 上运行:
    echo curl -o- https://raw.githubusercontent.com/wso2/wdp-cli/main/scripts/install.sh ^| bash
    echo.
    pause
    exit /b 1
)

echo [信息] Choreo CLI 已安装
echo.

REM 运行 Python 部署脚本
echo [信息] 开始部署...
echo.
python deploy-to-choreo.py

if errorlevel 1 (
    echo.
    echo [错误] 部署失败
    pause
    exit /b 1
)

echo.
echo [成功] 部署完成！
echo.
pause
