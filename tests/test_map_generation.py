#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
from src.map_generator import draw_china_map, draw_8000km_range_map

class TestMapGeneration(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_output_dir = "tests/outputs"
        os.makedirs(self.test_output_dir, exist_ok=True)
        
    def tearDown(self):
        """测试后的清理工作"""
        # 可选：删除测试生成的文件
        # 注意：为了保留测试结果以便检查，这里不自动删除
        print(f"测试生成的文件保存在: {self.test_output_dir}")
    
    def test_china_map_generation(self):
        """测试中国地图生成功能"""
        try:
            files = draw_china_map(
                output_dir=self.test_output_dir,
                filename_prefix="test_china_map",
                show_map=False  # 不显示地图，仅保存文件
            )
            
            # 检查文件是否生成成功
            for file_path in files:
                self.assertTrue(os.path.exists(file_path), f"文件未生成: {file_path}")
                print(f"中国地图测试文件已生成: {file_path}")
        except Exception as e:
            self.fail(f"中国地图生成失败: {e}")
    
    def test_range_map_generation(self):
        """测试8000公里范围地图生成功能"""
        try:
            files = draw_8000km_range_map(
                radius_km=5000,  # 使用较小的半径进行测试
                output_dir=self.test_output_dir,
                filename_prefix="test_range_map",
                show_map=False  # 不显示地图，仅保存文件
            )
            
            # 检查文件是否生成成功
            for file_path in files:
                self.assertTrue(os.path.exists(file_path), f"文件未生成: {file_path}")
                print(f"范围地图测试文件已生成: {file_path}")
        except Exception as e:
            self.fail(f"范围地图生成失败: {e}")

if __name__ == '__main__':
    unittest.main()