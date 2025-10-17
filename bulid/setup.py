"""
cx_Freeze setup script (替代方案)
用于将FigAgent打包成Windows可执行文件
"""
from cx_Freeze import setup, Executable
import sys

# 依赖的模块
build_exe_options = {
    "packages": [
        "os", "sys", "pathlib",
        "pandas", "numpy", 
        "matplotlib", "seaborn",
        "requests", "json",
        "openpyxl", "pyarrow",
        "fig_agent",
    ],
    "excludes": [
        "tkinter",
        "PyQt5", "PyQt6",
        "PySide2", "PySide6",
        "IPython", "jupyter",
    ],
    "include_files": [
        # 如果需要包含额外文件，在这里添加
        # ("path/to/file", "destination"),
    ],
}

# GUI应用程序基础（如果需要无控制台窗口）
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

base = None  # 保留控制台窗口

setup(
    name="FigAgent",
    version="1.0",
    description="自动化数据可视化Agent",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "fig_agent_main.py",
            base=base,
            target_name="FigAgent.exe",
            # icon="icon.ico",  # 如果有图标
        )
    ],
)

# 使用方法：
# python setup.py build

