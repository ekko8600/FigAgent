#!/bin/bash
# FigAgent 安装脚本

echo "=================================="
echo "FigAgent 自动化数据可视化工具"
echo "安装脚本"
echo "=================================="
echo ""

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "当前Python版本: $python_version"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip"
    exit 1
fi

echo "✓ pip3 已安装"
echo ""

# 安装依赖
echo "安装依赖包..."
echo "这可能需要几分钟时间..."
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 依赖安装成功!"
else
    echo ""
    echo "✗ 依赖安装失败"
    echo "请手动运行: pip3 install -r requirements.txt"
    exit 1
fi

echo ""
echo "=================================="
echo "安装完成!"
echo "=================================="
echo ""
echo "下一步："
echo "1. 编辑 config.py 设置你的 DeepSeek API 密钥"
echo "2. 运行快速开始: python3 -m fig_agent.quickstart"
echo "3. 或运行命令行界面: python3 -m fig_agent.cli"
echo ""
echo "查看文档："
echo "- README.md - 项目概述"
echo "- USAGE_GUIDE.md - 详细使用指南"
echo "- PROJECT_SUMMARY.md - 项目总结"
echo ""
echo "Happy Visualizing! 📊✨"

