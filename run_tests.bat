@echo off
setlocal enabledelayedexpansion

echo ====================================
echo   StaffFAQ 自动化测试
echo ====================================
echo.

REM 检查是否传入了 API Key 参数
if "%1"=="" (
    echo [错误] 请传入 DeepSeek API Key
    echo.
    echo 用法：run_tests.bat sk-你的APIKey [类别]
    echo 示例：run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300
    echo       run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300 annual_leave
    echo.
    pause
    exit /b 1
)

echo [配置] API Key: %1...
if not "%2"=="" (
    echo [配置] 测试类别：%2
) else (
    echo [配置] 测试类别：all（所有）
)
echo.
echo [提示] 测试报告将保存到 test/results 目录
echo.

python test_automated.py %1 %2

echo.
echo ====================================
echo   测试完成
echo ====================================
echo.
echo [报告] 查看 test/results/latest_report.json 了解详情
echo.

pause
