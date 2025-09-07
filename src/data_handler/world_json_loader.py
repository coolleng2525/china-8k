#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
import os
import time
from src.utils.config_loader import config_loader


def load_world_map_data(data_path=None, force_download=False):
    """
    加载世界地图的JSON数据
    
    首先尝试从本地加载，如果不存在或格式错误则从网络下载
    如果下载失败，返回增强的简化世界边界数据
    
    参数:
        data_path: 数据文件路径
        force_download: 是否强制下载数据，即使本地文件已存在
    
    返回:
        JSON格式的地图数据
    """
    # 从配置文件获取设置
    world_config = config_loader.get('world', {})
    WORLD_JSON_URL = world_config.get('json_urls', {}).get('primary', 
        'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
    ALTERNATIVE_WORLD_JSON_URL = world_config.get('json_urls', {}).get('alternative', 
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
    LOCAL_JSON_PATH = world_config.get('local_path', 'data/world.json')
    
    # 使用传入的路径或配置文件中的路径或默认路径
    load_path = data_path if data_path else LOCAL_JSON_PATH
    
    # 首先尝试从本地加载
    if os.path.exists(load_path) and not force_download:
        print(f"正在从本地加载世界地图数据: {load_path}...")
        try:
            with open(load_path, 'r', encoding='utf-8') as f:
                # 验证JSON格式是否正确
                data = json.load(f)
                if 'features' in data:
                    return data
                elif 'objects' in data and 'countries' in data['objects']:  # 处理备用数据源格式
                    return transform_alt_data_format(data)
                else:
                    print(f"本地JSON文件格式不完整，缺少必要字段")
        except json.JSONDecodeError as e:
            print(f"本地加载世界地图数据失败: 格式错误 - {e}")
            # 删除损坏的文件
            try:
                os.remove(load_path)
                print(f"已删除损坏的文件: {load_path}")
            except Exception as e:
                print(f"无法删除损坏的文件: {e}")
        except Exception as e:
            print(f"本地加载世界地图数据失败: {e}")
    else:
        if force_download:
            print(f"强制重新下载世界地图数据，忽略已存在的本地文件: {load_path}")
        else:
            print(f"本地文件不存在: {load_path}")
    
    # 尝试从两个不同的数据源下载数据
    for url in [WORLD_JSON_URL, ALTERNATIVE_WORLD_JSON_URL]:
        print(f"尝试从数据源: {url}")
        if download_and_verify_data(url, load_path):
            try:
                with open(load_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'objects' in data and 'countries' in data['objects']:
                        return transform_alt_data_format(data)
                    return data
            except Exception as e:
                print(f"读取下载的文件时出错: {e}")
                continue
    
    # 所有尝试都失败，返回增强的简化世界边界数据
    print("所有数据源都失败，使用增强的简化世界边界数据")
    return get_enhanced_simplified_world_boundary()


def download_and_verify_data(url, save_path):
    """
    下载并验证世界地图数据
    如果文件已存在，先创建备份
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"正在从网络下载世界地图数据（尝试 {attempt+1}/{max_retries}）到: {save_path}...")
            # 确保保存目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 检查文件是否已存在，如果存在则创建备份
            if os.path.exists(save_path):
                backup_path = f"{save_path}.bak"
                # 如果备份文件已存在，删除它
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                # 创建新的备份文件
                os.rename(save_path, backup_path)
                print(f"已将已存在的文件备份为: {backup_path}")
            
            # 设置超时时间为30秒
            response = urllib.request.urlopen(url, timeout=30)
            data = response.read().decode('utf-8')
            
            # 简单验证JSON数据格式
            json_data = json.loads(data)
            if 'features' in json_data or ('objects' in json_data and 'countries' in json_data['objects']):
                # 保存到本地
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(data)
                print(f"世界地图数据下载完成，已保存到: {save_path}")
                return True
            else:
                print("下载的JSON数据格式不完整，缺少必要字段")
        except urllib.error.URLError as e:
            print(f"网络请求错误: {e}")
        except json.JSONDecodeError as e:
            print(f"下载的文件格式错误: {e}")
        except Exception as e:
            print(f"下载过程中发生错误: {e}")
        
        # 如果不是最后一次尝试，等待一段时间后重试
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 指数退避策略
            print(f"{wait_time}秒后重试...")
            time.sleep(wait_time)
    
    return False


def transform_alt_data_format(alt_data):
    """
    转换备用数据源的格式为标准格式
    """
    try:
        from pyproj import Proj, transform
        # 提取国家数据并转换格式
        features = []
        countries = alt_data['objects']['countries']
        for i, geom in enumerate(countries['geometries']):
            feature = {
                "type": "Feature",
                "geometry": geom['coordinates'],
                "properties": {"name": f"Country_{i}", "name_en": f"Country_{i}"}
            }
            features.append(feature)
        
        return {"type": "FeatureCollection", "features": features}
    except Exception as e:
        print(f"转换数据格式时出错: {e}")
        # 如果转换失败，返回简化数据
        return get_enhanced_simplified_world_boundary()


def get_enhanced_simplified_world_boundary():
    """
    获取增强的简化世界边界数据
    包含更多国家和地区的简化边界
    """
    # 增强的世界主要国家和地区边界数据
    simplified_countries = {
        "type": "FeatureCollection",
        "features": [
            # 中国
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [73.5, 53.5], [135.1, 53.5], [135.1, 18.2], [73.5, 18.2], [73.5, 53.5]
                    ]]
                },
                "properties": {"name": "中国", "name_en": "China"}
            },
            # 美国
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-124.8, 49.4], [-66.9, 49.4], [-66.9, 25.8], [-124.8, 25.8], [-124.8, 49.4]
                    ]]
                },
                "properties": {"name": "美国", "name_en": "United States"}
            },
            # 俄罗斯
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [27.0, 70.0], [180.0, 70.0], [180.0, 45.0], [27.0, 45.0], [27.0, 70.0]
                    ]]
                },
                "properties": {"name": "俄罗斯", "name_en": "Russia"}
            },
            # 印度
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [68.0, 35.0], [97.0, 35.0], [97.0, 8.0], [68.0, 8.0], [68.0, 35.0]
                    ]]
                },
                "properties": {"name": "印度", "name_en": "India"}
            },
            # 澳大利亚
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [113.0, -10.0], [153.0, -10.0], [153.0, -43.0], [113.0, -43.0], [113.0, -10.0]
                    ]]
                },
                "properties": {"name": "澳大利亚", "name_en": "Australia"}
            },
            # 欧洲
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-10.0, 71.0], [40.0, 71.0], [40.0, 35.0], [-10.0, 35.0], [-10.0, 71.0]
                    ]]
                },
                "properties": {"name": "欧洲", "name_en": "Europe"}
            },
            # 非洲
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-25.0, 37.0], [52.0, 37.0], [52.0, -35.0], [-25.0, -35.0], [-25.0, 37.0]
                    ]]
                },
                "properties": {"name": "非洲", "name_en": "Africa"}
            },
            # 南美洲
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-82.0, 12.0], [-34.0, 12.0], [-34.0, -55.0], [-82.0, -55.0], [-82.0, 12.0]
                    ]]
                },
                "properties": {"name": "南美洲", "name_en": "South America"}
            },
            # 东南亚
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [95.0, 20.0], [140.0, 20.0], [140.0, -10.0], [95.0, -10.0], [95.0, 20.0]
                    ]]
                },
                "properties": {"name": "东南亚", "name_en": "Southeast Asia"}
            },
            # 中东
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [30.0, 40.0], [60.0, 40.0], [60.0, 10.0], [30.0, 10.0], [30.0, 40.0]
                    ]]
                },
                "properties": {"name": "中东", "name_en": "Middle East"}
            }
        ]
    }
    
    return simplified_countries


if __name__ == "__main__":
    # 测试函数
    data = load_world_map_data()
    print(f"加载的地图数据包含 {len(data.get('features', []))} 个地理特征")