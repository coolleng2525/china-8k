# 中国地图生成器

一个用于生成中国地图和以中国边界为起点的8000公里范围地图的Python应用程序。

## 功能特点

- 生成包含省界和主要城市的中国地图
- 生成以中国边界为起点的8000公里范围地图，标记范围内的国家
- 支持SVG和PNG两种输出格式
- 自动下载中国地图JSON数据（来自GitHub仓库）
- 支持中英文双语显示

## 目录结构

```
china_8k/
├── src/                  # 源代码目录
│   ├── map_generator/    # 地图生成模块
│   ├── data_handler/     # 数据处理模块
│   └── utils/            # 工具函数模块
├── data/                 # 数据存储目录（自动创建）
├── outputs/              # 输出文件目录（自动创建）
├── tests/                # 测试代码目录
├── scripts/              # 辅助脚本目录
├── main.py               # 主程序入口
├── setup.py              # 安装配置文件
├── requirements.txt      # 依赖包列表
└── README.md             # 项目说明文档
```

## 安装指南

### 1. 克隆仓库（如果适用）

```bash
git clone <repository-url>
cd china_8k
```

### 2. 使用Makefile管理项目

本项目提供了一个功能完善的Makefile，可以帮助您在虚拟环境中管理和构建项目。

#### 创建虚拟环境

```bash
make venv
```

#### 激活虚拟环境

```bash
# 先查看激活命令
make activate
# 然后根据提示手动执行激活命令
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\\Scripts\\activate
```

#### 安装项目依赖

```bash
make install-deps
```

#### 安装PyInstaller（用于构建可执行文件）

```bash
make install-pyinstaller
```

## 使用方法

### 生成中国地图

```bash
python main.py china
```

可选参数：
- `--output-dir`: 指定输出目录（默认: outputs）
- `--filename`: 指定输出文件名前缀（默认: china_map）
- `--no-show`: 不显示地图，仅保存文件

### 生成8000公里范围地图

```bash
python main.py range
```

可选参数：
- `--radius`: 指定范围半径（公里，默认: 8000）
- `--output-dir`: 指定输出目录（默认: outputs）
- `--filename`: 指定输出文件名前缀（默认: china_8000km_range）
- `--no-show`: 不显示地图，仅保存文件

### 下载中国地图数据

```bash
python main.py download
```

可选参数：
- `--force`: 强制重新下载数据，即使本地已有
- `--output-path`: 指定数据保存路径（默认: data/china.json）

### 生成中国地图（使用自定义数据文件）

```bash
python main.py china --data-path path/to/your/china.json
```

## 依赖包

- numpy: 数值计算库
- matplotlib: 绘图库
- cartopy: 地图投影库（可选，用于高级地图功能）

## 注意事项

1. 首次运行时，程序会从GitHub下载中国地图的JSON数据，请确保网络连接正常
2. 如果无法下载在线数据，程序会使用内置的简化中国边界数据
3. 为了正确显示中文，请确保您的系统安装了中文字体

### 3. 构建可执行文件

使用Makefile可以轻松构建适用于不同平台的可执行文件：

#### 构建macOS平台可执行文件

```bash
make build-macos
```

生成的可执行文件将位于 `dist/macos/` 目录中。

#### 构建Windows平台可执行文件

在Windows系统上：

```bash
make build-windows
```

在macOS/Linux系统上（需要安装wine）：

```bash
make build-windows-with-wine
```

生成的可执行文件将位于 `dist/windows/` 目录中。

### 4. 运行测试

```bash
make test
```

### 5. 清理构建文件

```bash
make clean
```

## 免责声明

本程序生成的地图仅供参考，地图边界和范围的准确性取决于使用的数据来源。