# Windows打包文件说明

## 📁 新增文件一览

为了支持将FigAgent打包成Windows EXE，已添加以下文件：

### 1. 核心文件

| 文件 | 用途 | 必需 |
|------|------|------|
| `fig_agent_main.py` | 程序入口点 | ✅ 是 |
| `FigAgent.spec` | PyInstaller配置文件 | ✅ 是 |
| `build_exe.py` | 自动化构建脚本 | 推荐 |

### 2. 文档文件

| 文件 | 内容 |
|------|------|
| `WINDOWS_BUILD_GUIDE.md` | 详细打包指南（完整版） |
| `BUILD_QUICKSTART.md` | 快速开始（简化版） |
| `PACKAGING_README.md` | 本文件（文件说明） |

### 3. 可选文件

| 文件 | 用途 |
|------|------|
| `setup.py` | cx_Freeze打包配置（替代方案） |

## 🎯 三种打包方式

### 方式1：自动构建（最简单）⭐
```bash
python build_exe.py
```
**优点**：全自动，一键完成  
**输出**：`dist/FigAgent.exe`（单文件）

### 方式2：使用spec文件（可定制）
```bash
pyinstaller FigAgent.spec
```
**优点**：可自定义配置（图标、模块等）  
**输出**：`dist/FigAgent.exe`

### 方式3：使用cx_Freeze（替代方案）
```bash
python setup.py build
```
**优点**：某些情况下更稳定  
**输出**：`build/exe.win-xxx/`文件夹

## 📊 文件关系图

```
打包流程
    ↓
fig_agent_main.py ────→ 程序入口
    ↓
FigAgent.spec ────→ 配置打包参数
    ↓
build_exe.py ────→ 自动化构建
    ↓
dist/FigAgent.exe ────→ 最终产品
```

## 🚀 快速开始

### 第一次打包

```bash
# 1. 安装依赖
pip install -r fig_agent/requirements.txt
pip install pyinstaller

# 2. 构建exe
python build_exe.py

# 3. 测试
cd dist
FigAgent.exe
```

### 后续打包

```bash
# 清理旧文件
python build_exe.py --clean

# 重新构建
python build_exe.py
```

## 📝 自定义配置

### 添加图标

