#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def run_demo():
    """
    运行地图生成器的演示
    """
    print("===== 中国地图生成器演示 ======")
    print("这个脚本将演示地图生成器的基本功能")
    print("\n1. 生成中国地图")
    
    try:
        # 运行中国地图生成
        os.system(f"{sys.executable} main.py china --no-show")
        print("\n2. 生成8000公里范围地图")
        
        # 运行8000公里范围地图生成
        os.system(f"{sys.executable} main.py range --no-show")
        
        print("\n===== 演示完成 =====")
        print("\n生成的文件:")
        
        # 显示生成的文件
        if os.path.exists("outputs"):
            output_files = os.listdir("outputs")
            for file in output_files:
                print(f"- outputs/{file}")
        
        print("\n使用方法:")
        print("- 生成中国地图: python main.py china")
        print("- 生成8000公里范围地图: python main.py range")
        print("\n查看帮助: python main.py -h")
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_demo()