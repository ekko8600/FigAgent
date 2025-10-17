"""
FigAgent - 自动化数据可视化Agent入口文件

这个文件提供了快速导入和使用FigAgent的便捷方式。
"""

from .visualization_agent import VisualizationAgent
from .config import DEEPSEEK_API_KEY

# 导出主要接口
__all__ = ['VisualizationAgent', 'DEEPSEEK_API_KEY']


def create_agent(api_key=None, output_dir="./output"):
    """
    快速创建一个VisualizationAgent实例
    
    Args:
        api_key: DeepSeek API密钥，如果为None则使用config中的密钥
        output_dir: 输出目录
        
    Returns:
        VisualizationAgent实例
    """
    if api_key is None:
        api_key = DEEPSEEK_API_KEY
    
    return VisualizationAgent(api_key=api_key, output_dir=output_dir)
