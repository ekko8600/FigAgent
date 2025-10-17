import argparse
from pathlib import Path
from .visualization_agent import VisualizationAgent
from .config_manager import ConfigManager


class CLI:
    def __init__(self, api_key: str):
        self.agent = VisualizationAgent(api_key=api_key)
        self.running = True
    
    def show_menu(self):
        """显示菜单"""
        print("\n" + "="*60)
        print("自动化数据可视化Agent")
        print("="*60)
        print("1. 加载数据文件/文件夹")
        print("2. 查看数据摘要")
        print("3. 获取可视化建议")
        print("4. 生成可视化")
        print("5. 为所有数据生成可视化")
        print("6. 优化当前可视化")
        print("7. 导出代码")
        print("8. 查看历史")
        print("0. 退出")
        print("="*60)
    
    def load_data_interactive(self):
        """交互式加载数据"""
        print("\n请输入数据文件或文件夹路径（多个用逗号分隔）：")
        print("  - 文件: /path/to/file.csv")
        print("  - 文件夹: /path/to/directory/")
        paths_input = input("> ").strip()
        
        if not paths_input:
            print("未输入路径")
            return
        
        paths = [p.strip() for p in paths_input.split(',')]
        self.agent.load_data(paths)
    
    def show_data_summary(self):
        """显示数据摘要"""
        if not self.agent.current_analyses:
            print("\n请先加载数据")
            return
        
        print("\n当前已加载的数据：")
        for i, (file_path, analysis) in enumerate(self.agent.current_analyses.items(), 1):
            print(f"\n{i}. {file_path}")
            print("-" * 60)
            summary = self.agent.data_analyzer.generate_summary(analysis)
            print(summary)
    
    def get_suggestions(self):
        """获取可视化建议"""
        if not self.agent.current_analyses:
            print("\n请先加载数据")
            return
        
        try:
            suggestions = self.agent.suggest_visualizations()
        except Exception as e:
            print(f"\n获取建议失败: {str(e)}")
    
    def generate_visualization_interactive(self):
        """交互式生成可视化"""
        if not self.agent.current_data:
            print("\n请先加载数据")
            return
        
        # 选择数据文件
        file_paths = list(self.agent.current_data.keys())
        if len(file_paths) > 1:
            print("\n请选择要可视化的数据：")
            for i, path in enumerate(file_paths, 1):
                print(f"{i}. {path}")
            try:
                choice = int(input("> ").strip())
                file_path = file_paths[choice - 1]
            except (ValueError, IndexError):
                print("无效的选择")
                return
        else:
            file_path = file_paths[0]
        
        # 输入需求
        print("\n请描述你的可视化需求（直接回车使用自动推荐）：")
        requirements = input("> ").strip()
        if not requirements:
            requirements = None
        
        # 输入输出文件名
        print("\n请输入输出文件名（直接回车使用默认名称）：")
        output_filename = input("> ").strip()
        if not output_filename:
            output_filename = None
        
        try:
            result = self.agent.generate_visualization(
                file_path=file_path,
                requirements=requirements,
                output_filename=output_filename
            )
            
            if not result['success']:
                print(f"\n生成失败: {result['error']}")
                print("\n是否要重试？(y/n)")
                if input("> ").strip().lower() == 'y':
                    self.generate_visualization_interactive()
        except Exception as e:
            print(f"\n生成失败: {str(e)}")
    
    def refine_visualization_interactive(self):
        """交互式优化可视化"""
        if not self.agent.generated_codes:
            print("\n请先生成可视化")
            return
        
        print("\n请描述你希望如何改进可视化：")
        feedback = input("> ").strip()
        
        if not feedback:
            print("未输入反馈")
            return
        
        print("\n请输入输出文件名（直接回车使用默认名称）：")
        output_filename = input("> ").strip()
        if not output_filename:
            output_filename = None
        
        try:
            result = self.agent.refine_visualization(
                feedback=feedback,
                output_filename=output_filename
            )
            
            if not result['success']:
                print(f"\n优化失败: {result['error']}")
        except Exception as e:
            print(f"\n优化失败: {str(e)}")
    
    def export_code_interactive(self):
        """交互式导出代码"""
        if not self.agent.generated_codes:
            print("\n请先生成可视化")
            return
        
        print("\n请输入输出文件名（直接回车使用默认名称）：")
        output_file = input("> ").strip()
        if not output_file:
            output_file = "visualization_script.py"
        
        try:
            self.agent.export_code(output_file)
        except Exception as e:
            print(f"\n导出失败: {str(e)}")
    
    def show_history(self):
        """显示历史"""
        history = self.agent.get_history()
        
        print("\n" + "="*60)
        print("历史记录")
        print("="*60)
        
        print(f"\n已加载文件数: {len(history['loaded_files'])}")
        for path in history['loaded_files']:
            print(f"  - {path}")
        
        print(f"\n已生成代码数: {len(history['generated_codes'])}")
        print(f"成功执行次数: {sum(1 for h in history['execution_history'] if h['success'])}")
        print(f"失败次数: {sum(1 for h in history['execution_history'] if not h['success'])}")
    
    def generate_all_visualizations_interactive(self):
        """为所有数据生成综合可视化"""
        if not self.agent.current_data:
            print("\n请先加载数据")
            return
        
        print(f"\n将综合分析 {len(self.agent.current_data)} 个数据文件")
        print("系统会将所有数据作为整体进行分析，并智能决定:")
        print("  - 生成单个综合图表（数据可有效对比时）")
        print("  - 生成多个图表（数据复杂需要分开展示时）")
        print("\n请描述可视化需求（直接回车使用自动推荐）：")
        requirements = input("> ").strip()
        if not requirements:
            requirements = None
        
        try:
            self.agent.generate_all_visualizations(requirements=requirements)
        except Exception as e:
            print(f"\n生成失败: {str(e)}")
    
    def run(self):
        """运行CLI"""
        print("\n欢迎使用自动化数据可视化Agent!")
        
        while self.running:
            self.show_menu()
            choice = input("\n请选择功能 (0-8): ").strip()
            
            if choice == '0':
                print("\n再见！")
                self.running = False
            elif choice == '1':
                self.load_data_interactive()
            elif choice == '2':
                self.show_data_summary()
            elif choice == '3':
                self.get_suggestions()
            elif choice == '4':
                self.generate_visualization_interactive()
            elif choice == '5':
                self.generate_all_visualizations_interactive()
            elif choice == '6':
                self.refine_visualization_interactive()
            elif choice == '7':
                self.export_code_interactive()
            elif choice == '8':
                self.show_history()
            else:
                print("\n无效的选择，请重试")


def main():
    parser = argparse.ArgumentParser(description='自动化数据可视化Agent')
    parser.add_argument('--api-key', type=str, help='DeepSeek API密钥')
    args = parser.parse_args()
    
    config_mgr = ConfigManager()
    
    if args.api_key:
        api_key = args.api_key
        config_mgr.save_api_key(api_key)
    else:
        api_key = config_mgr.prompt_for_api_key()
    
    if not api_key:
        print("\n错误: 需要API密钥才能继续")
        print("请访问 https://www.deepseek.com 获取API密钥")
        return
    
    cli = CLI(api_key=api_key)
    cli.run()


if __name__ == '__main__':
    main()

