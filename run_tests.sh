#!/bin/bash

echo "===================================="
echo "  StaffFAQ 自动化测试"
echo "===================================="
echo ""

# 检查是否传入了 API Key 参数
if [ -z "$1" ]; then
    echo "[错误] 请传入 DeepSeek API Key"
    echo ""
    echo "用法：./run_tests.sh sk-你的APIKey [类别]"
    echo "示例：./run_tests.sh sk-cbe6232d3c47455bb502d46b8a804300"
    echo "      ./run_tests.sh sk-cbe6232d3c47455bb502d46b8a804300 annual_leave"
    echo ""
    exit 1
fi

echo "[配置] API Key: ${1:0:10}..."
if [ -n "$2" ]; then
    echo "[配置] 测试类别：$2"
else
    echo "[配置] 测试类别：all（所有）"
fi
echo ""
echo "[提示] 测试报告将保存到 test/results 目录"
echo ""

python test_automated.py "$1" "$2"

echo ""
echo "===================================="
echo "  测试完成"
echo "===================================="
echo ""
echo "[报告] 查看 test/results/latest_report.json 了解详情"
echo ""
