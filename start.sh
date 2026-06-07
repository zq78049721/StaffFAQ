#!/bin/bash

echo "========================================"
echo "  StaffFAQ 安全启动脚本"
echo "========================================"
echo ""
echo "[说明] 支持两种方式启动："
echo "  1. python app.py sk-你的APIKey  （命令行传入，推荐）"
echo "  2. 直接运行此脚本（从 .env 读取）"
echo ""

# 检查是否传入了 API Key 参数
if [ -z "$1" ]; then
    # 没有传入参数，检查 .env 文件
    if [ -f ".env" ]; then
        echo "[模式] 从 .env 文件读取配置"
        echo "[提示] 如需传入 API Key，请使用: ./start.sh sk-你的APIKey"
        echo ""
    else
        echo "[模式] 交互式配置"
        echo "===================================="
        echo "  配置 DeepSeek API Key"
        echo "===================================="
        echo ""
        echo "[说明] 此配置仅保存在内存中，不会写入文件"
        echo "[说明] 每次重启服务器需要重新输入"
        echo ""
        
        read -p "请输入 DeepSeek API Key (sk-开头): " DEEPSEEK_KEY
        
        if [ -z "$DEEPSEEK_KEY" ]; then
            echo "[错误] API Key 不能为空！"
            exit 1
        fi
        
        if [[ $DEEPSEEK_KEY == sk-* ]]; then
            echo "[✓] API Key 格式正确"
        else
            echo "[警告] API Key 应该以 sk- 开头，请确认是否正确"
            echo ""
            read -p "是否继续？(y/n): " CONFIRM
            if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
                echo "[已取消]"
                exit 1
            fi
        fi
        
        # 设置环境变量（仅在当前会话中有效）
        export LLM_PROVIDER=deepseek
        export LLM_MODEL=deepseek-chat
        export DEEPSEEK_API_KEY=$DEEPSEEK_KEY
        export TEMPERATURE=0.2
        
        echo ""
        echo "[✓] 配置完成，正在启动服务器..."
        echo ""
    fi
else
    # 传入了参数，直接使用
    echo "[模式] 从命令行参数读取 API Key"
    echo "[参数] ${1:0:10}..."
    echo ""
fi

echo "========================================"
echo "  启动服务器"
echo "========================================"
echo ""

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "rag_env/bin/activate" ]; then
    source rag_env/bin/activate
else
    echo "[错误] 未找到虚拟环境，请先运行 setup.sh"
    exit 1
fi

# 显示配置信息
echo "[配置] LLM Provider: ${LLM_PROVIDER:-从.env 读取}"
echo "[配置] LLM Model: ${LLM_MODEL:-从.env 读取}"
echo "[配置] Temperature: ${TEMPERATURE:-从.env 读取}"
if [ -n "$DEEPSEEK_API_KEY" ]; then
    echo "[配置] API Key: ${DEEPSEEK_API_KEY:0:10}... (已隐藏)"
else
    echo "[配置] API Key: 从 .env 文件读取"
fi
echo ""

echo "[启动] 正在启动 StaffFAQ..."
echo "[提示] 按 Ctrl+C 停止服务"
echo ""

streamlit run app.py -- "$1"
