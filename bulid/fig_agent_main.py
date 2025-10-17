#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FigAgent 主入口文件
用于PyInstaller打包和直接运行
"""
import sys
import os

# 确保打包后能找到模块
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe
    application_path = sys._MEIPASS
    # 设置matplotlib后端为Agg（无GUI）
    import matplotlib
    matplotlib.use('Agg')
else:
    # 如果是源码运行
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加到路径
sys.path.insert(0, application_path)

# 导入并运行CLI
from fig_agent.cli import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)

