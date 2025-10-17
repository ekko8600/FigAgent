"""配置管理模块"""
from pathlib import Path


class ConfigManager:
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = Path(__file__).parent / "config.py"
        self.config_file = Path(config_file)
    
    def get_api_key(self) -> str:
        """获取API密钥"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.split('\n'):
                    if 'DEEPSEEK_API_KEY' in line and '=' in line:
                        key = line.split('=')[1].strip().strip('"').strip("'")
                        if key and key != "your-api-key-here":
                            return key
        except:
            pass
        return ""
    
    def save_api_key(self, api_key: str):
        """保存API密钥到配置文件"""
        content = f'DEEPSEEK_API_KEY = "{api_key}"\n'
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def prompt_for_api_key(self) -> str:
        """提示用户输入API密钥"""
        existing_key = self.get_api_key()
        
        if existing_key:
            print(f"\n当前API密钥: {existing_key[:10]}...{existing_key[-4:]}")
            use_existing = input("是否使用现有密钥? (Y/n): ").strip().lower()
            if use_existing != 'n':
                return existing_key
        
        print("\n请输入你的DeepSeek API密钥:")
        print("(可在 https://www.deepseek.com 获取)")
        api_key = input("> ").strip()
        
        if api_key:
            self.save_api_key(api_key)
            print("✓ API密钥已保存")
            return api_key
        
        return existing_key

