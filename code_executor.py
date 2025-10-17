import sys
import io
import os
import glob
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional, List
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class CodeExecutor:
    def __init__(self, output_dir: str = "./"):
        self.output_dir = output_dir
    
    def execute_visualization_code(
        self, 
        code: str, 
        df: pd.DataFrame,
        output_filename: str = "output.png",
        base_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """执行可视化代码，支持多图输出"""
        result = {
            'success': False,
            'output': '',
            'error': '',
            'output_file': None,
            'output_files': []
        }
        
        exec_globals = {
            'pd': pd,
            'df': df,
            'np': __import__('numpy'),
            'plt': plt,
            'matplotlib': matplotlib,
            'sns': __import__('seaborn'),
            '__builtins__': __builtins__
        }
        
        # 处理文件名
        if base_filename and not base_filename.endswith('.png'):
            code = code.replace('output.png', f'{base_filename}.png')
        elif output_filename != 'output.png':
            code = code.replace('output.png', output_filename)
        
        if 'savefig' not in code and 'save(' not in code:
            code += f"\nplt.savefig('{output_filename}', dpi=300, bbox_inches='tight')"
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # 记录执行前的图片文件
        if base_filename:
            output_pattern = base_filename if os.path.isdir(base_filename) else os.path.dirname(base_filename) or '.'
            before_files = set(glob.glob(os.path.join(output_pattern, '*.png')))
        else:
            before_files = set()
        
        try:
            plt.clf()
            plt.close('all')
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, exec_globals)
            
            result['success'] = True
            result['output'] = stdout_capture.getvalue()
            
            # 检测生成的文件
            if base_filename:
                after_files = set(glob.glob(os.path.join(output_pattern, '*.png')))
                new_files = list(after_files - before_files)
                if new_files:
                    result['output_files'] = sorted(new_files)
                    result['output_file'] = new_files[0] if len(new_files) == 1 else None
                else:
                    result['output_file'] = output_filename
            else:
                result['output_file'] = output_filename
            
            plt.close('all')
            
        except Exception as e:
            result['success'] = False
            result['error'] = f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}"
            result['output'] = stdout_capture.getvalue()
            plt.close('all')
        
        return result
    
    def execute_combined_visualization(
        self,
        code: str,
        data_dict: Dict[str, pd.DataFrame],
        output_dir: str,
        base_filename: str = "combined"
    ) -> Dict[str, Any]:
        """执行多数据集综合可视化代码"""
        result = {
            'success': False,
            'output': '',
            'error': '',
            'output_file': None,
            'output_files': []
        }
        
        exec_globals = {
            'pd': pd,
            'data_dict': data_dict,
            'np': __import__('numpy'),
            'plt': plt,
            'matplotlib': matplotlib,
            'sns': __import__('seaborn'),
            '__builtins__': __builtins__
        }
        
        # 记录执行前的文件
        before_files = set(glob.glob(os.path.join(output_dir, '*.png')))
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            plt.clf()
            plt.close('all')
            
            # 切换到输出目录以便正确保存文件
            original_dir = os.getcwd()
            os.chdir(output_dir)
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, exec_globals)
            
            os.chdir(original_dir)
            
            result['success'] = True
            result['output'] = stdout_capture.getvalue()
            
            # 检测生成的文件
            after_files = set(glob.glob(os.path.join(output_dir, '*.png')))
            new_files = sorted(list(after_files - before_files))
            
            if new_files:
                result['output_files'] = new_files
                result['output_file'] = new_files[0] if len(new_files) == 1 else None
            else:
                # 如果没有检测到新文件，可能使用了默认名称
                default_output = os.path.join(output_dir, 'output.png')
                if os.path.exists(default_output):
                    result['output_file'] = default_output
            
            plt.close('all')
            
        except Exception as e:
            result['success'] = False
            result['error'] = f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}"
            result['output'] = stdout_capture.getvalue()
            plt.close('all')
            try:
                os.chdir(original_dir)
            except:
                pass
        
        return result
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """验证代码语法"""
        result = {'valid': False, 'error': ''}
        try:
            compile(code, '<string>', 'exec')
            result['valid'] = True
        except SyntaxError as e:
            result['error'] = f"语法错误: {str(e)}"
        except Exception as e:
            result['error'] = f"编译错误: {str(e)}"
        return result
