@echo off
echo ========================================
echo   StaffFAQ 安装脚本 (Windows)
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 创建虚拟环境失败
    pause
    exit /b 1
)

echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [3/4] 升级 pip...
python -m pip install --upgrade pip

echo [4/4] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 复制 .env.example 为 .env
echo 2. 在 .env 文件中填入你的 API Key
echo 3. 运行: streamlit run app.py
echo.
pause
