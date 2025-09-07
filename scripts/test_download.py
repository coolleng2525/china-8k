#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

# 确保我们可以导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_handler.json_loader import download_china_map_data, load_china_map_data


def test_download_functionality():
    """
    测试地图数据下载功能
    """
    print("=== 测试地图数据下载功能 ===")
    
    # 测试1: 使用默认路径下载
    print("\n测试1: 使用默认路径下载数据")
    try:
        data = download_china_map_data()
        print(f"✓ 成功下载数据，包含 {len(data.get('features', []))} 个地理特征")
        
        # 验证数据文件是否存在
        default_path = "data/china.json"
        if os.path.exists(default_path):
            print(f"✓ 数据文件已保存到: {default_path}")
            # 验证文件内容
            with open(default_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                if len(loaded_data.get('features', [])) > 0:
                    print("✓ 文件内容有效")
    except Exception as e:
        print(f"✗ 测试1失败: {e}")
    
    # 测试2: 使用自定义路径下载
    print("\n测试2: 使用自定义路径下载数据")
    custom_path = "data/test_custom_china.json"
    try:
        # 先删除可能存在的文件
        if os.path.exists(custom_path):
            os.remove(custom_path)
            print(f"已删除旧的测试文件: {custom_path}")
            
        data = download_china_map_data(output_path=custom_path)
        print(f"✓ 成功下载数据到自定义路径，包含 {len(data.get('features', []))} 个地理特征")
        
        # 验证文件是否存在
        if os.path.exists(custom_path):
            print(f"✓ 数据文件已保存到: {custom_path}")
            # 清理测试文件
            os.remove(custom_path)
            print(f"✓ 已清理测试文件: {custom_path}")
    except Exception as e:
        print(f"✗ 测试2失败: {e}")
    
    # 测试3: 使用load函数加载数据
    print("\n测试3: 使用load函数加载数据")
    try:
        data = load_china_map_data()
        print(f"✓ 成功加载数据，包含 {len(data.get('features', []))} 个地理特征")
    except Exception as e:
        print(f"✗ 测试3失败: {e}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_download_functionality()