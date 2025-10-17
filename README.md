# FigAgent - 自动化数据可视化Agent

一个基于DeepSeek大语言模型的智能数据可视化工具，可以自动分析数据特征并生成高质量的可视化图表。

## 功能特点

### 核心功能

1. **智能数据分析**
   - 自动识别数据格式（CSV、Excel、JSON等）
   - 分析数据特征（数值列、分类列、时间列）
   - 提供详细的数据摘要和统计信息

2. **AI驱动的可视化生成**
   - 根据数据特征自动推荐合适的可视化类型
   - 基于用户需求生成定制化的可视化代码
   - 支持matplotlib、seaborn等主流可视化库
   - **默认采用SCI论文风格**：简洁专业、英文标签、高分辨率（300 DPI）

3. **迭代优化**
   - 根据用户反馈不断优化可视化效果
   - 支持多轮对话式的图表调整
   - 自动记录历史版本

4. **代码导出**
   - 导出完整的Python可视化脚本
   - 代码可直接运行，方便复用和修改

## 项目结构

```
fig_agent/
├── __init__.py              # 包初始化文件
├── config.py                # 配置文件（API密钥）
├── visualization_agent.py   # 主Agent类
├── data_analyzer.py         # 数据分析模块
├── llm_client.py           # LLM客户端模块
├── code_executor.py        # 代码执行模块
├── cli.py                  # 命令行界面
├── example_usage.py        # 使用示例
└── README.md               # 项目文档
```

## 安装依赖

```bash
pip install pandas numpy matplotlib seaborn requests
```

## 配置

在 `config.py` 中设置你的DeepSeek API密钥：

```python
DEEPSEEK_API_KEY = "your-api-key-here"
```

## 使用方法

### 方法1: 命令行界面

```bash
python -m fig_agent.cli
```

交互式菜单提供以下功能：
- 加载数据文件
- 查看数据摘要
- 获取可视化建议
- 生成可视化
- 优化可视化
- 导出代码
- 查看历史记录

### 方法2: Python API

#### 基础使用

```python
from fig_agent import VisualizationAgent
from fig_agent.config import DEEPSEEK_API_KEY

# 初始化Agent
agent = VisualizationAgent(
    api_key=DEEPSEEK_API_KEY,
    output_dir="./output"
)

# 加载数据
agent.load_data(["data/sample.csv"])

# 生成可视化
result = agent.generate_visualization(
    requirements="生成一个美观的数据分布图"
)

if result['success']:
    print(f"成功！图片已保存到: {result['output_file']}")
```

#### 高级用法：迭代优化

```python
# 第一次生成
result1 = agent.generate_visualization(
    requirements="生成散点图"
)

# 根据反馈优化
result2 = agent.refine_visualization(
    feedback="请使用更大的点，并添加趋势线"
)
```

#### 获取可视化建议

```python
# 获取AI推荐的可视化类型
suggestions = agent.suggest_visualizations()
```

#### 导出代码

```python
# 将生成的代码导出为Python脚本
agent.export_code("my_visualization.py")
```

## 默认样式设置

### 📊 SCI论文风格（默认）

FigAgent默认生成**符合科学论文标准**的可视化图表，具有以下特点：

- ✅ **英文标签**：所有标题、坐标轴、图例默认使用英文
- ✅ **专业配色**：色盲友好的配色方案，避免使用过亮或霓虹色
- ✅ **高分辨率**：300 DPI，适合论文发表
- ✅ **简洁设计**：移除顶部和右侧边框，使用浅色网格
- ✅ **标准字体**：Arial或DejaVu Sans，字号适中（标题14pt，坐标轴12pt）
- ✅ **出版级质量**：符合Nature、Science等顶级期刊要求

### 自定义样式

如果需要中文标签或其他风格，可以在需求中明确指定：

```python
# 使用中文标签
result = agent.generate_visualization(
    requirements="""
    Generate a line chart showing sales trends.
    Use CHINESE labels and titles.
    Use SimHei font for Chinese characters.
    """
)

# 自定义配色和风格
result = agent.generate_visualization(
    requirements="""
    Create a bar chart with:
    - Chinese labels (中文标签)
    - Bright, colorful design (not scientific style)
    - Large fonts (16pt for title, 14pt for labels)
    - Gradient colors from blue to red
    """
)
```

