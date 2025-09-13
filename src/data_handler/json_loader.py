#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import urllib.request
import os
from src.utils.config_loader import config_loader  # 导入配置加载器

# 初始化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从配置中加载路径和URL设置
download_config = config_loader.get('download', {})
LOCAL_JSON_PATH = download_config.get('china_data_path', 'data/china.json')
# 中国地图JSON数据的GitHub URL
CHINA_JSON_URL = "https://raw.githubusercontent.com/echarts-maps/echarts-china-provinces-js/master/echarts-china-provinces-js/data/china.json"

def load_china_map_data(data_path=None):
    """
    加载中国地图的JSON数据
    
    首先尝试从本地加载，如果不存在则从GitHub下载
    如果下载失败，返回简化的中国边界数据
    
    参数:
        data_path: 数据文件路径，默认为LOCAL_JSON_PATH
    
    返回:
        JSON格式的地图数据
    """
    # 使用传入的路径或默认路径
    load_path = data_path if data_path else LOCAL_JSON_PATH
    
    # 首先尝试从本地加载
    if os.path.exists(load_path):
        logger.info(f"从本地加载中国地图数据: {load_path}")
        try:
            with open(load_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug("中国各省份名称列表:")
                    for idx, feature in enumerate(data['features'], 1):
                        province_name = feature['properties'].get('name')
                        if province_name:
                            logger.debug(f"{idx}. {province_name}")
                return data
        except Exception as e:
            logger.error(f"本地加载失败: {e}", exc_info=True)
            return download_china_map_data(output_path=load_path)
    else:
        # 本地文件不存在，尝试下载
        logger.warning(f"本地文件不存在: {load_path}")
        return download_china_map_data(output_path=load_path)

def download_china_map_data(output_path=None):
    """
    从GitHub下载中国地图JSON数据
    
    参数:
        output_path: 数据保存路径，默认为LOCAL_JSON_PATH
    
    返回:
        JSON格式的地图数据
    """
    # 使用传入的路径或默认路径
    save_path = output_path if output_path else LOCAL_JSON_PATH
    logger.info(f"正在从GitHub下载中国地图数据到: {save_path}...")
    try:
        # 确保保存目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 下载JSON文件
        urllib.request.urlretrieve(CHINA_JSON_URL, save_path)
        logger.info(f"中国地图数据下载完成，已保存到: {save_path}")
        
        # 读取下载的JSON数据
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 打印省份名称列表（仅在DEBUG级别）
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("中国各省份名称列表:")
                for idx, feature in enumerate(data['features'], 1):
                    province_name = feature['properties'].get('name')
                    if province_name:
                        logger.debug(f"{idx}. {province_name}")
            
            return data
    except Exception as e:
        logger.error(f"下载中国地图数据时出错: {e}", exc_info=True)
        # 如果下载失败，返回简化的中国边界数据
        return get_simplified_china_boundary()

def get_simplified_china_boundary():
    """
    获取简化的中国边界数据
    
    返回:
        简化的中国边界JSON数据
    """
    logger.warning("使用简化的中国边界数据")
    return {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [73.5, 53.5], [135.1, 53.5], [135.1, 18.2], [73.5, 18.2], [73.5, 53.5]
                ]]
            },
            "properties": {"name": "中国"}
        }]
    }