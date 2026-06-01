#!/bin/bash

echo "========================================"
echo "  StaffFAQ 安装脚本 (Linux/Mac)"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi

echo "[1/4] 创建虚拟环境..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[错误] 创建虚拟环境失败"
    exit 1
fi

echo "[2/4] 激活虚拟环境..."
source venv/bin/activate

echo "[3/4] 升级 pip..."
pip install --upgrade pip

echo "[4/4] 安装依赖包..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 安装依赖失败"
    exit 1
fi

echo ""
echo "========================================"
echo "  安装完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. 复制 .env.example 为 .env"
echo "2. 在 .env 文件中填入你的 API Key"
echo "3. 运行: streamlit run app.py"
echo ""