### 常见自定义选项

```python
# 1. 演示文稿风格（大字体、鲜艳颜色）
requirements = """
Create a presentation-style chart:
- Large fonts (title 18pt, labels 16pt)
- Bright, high-contrast colors
- Bold lines (width 3.0)
- Dark background with light text
"""

# 2. 网页风格（现代、交互式）
requirements = """
Create a modern web-style visualization:
- Use Plotly for interactivity
- Modern color scheme (e.g., #3498db, #e74c3c)
- Hover tooltips
- Responsive design
"""

# 3. 打印风格（黑白、高对比度）
requirements = """
Create a print-friendly black and white chart:
- Grayscale colors only
- Different line styles (solid, dashed, dotted)
- High contrast
- Clear patterns for filled areas
"""
```

## 使用示例

查看 `example_usage.py` 获取更多详细示例：

```bash
python -m fig_agent.example_usage
```

## API参考

### VisualizationAgent

主Agent类，集成所有功能。

#### 初始化参数
- `api_key`: DeepSeek API密钥
- `output_dir`: 输出目录路径（默认：`./output`）

#### 主要方法

**load_data(file_paths: List[str])**
- 加载一个或多个数据文件
- 返回加载结果字典

**suggest_visualizations(file_path: Optional[str] = None)**
- 获取AI推荐的可视化类型
- 返回建议列表

**generate_visualization(file_path: Optional[str] = None, requirements: Optional[str] = None, output_filename: Optional[str] = None)**
- 生成可视化图表
- 返回执行结果字典

**refine_visualization(feedback: str, output_filename: Optional[str] = None)**
- 根据反馈优化可视化
- 返回优化结果字典

**export_code(output_file: str = "visualization_script.py")**
- 导出最后生成的代码
- 无返回值

**get_history()**
- 获取操作历史记录
- 返回历史记录字典

## 支持的数据格式

- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- Parquet (.parquet)
- 文本文件 (.txt)

## 工作原理

1. **数据分析**: 自动读取并分析数据，识别列类型、统计特征等
2. **需求理解**: 结合数据特征和用户需求，使用LLM理解可视化意图
3. **代码生成**: LLM生成完整的Python可视化代码
4. **安全执行**: 在沙箱环境中执行代码，生成图表
5. **迭代优化**: 根据用户反馈不断改进

## 示例场景

### 场景1: 快速探索数据

```python
agent = VisualizationAgent(api_key=API_KEY)
agent.load_data(["sales_data.csv"])
agent.suggest_visualizations()  # 获取建议
agent.generate_visualization()  # 自动生成合适的图表
```

### 场景2: 定制化报表

```python
agent = VisualizationAgent(api_key=API_KEY)
agent.load_data(["quarterly_report.xlsx"])

requirements = """
请创建一个专业的季度报表图表：
1. 柱状图显示各季度收入
2. 添加同比增长率的折线
3. 使用公司配色方案（蓝色主色调）
4. 添加数据标签
5. 标题使用18号字体
"""

agent.generate_visualization(requirements=requirements)
```

### 场景3: 论文图表制作

```python
agent = VisualizationAgent(api_key=API_KEY)
agent.load_data(["experiment_results.csv"])

requirements = """
生成符合学术论文标准的图表：
1. 使用箱线图展示实验结果
2. 添加显著性标记
3. 黑白配色，适合打印
4. 坐标轴标签使用Times New Roman字体
5. 图例放在右上角
"""

result = agent.generate_visualization(requirements=requirements)

# 如果需要调整
agent.refine_visualization(
    feedback="请增大字体大小，调整为双列宽度"
)
```

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到公开仓库
2. **数据隐私**: 数据会通过API传输摘要信息（非完整数据）
3. **代码执行**: 生成的代码会在本地执行，请确保环境安全
4. **网络连接**: 需要稳定的网络连接以访问DeepSeek API



