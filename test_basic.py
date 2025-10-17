"""
基础功能测试 - 测试不需要API调用的基本功能
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fig_agent.data_analyzer import DataAnalyzer
from fig_agent.code_executor import CodeExecutor


def test_data_analyzer():
    """测试数据分析模块"""
    print("="*60)
    print("测试1: 数据分析模块")
    print("="*60)
    
    # 创建测试数据
    test_data = pd.DataFrame({
        '数值列1': np.random.randn(100),
        '数值列2': np.random.randint(1, 100, 100),
        '分类列': np.random.choice(['A', 'B', 'C'], 100),
        '日期列': pd.date_range('2024-01-01', periods=100)
    })
    
    analyzer = DataAnalyzer()
    
    # 测试分析功能
    analysis = analyzer.analyze_dataframe(test_data)
    
    print("\n✓ DataFrame分析完成")
    print(f"  - 形状: {analysis['shape']}")
    print(f"  - 数值列: {analysis['numeric_columns']}")
    print(f"  - 分类列: {analysis['categorical_columns']}")
    print(f"  - 时间列: {analysis['datetime_columns']}")
    
    # 测试摘要生成
    summary = analyzer.generate_summary(analysis)
    print("\n✓ 数据摘要生成:")
    print(summary)
    
    return True


def test_code_executor():
    """测试代码执行模块"""
    print("\n" + "="*60)
    print("测试2: 代码执行模块")
    print("="*60)
    
    # 创建测试数据
    test_df = pd.DataFrame({
        'x': range(10),
        'y': [i**2 for i in range(10)]
    })
    
    # 创建测试代码
    test_code = """
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], marker='o')
plt.title('测试图表')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.grid(True)
plt.savefig('test_output.png', dpi=150, bbox_inches='tight')
"""
    
    executor = CodeExecutor(output_dir="./test_output")
    
    # 测试代码验证
    validation = executor.validate_code(test_code)
    print(f"\n✓ 代码验证: {'通过' if validation['valid'] else '失败'}")
    
    if not validation['valid']:
        print(f"  错误: {validation['error']}")
        return False
    
    # 测试代码执行
    result = executor.execute_visualization_code(
        code=test_code,
        df=test_df,
        output_filename="./test_output/test_chart.png"
    )
    
    print(f"\n✓ 代码执行: {'成功' if result['success'] else '失败'}")
    
    if result['success']:
        print(f"  输出文件: {result['output_file']}")
    else:
        print(f"  错误: {result['error']}")
    
    return result['success']


def test_data_loading():
    """测试数据加载功能"""
    print("\n" + "="*60)
    print("测试3: 数据文件加载")
    print("="*60)
    
    # 创建临时测试文件
    test_dir = Path("./test_data")
    test_dir.mkdir(exist_ok=True)
    
    test_csv = test_dir / "test.csv"
    test_data = pd.DataFrame({
        'A': range(50),
        'B': np.random.randn(50),
        'C': np.random.choice(['类别1', '类别2', '类别3'], 50)
    })
    test_data.to_csv(test_csv, index=False, encoding='utf-8-sig')
    
    analyzer = DataAnalyzer()
    
    # 测试读取
    df = analyzer.read_data(str(test_csv))
    print(f"\n✓ 成功读取CSV文件")
    print(f"  形状: {df.shape}")
    
    # 测试多文件分析
    results = analyzer.analyze_multiple_files([str(test_csv)])
    
    if str(test_csv) in results and results[str(test_csv)]['success']:
        print(f"✓ 成功分析文件")
    else:
        print(f"✗ 分析失败")
        return False
    
    # 清理
    test_csv.unlink()
    test_dir.rmdir()
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("FigAgent 基础功能测试")
    print("="*70)
    
    tests = [
        ("数据分析模块", test_data_analyzer),
        ("代码执行模块", test_code_executor),
        ("数据加载功能", test_data_loading)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name}测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    total_passed = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    print(f"\n通过率: {total_passed}/{total_tests} ({total_passed/total_tests*100:.1f}%)")
    
    if total_passed == total_tests:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  {total_tests - total_passed} 个测试失败")


if __name__ == "__main__":
    run_all_tests()