1. 准备图标文件：`icon.ico`
2. 编辑 `FigAgent.spec`：
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # 添加这行
   )
   ```
3. 重新打包：`pyinstaller FigAgent.spec`

### 修改exe名称

编辑 `build_exe.py`：
```python
cmd = [
    "pyinstaller",
    "--name=YourCustomName",  # 修改这里
    ...
]
```

### 添加额外模块

如果遇到 "Module not found" 错误，编辑 `FigAgent.spec`：
```python
hiddenimports = [
    'matplotlib',
    'seaborn',
    'your_missing_module',  # 添加缺失的模块
]
```

## 🔍 文件详解

### `fig_agent_main.py`
- **作用**：程序的真正入口点
- **特性**：
  - 处理打包后的路径问题
  - 设置matplotlib后端
  - 异常处理和友好的错误提示
- **修改**：通常不需要修改

### `FigAgent.spec`
- **作用**：PyInstaller的详细配置
- **关键配置**：
  - `hiddenimports`：隐藏导入的模块
  - `excludes`：排除不需要的模块
  - `icon`：exe图标
  - `console`：是否显示控制台
- **修改**：根据需要自定义

### `build_exe.py`
- **作用**：自动化整个打包流程
- **功能**：
  - 检查和安装PyInstaller
  - 创建入口文件
  - 执行打包命令
  - 显示友好的提示信息
- **参数**：`--clean` 清理构建文件

## ⚙️ 配置对比

### 单文件 vs 多文件

**单文件模式**（默认）：
```python
"--onefile"  # 在 build_exe.py 中
```
- ✅ 优点：只有一个exe，易于分发
- ❌ 缺点：启动稍慢（3-5秒），文件较大

**多文件模式**：
```python
"--onedir"  # 替换 --onefile
```
- ✅ 优点：启动快，体积稍小
- ❌ 缺点：生成文件夹，包含多个文件

### 控制台 vs 无控制台

**有控制台**（默认）：
```python
console=True  # 在 FigAgent.spec 中
```
- ✅ 适合：CLI应用（当前推荐）
- 显示：黑色命令行窗口

**无控制台**：
```python
console=False
```
- ✅ 适合：纯GUI应用
- 隐藏：命令行窗口

## 🐛 常见问题处理

### 问题：打包失败

**症状**：PyInstaller报错
```
ModuleNotFoundError: No module named 'xxx'
```

**解决**：在 `FigAgent.spec` 添加：
```python
hiddenimports = ['xxx']
```

### 问题：exe无法运行

**症状**：双击exe无反应或闪退

**诊断方法**：
```cmd
# 在命令行运行查看错误
FigAgent.exe
```

**常见原因**：
1. 缺少系统库 → 安装 VC++ Redistributable
2. 杀毒软件拦截 → 添加白名单
3. 权限问题 → 以管理员运行

### 问题：文件太大

**正常大小**：100-200 MB

**减小方法**：
1. 使用UPX压缩（可能不稳定）
2. 排除不需要的库
3. 使用多文件模式
4. 使用Nuitka编译（高级）

## 📚 进一步阅读

- **快速开始**：`BUILD_QUICKSTART.md`
- **详细指南**：`WINDOWS_BUILD_GUIDE.md`
- **PyInstaller文档**：https://pyinstaller.org
- **cx_Freeze文档**：https://cx-freeze.readthedocs.io

## 🎁 分发建议

### 最小分发
```
FigAgent.exe
```

### 推荐分发
```
FigAgent_v1.0/
├── FigAgent.exe
├── README.txt
└── sample_data/
    └── example.csv
```

### 完整分发
```
FigAgent_v1.0/
├── FigAgent.exe
├── README.txt
├── 使用指南.pdf
├── sample_data/
│   ├── example1.csv
│   └── example2.xlsx
└── output/  (空文件夹)
```

## ✅ 验证清单

打包完成后，请检查：

- [ ] exe文件存在于 `dist/` 目录
- [ ] 文件大小正常（100-200MB）
- [ ] 在当前机器可以运行
- [ ] 可以加载示例数据
- [ ] 可以生成可视化图表
- [ ] API密钥可以保存
- [ ] 在其他Windows电脑测试（如果可能）

## 🔄 更新流程

当代码更新后：

```bash
# 1. 更新代码
git pull  # 或其他方式

# 2. 清理旧构建
python build_exe.py --clean

# 3. 重新打包
python build_exe.py

# 4. 测试新版本
cd dist
FigAgent.exe

# 5. 分发新版本
```

## 📞 获取帮助

如果遇到问题：

1. **检查文档**
   - `BUILD_QUICKSTART.md` - 快速问题
   - `WINDOWS_BUILD_GUIDE.md` - 详细问题

2. **查看日志**
   - PyInstaller构建日志
   - exe运行时错误信息

3. **常见问题**
   - 模块缺失 → 添加到 `hiddenimports`
   - 杀毒拦截 → 添加白名单
   - 运行库缺失 → 安装 VC++ Redistributable

## 🎯 总结

| 需求 | 文件 | 命令 |
|------|------|------|
| 快速打包 | `build_exe.py` | `python build_exe.py` |
| 自定义打包 | `FigAgent.spec` | `pyinstaller FigAgent.spec` |
| 了解详情 | `WINDOWS_BUILD_GUIDE.md` | - |
| 快速开始 | `BUILD_QUICKSTART.md` | - |

---

**选择适合你的方式，开始打包吧！** 🚀

如果你只是想快速打包，直接运行：
```bash
python build_exe.py
```

就这么简单！✨

