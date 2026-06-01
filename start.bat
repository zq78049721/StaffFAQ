@echo off
echo ========================================
echo   StaffFAQ 安全启动脚本
echo ========================================
echo.

REM 检查 .env 文件是否存在
if not exist ".env" (
    echo [提示] 未找到 .env 文件，将使用环境变量
    echo.
    echo 请设置以下环境变量：
    echo   - DEEPSEEK_API_KEY (DeepSeek API Key)
    echo   - LLM_PROVIDER (deepseek/ollama/zhipu)
    echo   - LLM_MODEL (模型名称)
    echo.
    echo 或者创建 .env 文件并填入配置
    echo.
    pause
)

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "rag_env\Scripts\activate.bat" (
    call rag_env\Scripts\activate.bat
) else (
    echo [错误] 未找到虚拟环境，请先运行 setup.bat
    pause
    exit /b 1
)

echo [启动] 正在启动 StaffFAQ...
echo [提示] 按 Ctrl+C 停止服务
echo.

streamlit run app.py
