#!/bin/bash

# 运行编译后的中国地图生成器程序

# 定义程序路径
PROGRAM_PATH="dist/macos/china_map_generator"

# 检查程序是否存在
if [ -f "$PROGRAM_PATH" ]; then
    echo "正在运行中国地图生成器程序..."
    "$PROGRAM_PATH"
else
    echo "错误：编译后的程序不存在！"
    echo "请先执行 'make build-macos' 命令编译程序。"
    exit 1
fi