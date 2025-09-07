# Makefile for China Map Generator

# 项目名称和版本
PROJECT_NAME = china_map_generator
VERSION = 0.1.0

# 项目配置
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
BUILD_DIR = build
DIST_DIR = dist
PYINSTALLER = $(VENV_DIR)/bin/pyinstaller
PYI_FLAGS = --name china_map_generator --onefile --windowed

# 创建虚拟环境
venv: check-venv
	@echo "虚拟环境已存在，如需重新创建，请先执行 'make clean'"

check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		@echo "虚拟环境已创建，请执行 'source $(VENV_DIR)/bin/activate' 激活虚拟环境"; \
	fi

# 显示激活虚拟环境的命令
activate:
	@echo "请执行以下命令激活虚拟环境："
	@echo "source $(VENV_DIR)/bin/activate"

# 安装项目依赖
install-deps: check-venv
	$(PIP) install --default-timeout=100 -r requirements.txt

# 安装PyInstaller
install-pyinstaller: check-venv
	$(PIP) install --default-timeout=100 pyinstaller

# 构建macOS平台可执行文件
build-macos: check-venv install-deps install-pyinstaller
	$(PYINSTALLER) $(PYI_FLAGS) --distpath $(DIST_DIR)/macos main.py
	@echo "macOS可执行文件已生成在 $(DIST_DIR)/macos/ 目录中"

# 构建Windows平台可执行文件（在macOS上使用wine或在Windows上直接运行）
build-windows: check-venv install-deps install-pyinstaller
	@echo "注意：在Windows上运行此目标以构建Windows可执行文件"
	@echo "或者在macOS/Linux上安装wine后运行：make build-windows-with-wine"

# 在macOS/Linux上使用wine构建Windows可执行文件
build-windows-with-wine:
	@echo "确保已安装wine和pyinstaller（wine环境中）"
	wine $(PYTHON) -m PyInstaller $(PYI_FLAGS) --distpath $(DIST_DIR)/windows --target-arch=win32 main.py
	@echo "Windows可执行文件已生成在 $(DIST_DIR)/windows/ 目录中（如果构建成功）"

# 运行测试
test: check-venv
	$(PYTHON) -m unittest discover -s tests

# 清理构建文件
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) __pycache__ *.spec
	find . -name "*.pyc" -delete
	@echo "构建文件已清理"

# 生成世界各国分界图
world-map: check-venv install-deps
	$(PYTHON) main.py world
	@echo "世界各国分界图已生成在 outputs/ 目录中"

# 生成世界地图上的中国8000公里范围图
world-range: check-venv install-deps
	$(PYTHON) main.py world-range
	@echo "世界地图上的中国8000公里范围图已生成在 outputs/ 目录中"

# 帮助信息
# 在help目标中添加新命令的说明
help:
	@echo "可用目标："
	@echo "  venv          : 创建虚拟环境"
	@echo "  activate      : 显示激活虚拟环境的命令"
	@echo "  install-deps  : 在虚拟环境中安装项目依赖"
	@echo "  install-pyinstaller : 在虚拟环境中安装PyInstaller"
	@echo "  build-macos   : 在虚拟环境中构建macOS平台可执行文件"
	@echo "  build-windows : 在虚拟环境中构建Windows平台可执行文件"
	@echo "  test          : 在虚拟环境中运行测试"
	@echo "  clean         : 清理构建文件"
	@echo "  world-map     : 生成世界各国分界图"
	@echo "  world-range   : 生成世界地图上的中国8000公里范围图"

# 伪目标
.PHONY: help venv activate check-venv install-deps install-pyinstaller build-macos build-windows build-windows-with-wine test clean world-map world-range