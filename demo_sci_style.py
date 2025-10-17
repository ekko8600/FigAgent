"""
演示SCI论文风格的可视化生成

这个脚本展示了FigAgent默认生成的科学论文风格图表
"""
import pandas as pd
import numpy as np
from pathlib import Path
from fig_agent import VisualizationAgent
from fig_agent.config import DEEPSEEK_API_KEY


def create_demo_data():
    """创建演示数据"""
    print("创建演示数据...")
    
    # 创建数据目录
    data_dir = Path("./demo_data")
    data_dir.mkdir(exist_ok=True)
    
    # 科研实验数据示例
    np.random.seed(42)
    
    # 示例1: 不同处理组的实验结果
    treatments = ['Control', 'Treatment A', 'Treatment B', 'Treatment C']
    data = []
    for treatment in treatments:
        base_value = {'Control': 50, 'Treatment A': 65, 'Treatment B': 75, 'Treatment C': 70}[treatment]
        values = np.random.normal(base_value, 8, 30)
        data.extend([{'Treatment': treatment, 'Response': val, 'Replicate': i+1} 
                    for i, val in enumerate(values)])
    
    experiment_data = pd.DataFrame(data)
    experiment_file = data_dir / "experiment_results.csv"
    experiment_data.to_csv(experiment_file, index=False)
    print(f"✓ 创建实验数据: {experiment_file}")
    
    # 示例2: 时间序列数据
    time_points = np.arange(0, 100, 2)
    group1 = 10 * np.exp(0.03 * time_points) + np.random.normal(0, 5, len(time_points))
    group2 = 8 * np.exp(0.035 * time_points) + np.random.normal(0, 5, len(time_points))
    
    timeseries_data = pd.DataFrame({
        'Time': np.tile(time_points, 2),
        'Value': np.concatenate([group1, group2]),
        'Group': ['Group 1']*len(time_points) + ['Group 2']*len(time_points)
    })
    timeseries_file = data_dir / "timeseries_data.csv"
    timeseries_data.to_csv(timeseries_file, index=False)
    print(f"✓ 创建时间序列数据: {timeseries_file}")
    
    return [str(experiment_file), str(timeseries_file)]


def demo_default_style():
    """演示默认SCI论文风格"""
    print("\n" + "="*70)
    print("FigAgent - SCI论文风格演示")
    print("="*70)
    
    # 创建示例数据
    demo_files = create_demo_data()
    
    # 初始化Agent
    print("\n初始化VisualizationAgent...")
    agent = VisualizationAgent(
        api_key=DEEPSEEK_API_KEY,
        output_dir="./demo_output"
    )
    print("✓ Agent初始化完成")
    
    # 示例1: 箱线图（默认SCI风格）
    print("\n" + "-"*70)
    print("示例1: 生成默认SCI论文风格的箱线图")
    print("-"*70)
    
    agent.load_data([demo_files[0]])
    
    try:
        result1 = agent.generate_visualization(
            requirements="""
            Create a box plot comparing Response values across different Treatments.
            Show individual data points overlaid on boxes.
            Add statistical significance markers if applicable.
            """,
            output_filename="sci_boxplot.png"
        )
        
        if result1['success']:
            print(f"\n✓ 图表生成成功: {result1['output_file']}")
            print("\n特点:")
            print("  - 英文标签")
            print("  - 简洁的边框（只保留左边和底部）")
            print("  - 色盲友好的配色")
            print("  - 300 DPI高分辨率")
            print("  - 适合论文发表")
        else:
            print(f"\n✗ 生成失败: {result1['error']}")
    except Exception as e:
        print(f"\n✗ 出错: {str(e)}")
    
    # 示例2: 折线图（默认SCI风格）
    print("\n" + "-"*70)
    print("示例2: 生成默认SCI论文风格的时间序列图")
    print("-"*70)
    
    agent.load_data([demo_files[1]])
    
    try:
        result2 = agent.generate_visualization(
            requirements="""
            Create a line plot showing Value vs Time for both groups.
            Use different line styles for different groups.
            Add confidence intervals or error bands if appropriate.
            """,
            output_filename="sci_lineplot.png"
        )
        
        if result2['success']:
            print(f"\n✓ 图表生成成功: {result2['output_file']}")
            print("\n特点:")
            print("  - 专业的线条样式")
            print("  - 清晰的图例")
            print("  - 标准的字体大小")
            print("  - 适合期刊投稿")
        else:
            print(f"\n✗ 生成失败: {result2['error']}")
    except Exception as e:
        print(f"\n✗ 出错: {str(e)}")
    
    # 示例3: 自定义为中文风格
    print("\n" + "-"*70)
    print("示例3: 自定义使用中文标签")
    print("-"*70)
    
    try:
        result3 = agent.generate_visualization(
            file_path=demo_files[0],
            requirements="""
            Create a bar chart showing mean Response for each Treatment.
            
            IMPORTANT: Use CHINESE labels and title:
            - Title: "不同处理组的响应值比较"
            - X-axis: "处理组"
            - Y-axis: "响应值"
            - Use SimHei font for Chinese characters
            
            Add error bars showing standard deviation.
            """,
            output_filename="chinese_barchart.png"
        )
        
        if result3['success']:
            print(f"\n✓ 图表生成成功: {result3['output_file']}")
            print("\n特点:")
            print("  - 中文标签")
            print("  - 仍保持专业风格")
            print("  - 可根据需求完全定制")
        else:
            print(f"\n✗ 生成失败: {result3['error']}")
    except Exception as e:
        print(f"\n✗ 出错: {str(e)}")
    
    # 总结
    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)
    print("\n生成的图表保存在: ./demo_output/")
    print("\n默认特点:")
    print("  ✓ 英文标签（符合国际期刊要求）")
    print("  ✓ SCI论文风格（简洁专业）")
    print("  ✓ 300 DPI高分辨率（适合打印）")
    print("  ✓ 色盲友好的配色")
    print("  ✓ 可通过需求描述完全自定义")
    print("\n如需中文标签，只需在需求中明确说明即可！")


if __name__ == "__main__":
    # 检查API密钥
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your-api-key-here":
        print("="*70)
        print("错误: 请先配置DeepSeek API密钥")
        print("="*70)
        print("\n请编辑 fig_agent/config.py 文件，设置你的API密钥：")
        print("DEEPSEEK_API_KEY = 'your-actual-api-key'")
        print("\n如果你还没有API密钥，请访问 https://www.deepseek.com 获取")
    else:
        demo_default_style()

