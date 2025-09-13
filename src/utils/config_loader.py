#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    配置加载器类，负责加载和管理配置文件
    """
    
    # 默认配置文件路径
    DEFAULT_CONFIG_PATH = 'config.json'
    
    def __init__(self, config_path=None):
        """
        初始化配置加载器
        
        参数:
            config_path: 配置文件路径，默认为DEFAULT_CONFIG_PATH
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
    
    def _load_config(self):
        """
        从文件加载配置
        
        返回:
            配置字典
        """
        # 如果配置文件不存在，返回默认配置
        if not os.path.exists(self.config_path):
            logger.warning(f"配置文件不存在: {self.config_path}，使用默认配置")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self):
        """
        获取默认配置
        
        返回:
            默认配置字典
        """
        return {
            "global": {
                "output_dir": "outputs",
                "show_map": True,
                "data_dir": "data",
                "log_level": "info"
            },
            "china": {
                "filename": "china_map",
                "data_path": None
            },
            "range": {
                "radius": 8000,
                "filename": "china_8000km_range"
            },
            "download": {
                "china_data_path": "data/china.json"
            },
            "world": {
                "filename": "world_map",
                "data_path": None,
                "json_urls": {
                    "primary": "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
                    "alternative": "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"
                },
                "local_path": "data/world.json"
            }
        }
    
    def get(self, section, default=None):
        """
        获取指定部分的配置
        
        参数:
            section: 配置部分名称
            default: 默认值
        
        返回:
            配置值或默认值
        """
        return self.config.get(section, default)
    
    def merge_with_args(self, args, section):
        """
        合并配置和命令行参数
        
        参数:
            args: 命令行参数对象
            section: 配置部分名称
        
        返回:
            合并后的参数字典
        """
        # 获取全局配置
        merged = self.config.get("global", {}).copy()
        
        # 获取指定部分的配置
        section_config = self.config.get(section, {})
        merged.update(section_config)
        
        # 处理命令行参数
        args_dict = vars(args)
        
        # 特殊处理show_map参数（对应no-show标志）
        if 'no_show' in args_dict and args_dict['no_show']:
            merged['show_map'] = False
        
        # 合并其他参数，优先使用命令行参数
        for key, value in args_dict.items():
            # 跳过命令和配置相关的参数
            if key in ['command', 'config', 'generate_config', 'no_show']:
                continue
            # 如果命令行参数不为None，则使用命令行参数
            if value is not None:
                # 转换参数名格式（例如 output_dir -> output-dir）
                config_key = key.replace('_', '-')
                # 但在merged字典中使用下划线格式
                merged[key] = value
        
        return merged
    
    def generate_default_config(self):
        """
        生成默认配置文件
        """
        try:
            # 确保配置文件所在目录存在
            os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
            
            # 写入默认配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._get_default_config(), f, ensure_ascii=False, indent=2)
            
            print(f"默认配置文件已生成: {self.config_path}")
            return True
        except Exception as e:
            print(f"生成默认配置文件失败: {e}")
            return False


# 创建一个全局配置加载器实例
config_loader = ConfigLoader()