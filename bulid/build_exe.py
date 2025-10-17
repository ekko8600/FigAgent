"""
构建Windows可执行文件的脚本
使用PyInstaller将FigAgent打包成exe
"""
import os
import sys
import subprocess
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller已安装 (版本: {PyInstaller.__version__})")
        return True
    except ImportError:
        print("✗ PyInstaller未安装")
        print("\n正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller安装完成")
        return True

def build_exe():
    """构建exe文件"""
    print("\n" + "="*60)
    print("开始构建FigAgent可执行文件")
    print("="*60 + "\n")
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return False
    
    # 根据操作系统确定路径分隔符
    import platform
    if platform.system() == 'Windows':
        path_sep = ';'
        exe_name = 'FigAgent.exe'
    else:
        path_sep = ':'
        exe_name = 'FigAgent'
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--name=FigAgent",
        "--onefile",  # 打包成单个文件
        "--console",  # 保留控制台窗口（CLI应用）
        f"--add-data=fig_agent{path_sep}fig_agent",  # 包含fig_agent模块
        "--hidden-import=matplotlib",
        "--hidden-import=seaborn",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=requests",
        "--hidden-import=openpyxl",
        "--hidden-import=pyarrow",
        "--collect-all=matplotlib",
        "--collect-all=seaborn",
        "--noupx",  # 不使用UPX压缩（避免某些问题）
        "fig_agent_main.py"
    ]
    
    print("执行命令:")
    print(" ".join(cmd))
    print()
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("✓ 构建成功！")
        print("="*60)
        print(f"\n可执行文件位置: dist/{exe_name}")
        print("\n使用方法:")
        print(f"  1. 命令行运行: ./{exe_name}")
        print(f"  2. 带参数运行: ./{exe_name} --api-key YOUR_API_KEY")
        if platform.system() == 'Windows':
            print(f"  3. 或直接双击 {exe_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 构建失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    import shutil
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['FigAgent.spec']
    
    print("\n清理构建文件...")
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"  删除目录: {d}")
    
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)
            print(f"  删除文件: {f}")
    
    print("✓ 清理完成")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='构建FigAgent.exe')
    parser.add_argument('--clean', action='store_true', help='清理构建文件')
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
    else:
        # 检查是否存在主入口文件
        if not os.path.exists('fig_agent_main.py'):
            print("创建主入口文件 fig_agent_main.py...")
            with open('fig_agent_main.py', 'w', encoding='utf-8') as f:
                f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
FigAgent 主入口文件
用于PyInstaller打包
\"\"\"
import sys
import os

# 确保打包后能找到模块
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe
    application_path = sys._MEIPASS
else:
    # 如果是源码运行
    application_path = os.path.dirname(os.path.abspath(__file__))

# 添加到路径
sys.path.insert(0, application_path)

# 导入并运行CLI
from fig_agent.cli import main

if __name__ == '__main__':
    main()
""")
            print("✓ 主入口文件创建完成")
        
        success = build_exe()
        
        if success:
            import platform
            system = platform.system()
            exe_name = 'FigAgent.exe' if system == 'Windows' else 'FigAgent'
            
            print("\n" + "="*60)
            print("📦 打包完成！")
            print("="*60)
            print("\n分发说明:")
            if system == 'Windows':
                print(f"  1. 将 dist/{exe_name} 复制到目标Windows电脑")
                print("  2. 确保目标电脑能访问互联网（调用DeepSeek API）")
                print("  3. 首次运行会提示输入API密钥")
                print("  4. API密钥会保存在 config.py 中")
            else:
                print(f"  1. 可执行文件位于 dist/{exe_name}")
                print("  2. 可以在当前系统（Linux/Mac）上运行")
                print("  3. 首次运行会提示输入API密钥")
                print(f"  4. 运行方式: cd dist && ./{exe_name}")
            print("\n注意事项:")
            print("  - 文件可能较大（100-200MB），因为包含了所有依赖")
            print("  - 首次运行可能需要几秒钟初始化")
            if system == 'Windows':
                print("  - 杀毒软件可能会误报，需要添加信任")

