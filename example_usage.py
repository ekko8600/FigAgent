"""
使用示例 - 展示如何使用VisualizationAgent
"""
from fig_agent import VisualizationAgent
from fig_agent.config import DEEPSEEK_API_KEY


def example_basic_usage():
    """基础使用示例"""
    print("="*60)
    print("示例1: 基础使用")
    print("="*60)
    
    # 初始化Agent
    agent = VisualizationAgent(api_key=DEEPSEEK_API_KEY, output_dir="./examples/output")
    
    # 加载数据
    print("\n1. 加载数据...")
    agent.load_data(["data/sample_data.csv"])
    
    # 获取可视化建议
    print("\n2. 获取可视化建议...")
    agent.suggest_visualizations()
    
    # 生成可视化
    print("\n3. 生成可视化...")
    result = agent.generate_visualization(
        requirements="生成一个美观的数据分布图"
    )
    
    if result['success']:
        print(f"\n成功！图片已保存到: {result['output_file']}")
    else:
        print(f"\n失败: {result['error']}")


def example_custom_requirements():
    """自定义需求示例"""
    print("\n" + "="*60)
    print("示例2: 自定义需求")
    print("="*60)
    
    agent = VisualizationAgent(api_key=DEEPSEEK_API_KEY, output_dir="./examples/output")
    
    # 加载数据
    agent.load_data(["data/sales_data.csv"])
    
    # 生成特定类型的可视化
    requirements = """
    请生成以下可视化：
    1. 使用柱状图展示各类别的销售额
    2. 添加数值标签
    3. 使用渐变颜色
    4. 标题使用大号字体
    5. 整体风格简洁专业
    """
    
    result = agent.generate_visualization(
        requirements=requirements,
        output_filename="sales_chart.png"
    )
    
    if result['success']:
        print(f"\n成功！图片已保存到: {result['output_file']}")


def example_iterative_refinement():
    """迭代优化示例"""
    print("\n" + "="*60)
    print("示例3: 迭代优化")
    print("="*60)
    
    agent = VisualizationAgent(api_key=DEEPSEEK_API_KEY, output_dir="./examples/output")
    
    # 加载数据
    agent.load_data(["data/time_series.csv"])
    
    # 第一次生成
    print("\n第一次生成...")
    result1 = agent.generate_visualization(
        requirements="生成时间序列折线图"
    )
    
    if result1['success']:
        print(f"生成成功: {result1['output_file']}")
        
        # 根据反馈优化
        print("\n根据反馈优化...")
        result2 = agent.refine_visualization(
            feedback="请添加移动平均线，并使用更鲜艳的颜色",
            output_filename="time_series_refined.png"
        )
        
        if result2['success']:
            print(f"优化成功: {result2['output_file']}")


def example_multiple_datasets():
    """多数据集示例"""
    print("\n" + "="*60)
    print("示例4: 多数据集")
    print("="*60)
    
    agent = VisualizationAgent(api_key=DEEPSEEK_API_KEY, output_dir="./examples/output")
    
    # 加载多个数据文件
    agent.load_data([
        "data/dataset1.csv",
        "data/dataset2.csv"
    ])
    
    # 为每个数据集生成可视化
    for file_path in agent.current_data.keys():
        print(f"\n为 {file_path} 生成可视化...")
        result = agent.generate_visualization(
            file_path=file_path,
            output_filename=f"{Path(file_path).stem}_visualization.png"
        )


def example_export_code():
    """导出代码示例"""
    print("\n" + "="*60)
    print("示例5: 导出代码")
    print("="*60)
    
    agent = VisualizationAgent(api_key=DEEPSEEK_API_KEY, output_dir="./examples/output")
    
    agent.load_data(["data/sample_data.csv"])
    
    result = agent.generate_visualization(
        requirements="生成散点图"
    )
    
    if result['success']:
        # 导出生成的代码
        agent.export_code("my_visualization_script.py")
        print("\n代码已导出，可以直接运行!")


if __name__ == "__main__":
    print("自动化数据可视化Agent - 使用示例\n")
    
    # 选择要运行的示例
    print("请选择要运行的示例:")
    print("1. 基础使用")
    print("2. 自定义需求")
    print("3. 迭代优化")
    print("4. 多数据集")
    print("5. 导出代码")
    print("0. 运行所有示例")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    examples = {
        '1': example_basic_usage,
        '2': example_custom_requirements,
        '3': example_iterative_refinement,
        '4': example_multiple_datasets,
        '5': example_export_code
    }
    
    if choice == '0':
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"\n示例执行失败: {str(e)}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"\n示例执行失败: {str(e)}")
    else:
        print("无效的选择")

