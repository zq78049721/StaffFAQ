@echo off
echo ====================================
echo   启动 StaffFAQ API 服务器
echo ====================================
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 启动 FastAPI 服务器
echo [INFO] 正在启动服务器...
echo [INFO] 访问地址: http://localhost:8000
echo [INFO] API 文档: http://localhost:8000/docs
echo.

python app.py

pause
