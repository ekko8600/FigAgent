import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from .data_analyzer import DataAnalyzer
from .llm_client import DeepSeekClient
from .code_executor import CodeExecutor


class VisualizationAgent:
    def __init__(self, api_key: str, output_dir: str = "./output"):
        self.api_key = api_key
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.data_analyzer = DataAnalyzer()
        self.llm_client = DeepSeekClient(api_key)
        self.code_executor = CodeExecutor(output_dir)
        
        self.current_data = {}
        self.current_analyses = {}
        self.generated_codes = []
        self.execution_history = []
    
    def load_data(self, file_paths: List[str]) -> Dict[str, Any]:
        """加载数据文件或文件夹"""
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        file_paths = self.data_analyzer.resolve_paths(file_paths)
        
        if not file_paths:
            print("未找到任何数据文件")
            return {}
        
        print(f"正在加载 {len(file_paths)} 个数据文件...")
        results = self.data_analyzer.analyze_multiple_files(file_paths)
        
        for file_path, result in results.items():
            if result['success']:
                self.current_data[file_path] = result['data']
                self.current_analyses[file_path] = result['analysis']
                print(f"✓ 成功加载: {file_path}")
                print(self.data_analyzer.generate_summary(result['analysis']))
            else:
                print(f"✗ 加载失败: {file_path} - {result['error']}")
        
        return results
    
    def suggest_visualizations(self, file_path: Optional[str] = None) -> List[str]:
        """建议可视化类型"""
        if not self.current_analyses:
            raise ValueError("请先加载数据")
        
        if file_path is None:
            file_path = list(self.current_analyses.keys())[0]
        
        analysis = self.current_analyses[file_path]
        summary = self.data_analyzer.generate_summary(analysis)
        
        print("正在分析数据特征并生成建议...")
        suggestions = self.llm_client.suggest_visualizations(summary)
        
        print("\n推荐的可视化类型：")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        
        return suggestions
    
    def generate_visualization(
        self, 
        file_path: Optional[str] = None,
        requirements: Optional[str] = None,
        output_filename: Optional[str] = None,
        allow_multiple: bool = True,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """生成可视化，支持单图或多图输出，失败时自动修复"""
        if not self.current_analyses:
            raise ValueError("请先加载数据")
        
        if file_path is None:
            file_path = list(self.current_data.keys())[0]
        
        if file_path not in self.current_data:
            raise ValueError(f"数据文件 {file_path} 未加载")
        
        df = self.current_data[file_path]
        analysis = self.current_analyses[file_path]
        summary = self.data_analyzer.generate_summary(analysis)
        
        if output_filename is None:
            output_filename = f"visualization_{len(self.generated_codes)}"
        
        # 尝试多次直到成功
        error_feedback = None
        for attempt in range(max_retries):
            if attempt > 0:
                print(f"\n第 {attempt + 1} 次尝试修复代码...")
            else:
                print("正在生成可视化代码...")
            
            code = self.llm_client.generate_visualization_code(
                data_summary=summary,
                user_requirements=requirements,
                allow_multiple=allow_multiple,
                num_files=len(self.current_data),
                previous_code=code if attempt > 0 else None,
                feedback=error_feedback if attempt > 0 else None
            )
            
            self.generated_codes.append({
                'code': code,
                'requirements': requirements,
                'file_path': file_path
            })
            
            print("生成的代码：")
            print("-" * 80)
            print(code)
            print("-" * 80)
            
            validation = self.code_executor.validate_code(code)
            if not validation['valid']:
                if attempt < max_retries - 1:
                    error_feedback = f"Code validation failed: {validation['error']}\n\nPlease fix the syntax errors."
                    continue
                else:
                    return {
                        'success': False,
                        'error': f"代码验证失败: {validation['error']}",
                        'code': code
                    }
            
            print("\n正在执行代码生成可视化...")
            
            result = self.code_executor.execute_visualization_code(
                code=code,
                df=df,
                output_filename=self.output_dir,
                base_filename=output_filename
            )
            
            self.execution_history.append(result)
            
            if result['success']:
                if isinstance(result.get('output_files'), list):
                    print(f"✓ 成功生成 {len(result['output_files'])} 个可视化:")
                    for f in result['output_files']:
                        print(f"  - {f}")
                else:
                    print(f"✓ 可视化成功生成: {result.get('output_file')}")
                result['code'] = code
                return result
            else:
                print(f"✗ 执行失败: {result['error']}")
                if attempt < max_retries - 1:
                    error_feedback = f"Code execution failed with error:\n{result['error']}\n\nPlease fix the code to resolve this error."
        
        result['code'] = code
        return result
    
    def generate_all_visualizations(self, requirements: Optional[str] = None, max_retries: int = 3) -> Dict[str, Any]:
        """统一分析所有数据，生成综合可视化，失败时自动修复"""
        if not self.current_data:
            raise ValueError("请先加载数据")
        
        print(f"\n{'='*60}")
        print(f"综合分析 {len(self.current_data)} 个数据文件")
        print('='*60)
        
        # 生成所有数据的综合摘要
        combined_summary = self._generate_combined_summary()
        
        output_filename = "combined_visualization"
        
        # 尝试多次直到成功
        error_feedback = None
        for attempt in range(max_retries):
            if attempt > 0:
                print(f"\n第 {attempt + 1} 次尝试修复代码...")
            else:
                print("\n正在生成综合可视化代码...")
            
            # 如果是修复，将错误信息添加到摘要中
            current_summary = combined_summary
            if error_feedback:
                current_summary += f"\n\nPrevious error: {error_feedback}"
            
            # 生成代码，智能判断是否需要多图
            code = self.llm_client.generate_combined_visualization_code(
                combined_summary=current_summary,
                user_requirements=requirements,
                num_datasets=len(self.current_data),
                data_dict=self.current_data
            )
            
            self.generated_codes.append({
                'code': code,
                'requirements': requirements,
                'file_path': 'combined_all',
                'is_combined': True
            })
            
            print("生成的代码：")
            print("-" * 80)
            print(code)
            print("-" * 80)
            
            validation = self.code_executor.validate_code(code)
            if not validation['valid']:
                if attempt < max_retries - 1:
                    error_feedback = f"Code validation failed: {validation['error']}\n\nPlease fix the syntax errors."
                    continue
                else:
                    return {
                        'success': False,
                        'error': f"代码验证失败: {validation['error']}",
                        'code': code
                    }
            
            print("\n正在执行代码生成可视化...")
            
            # 执行代码，传入所有数据
            result = self.code_executor.execute_combined_visualization(
                code=code,
                data_dict=self.current_data,
                output_dir=self.output_dir,
                base_filename=output_filename
            )
            
            self.execution_history.append(result)
            
            if result['success']:
                if isinstance(result.get('output_files'), list) and len(result['output_files']) > 1:
                    print(f"✓ 成功生成 {len(result['output_files'])} 个可视化:")
                    for f in result['output_files']:
                        print(f"  - {f}")
                else:
                    print(f"✓ 可视化成功生成: {result.get('output_file')}")
                result['code'] = code
                return result
            else:
                print(f"✗ 执行失败: {result['error']}")
                if attempt < max_retries - 1:
                    error_feedback = f"Code execution failed with error:\n{result['error']}\n\nPlease fix the code to resolve this error."
        
        result['code'] = code
        return result
    
    def _generate_combined_summary(self) -> str:
        """生成所有数据的综合摘要"""
        summaries = []
        summaries.append(f"Total datasets: {len(self.current_data)}\n")
        
        for i, (file_path, analysis) in enumerate(self.current_analyses.items(), 1):
            filename = Path(file_path).name
            summaries.append(f"\n--- Dataset {i}: {filename} ---")
            summaries.append(self.data_analyzer.generate_summary(analysis))
        
        # 添加整体统计
        total_rows = sum(a['shape'][0] for a in self.current_analyses.values())
        all_numeric_cols = set()
        all_categorical_cols = set()
        
        for analysis in self.current_analyses.values():
            all_numeric_cols.update(analysis['numeric_columns'])
            all_categorical_cols.update(analysis['categorical_columns'])
        
        summaries.append(f"\n\n--- Overall Statistics ---")
        summaries.append(f"Total rows across all datasets: {total_rows}")
        summaries.append(f"Common numeric columns: {list(all_numeric_cols)}")
        summaries.append(f"Common categorical columns: {list(all_categorical_cols)}")
        
        return '\n'.join(summaries)
    
    def refine_visualization(
        self, 
        feedback: str,
        output_filename: Optional[str] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """根据反馈优化可视化"""
        if not self.generated_codes:
            raise ValueError("还没有生成过可视化")
        
        last_generation = self.generated_codes[-1]
        previous_code = last_generation['code']
        file_path = last_generation['file_path']
        requirements = last_generation['requirements']
        is_combined = last_generation.get('is_combined', False)
        
        # 处理综合可视化的情况
        if is_combined or file_path == 'combined_all':
            return self._refine_combined_visualization(feedback, output_filename, max_retries)
        
        # 处理单文件可视化
        df = self.current_data[file_path]
        analysis = self.current_analyses[file_path]
        summary = self.data_analyzer.generate_summary(analysis)
        
        if output_filename is None:
            output_filename = f"visualization_refined_{len(self.generated_codes)}"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        print("正在根据反馈优化代码...")
        
        # 尝试多次直到成功
        for attempt in range(max_retries):
            if attempt > 0:
                print(f"\n第 {attempt + 1} 次尝试修复代码...")
            
            code = self.llm_client.generate_visualization_code(
                data_summary=summary,
                user_requirements=requirements,
                previous_code=previous_code,
                feedback=feedback
            )
            
            self.generated_codes.append({
                'code': code,
                'requirements': requirements,
                'feedback': feedback,
                'file_path': file_path
            })
            
            print("优化后的代码：")
            print("-" * 80)
            print(code)
            print("-" * 80)
            
            result = self.code_executor.execute_visualization_code(
                code=code,
                df=df,
                output_filename=output_path
            )
            
            self.execution_history.append(result)
            
            if result['success']:
                print(f"✓ 优化后的可视化生成成功: {output_path}")
                result['code'] = code
                return result
            else:
                print(f"✗ 执行失败: {result['error']}")
                if attempt < max_retries - 1:
                    # 将错误作为反馈，让LLM修复
                    feedback = f"Code execution failed with error:\n{result['error']}\n\nPlease fix the code to resolve this error."
                    previous_code = code
        
        result['code'] = code
        return result
    
    def _refine_combined_visualization(
        self,
        feedback: str,
        output_filename: Optional[str] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """优化综合可视化"""
        last_generation = self.generated_codes[-1]
        previous_code = last_generation['code']
        requirements = last_generation['requirements']
        
        combined_summary = self._generate_combined_summary()
        
        if output_filename is None:
            output_filename = f"combined_visualization_refined_{len(self.generated_codes)}"
        
        print("正在根据反馈优化综合可视化代码...")
        
        # 尝试多次直到成功
        for attempt in range(max_retries):
            if attempt > 0:
                print(f"\n第 {attempt + 1} 次尝试修复代码...")
            
            code = self.llm_client.generate_combined_visualization_code(
                combined_summary=combined_summary,
                user_requirements=requirements if not feedback.startswith("Code execution failed") else None,
                num_datasets=len(self.current_data),
                data_dict=self.current_data
            )
            
            # 如果是修复错误，添加错误信息到生成请求中
            if feedback.startswith("Code execution failed"):
                code = self.llm_client.generate_combined_visualization_code(
                    combined_summary=combined_summary + f"\n\nPrevious error: {feedback}",
                    user_requirements=requirements,
                    num_datasets=len(self.current_data),
                    data_dict=self.current_data
                )
            
            self.generated_codes.append({
                'code': code,
                'requirements': requirements,
                'feedback': feedback,
                'file_path': 'combined_all',
                'is_combined': True
            })
            
            print("优化后的代码：")
            print("-" * 80)
            print(code)
            print("-" * 80)
            
            result = self.code_executor.execute_combined_visualization(
                code=code,
                data_dict=self.current_data,
                output_dir=self.output_dir,
                base_filename=output_filename
            )
            
            self.execution_history.append(result)
            
            if result['success']:
                if isinstance(result.get('output_files'), list) and len(result['output_files']) > 1:
                    print(f"✓ 成功生成 {len(result['output_files'])} 个优化后的可视化:")
                    for f in result['output_files']:
                        print(f"  - {f}")
                else:
                    print(f"✓ 优化后的可视化生成成功: {result.get('output_file')}")
                result['code'] = code
                return result
            else:
                print(f"✗ 执行失败: {result['error']}")
                if attempt < max_retries - 1:
                    # 将错误作为反馈
                    feedback = f"Code execution failed with error:\n{result['error']}\n\nPlease fix the code to resolve this error."
                    previous_code = code
        
        result['code'] = code
        return result
    
    def get_history(self) -> Dict[str, Any]:
        """获取历史记录"""
        return {
            'loaded_files': list(self.current_data.keys()),
            'generated_codes': self.generated_codes,
            'execution_history': self.execution_history
        }
    
    def export_code(self, output_file: str = "visualization_script.py"):
        """导出最后生成的代码"""
        if not self.generated_codes:
            raise ValueError("还没有生成过代码")
        
        code = self.generated_codes[-1]['code']
        output_path = os.path.join(self.output_dir, output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"代码已导出到: {output_path}")
