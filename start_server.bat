@echo off
setlocal enabledelayedexpansion
echo ====================================
echo   StaffFAQ API 服务器启动脚本
echo ====================================
echo.
echo [说明] 支持两种方式启动：
echo   1. python app.py sk-你的APIKey  （命令行传入，推荐）
echo   2. 直接运行此脚本（从 .env 读取）
echo.

REM 检查是否传入了 API Key 参数
if "%1"=="" (
    REM 没有传入参数，检查 .env 文件
    if exist ".env" (
        echo [模式] 从 .env 文件读取配置
        echo [提示] 如需传入 API Key，请使用: %0 sk-你的APIKey
        echo.
    ) else (
        echo [模式] 交互式配置
        echo ====================================
        echo   配置 DeepSeek API Key
        echo ====================================
        echo.
        echo [说明] 此配置仅保存在内存中，不会写入文件
        echo [说明] 每次重启服务器需要重新输入
        echo.
        
        set /p DEEPSEEK_KEY=请输入 DeepSeek API Key (sk-开头): 
        
        if "!DEEPSEEK_KEY!"=="" (
            echo [错误] API Key 不能为空！
            pause
            exit /b 1
        )
        
        if "!DEEPSEEK_KEY:~0,3!"=="sk-" (
            echo [✓] API Key 格式正确
        ) else (
            echo [警告] API Key 应该以 sk- 开头，请确认是否正确
            echo.
            set /p CONFIRM=是否继续？(Y/N): 
            if /i not "!CONFIRM!"=="Y" (
                echo [已取消]
                pause
                exit /b 1
            )
        )
        
        REM 设置环境变量（仅在当前会话中有效）
        set LLM_PROVIDER=deepseek
        set LLM_MODEL=deepseek-chat
        set DEEPSEEK_API_KEY=!DEEPSEEK_KEY!
        set TEMPERATURE=0.2
        
        echo.
        echo [✓] 配置完成，正在启动服务器...
        echo.
    )
) else (
    REM 传入了参数，直接使用
    echo [模式] 从命令行参数读取 API Key
    echo [参数] %1
    echo.
)

echo ====================================
echo   启动服务器
echo ====================================
echo.

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "rag_env\Scripts\activate.bat" (
    call rag_env\Scripts\activate.bat
) else (
    echo [错误] 未找到虚拟环境！
    pause
    exit /b 1
)

REM 显示配置信息
echo [配置] LLM Provider: %LLM_PROVIDER%
echo [配置] LLM Model: %LLM_MODEL%
echo [配置] Temperature: %TEMPERATURE%
if defined DEEPSEEK_API_KEY (
    echo [配置] API Key: %DEEPSEEK_API_KEY:~0,10%... (已隐藏)
) else (
    echo [配置] API Key: 从 .env 文件读取
)
echo.
echo [INFO] 正在启动服务器...
echo [INFO] 访问地址: http://localhost:8000
echo [INFO] API 文档: http://localhost:8000/docs
echo.

python app.py %1

pause
