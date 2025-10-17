"""
FigAgent - 自动化数据可视化Agent

一个基于大语言模型的智能数据可视化工具，可以自动分析数据特征并生成合适的可视化代码。
"""

from .visualization_agent import VisualizationAgent
from .data_analyzer import DataAnalyzer
from .llm_client import DeepSeekClient
from .code_executor import CodeExecutor

__version__ = "0.1.0"
__all__ = ["VisualizationAgent", "DataAnalyzer", "DeepSeekClient", "CodeExecutor"]

