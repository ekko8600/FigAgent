import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Union


class DataAnalyzer:
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.parquet', '.txt']
    
    def scan_directory(self, directory: str) -> List[str]:
        """扫描目录下所有支持的数据文件"""
        dir_path = Path(directory)
        if not dir_path.is_dir():
            return []
        
        files = []
        for ext in self.supported_formats:
            files.extend([str(f) for f in dir_path.rglob(f'*{ext}')])
        return sorted(files)
    
    def resolve_paths(self, paths: List[str]) -> List[str]:
        """解析路径，支持文件和文件夹混合输入"""
        resolved = []
        for path_str in paths:
            path = Path(path_str)
            if path.is_dir():
                resolved.extend(self.scan_directory(path_str))
            elif path.is_file():
                resolved.append(str(path))
        return resolved
    
    def read_data(self, file_path: str) -> pd.DataFrame:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.csv':
            try:
                return pd.read_csv(file_path)
            except:
                try:
                    return pd.read_csv(file_path, sep='\t')
                except:
                    return pd.read_csv(file_path, sep=';')
        elif suffix in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif suffix == '.json':
            return pd.read_json(file_path)
        elif suffix == '.parquet':
            return pd.read_parquet(file_path)
        elif suffix == '.txt':
            try:
                return pd.read_csv(file_path, sep='\t')
            except:
                try:
                    return pd.read_csv(file_path, sep=',')
                except:
                    return pd.read_csv(file_path, sep='\s+')
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        analysis = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_columns': [],
            'categorical_columns': [],
            'datetime_columns': [],
            'statistics': {},
            'sample_data': df.head(3).to_dict('records')
        }
        
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                analysis['numeric_columns'].append(col)
                analysis['statistics'][col] = {
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None
                }
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                analysis['datetime_columns'].append(col)
            else:
                analysis['categorical_columns'].append(col)
                unique_count = df[col].nunique()
                analysis['statistics'][col] = {
                    'unique_count': int(unique_count),
                    'top_values': df[col].value_counts().head(5).to_dict()
                }
        
        return analysis
    
    def analyze_multiple_files(self, file_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        results = {}
        for file_path in file_paths:
            try:
                df = self.read_data(file_path)
                analysis = self.analyze_dataframe(df)
                results[file_path] = {
                    'success': True,
                    'data': df,
                    'analysis': analysis
                }
            except Exception as e:
                results[file_path] = {
                    'success': False,
                    'error': str(e)
                }
        return results
    
    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        summary = []
        summary.append(f"数据集形状: {analysis['shape'][0]}行 × {analysis['shape'][1]}列")
        summary.append(f"\n列名: {', '.join(analysis['columns'])}")
        
        if analysis['numeric_columns']:
            summary.append(f"\n数值列 ({len(analysis['numeric_columns'])}): {', '.join(analysis['numeric_columns'])}")
        
        if analysis['categorical_columns']:
            summary.append(f"\n分类列 ({len(analysis['categorical_columns'])}): {', '.join(analysis['categorical_columns'])}")
        
        if analysis['datetime_columns']:
            summary.append(f"\n时间列 ({len(analysis['datetime_columns'])}): {', '.join(analysis['datetime_columns'])}")
        
        missing = {k: v for k, v in analysis['missing_values'].items() if v > 0}
        if missing:
            summary.append(f"\n缺失值: {missing}")
        
        return '\n'.join(summary)

