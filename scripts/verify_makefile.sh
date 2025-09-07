#!/bin/bash

# 验证Makefile功能的脚本

# 显示帮助信息
make help

# 检查当前是否有虚拟环境
if [ -d "venv" ]; then
  echo "\n发现已存在的虚拟环境，跳过创建步骤..."
  echo "如果需要重新创建虚拟环境，请先运行 'make clean' 然后再运行 'make venv'"
else
  echo "\n虚拟环境不存在，将显示创建虚拟环境的命令..."
  echo "要实际创建虚拟环境，请运行：make venv"
fi

# 显示如何激活虚拟环境
echo "\n激活虚拟环境的命令："
make activate

# 显示构建命令
echo "\n构建命令："
echo "- 构建macOS可执行文件: make build-macos"
echo "- 构建Windows可执行文件: make build-windows (在Windows上)"
echo "- 构建Windows可执行文件(使用wine): make build-windows-with-wine"
echo "- 运行测试: make test"
echo "- 清理构建文件: make clean"

# 标记脚本为可执行文件
chmod +x $0