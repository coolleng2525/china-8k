#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
from src.data_handler.world_json_loader import load_world_map_data
from src.data_handler.json_loader import load_china_map_data
from src.utils.distance_calculator import great_circle_distance
from src.utils.font_config import setup_fonts

# 设置中文字体
font_set = setup_fonts()

# 地球半径（公里）
EARTH_RADIUS = 6371.0

# 中国的主要城市点
china_key_points = [
    (39.9, 116.4),  # 北京
    (31.2, 121.4),  # 上海
    (22.5, 114.1),  # 深圳
    (30.6, 104.0),  # 成都
    (23.1, 113.2),  # 广州
    (34.3, 108.9),  # 西安
    (43.8, 87.6),   # 乌鲁木齐
    (25.0, 102.7),  # 昆明
    (45.8, 126.7),  # 哈尔滨
    (22.1, 113.5)   # 珠海
]

# 世界主要城市数据
WORLD_MAJOR_CITIES = [
    {"name": "北京", "lat": 39.9, "lon": 116.4, "country": "中国"},
    {"name": "纽约", "lat": 40.7, "lon": -74.0, "country": "美国"},
    {"name": "伦敦", "lat": 51.5, "lon": -0.1, "country": "英国"},
    {"name": "东京", "lat": 35.6, "lon": 139.8, "country": "日本"},
    {"name": "巴黎", "lat": 48.8, "lon": 2.3, "country": "法国"},
    {"name": "莫斯科", "lat": 55.7, "lon": 37.6, "country": "俄罗斯"},
    {"name": "新加坡", "lat": 1.3, "lon": 103.8, "country": "新加坡"},
    {"name": "悉尼", "lat": -33.8, "lon": 151.2, "country": "澳大利亚"}
]

def draw_world_map_with_range(radius_km=8000, output_dir="outputs", filename_prefix="world_with_8000km_range", show_map=True, data_path=None):
    """
    绘制世界地图，并在上面叠加显示以中国边界为起点的8000公里范围
    
    参数:
        radius_km: 范围半径（公里）
        output_dir: 输出文件目录
        filename_prefix: 输出文件名前缀
        show_map: 是否显示地图
        data_path: 地图数据文件路径，默认为None（使用默认路径）
    
    返回:
        生成的文件路径列表
    """
    # 创建图形和坐标轴，增加宽度使地图更宽广
    plt.figure(figsize=(25, 10), dpi=150)  # 增加宽度从18到25
    ax = plt.axes()
    
    # 使用标准全球范围，但通过图形比例让中国在视觉上居中
    ax.set_xlim(-180, 180)  # 完整经度范围
    ax.set_ylim(-90, 90)    # 完整纬度范围
    
    # 新代码：设置地图范围以中国为中心，同时包含美洲
    # 中国地理中心约在兰州附近（36°N, 104°E）
    # 进一步扩大显示范围，确保显示美洲大陆
    center_lon = 104  # 中国地理中心经度
    center_lat = 36   # 中国地理中心纬度
    span_lon = 360    # 扩大经度范围至全球（原为280）
    span_lat = 170    # 扩大纬度范围（原为160）
    
    ax.set_xlim(center_lon - span_lon/2, center_lon + span_lon/2)
    ax.set_ylim(center_lat - span_lat/2, center_lat + span_lat/2)
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 获取世界地图数据
    world_data = load_world_map_data(data_path=data_path)
    
    # 获取中国地图数据
    china_data = load_china_map_data()
    
    # 存储所有国家的多边形（不包括中国）
    patches = []
    country_names = []
    
    # 颜色列表，用于不同国家
    colors = plt.cm.tab20(np.linspace(0, 1, 20))
    
    # 遍历JSON数据中的每个特征（不包括中国）
    for i, feature in enumerate(world_data['features']):
        geometry = feature['geometry']
        properties = feature.get('properties', {})
        
        # 获取国家名称
        country_name = properties.get('name', f'Country_{i}')
        # 跳过中国，因为我们将使用专门的中国地图数据
        if country_name in ['中国', 'China', 'CN']:
            continue
        
        country_names.append(country_name)
        
        # 处理多边形
        if geometry['type'] == 'Polygon':
            coordinates = geometry['coordinates']
            for polygon_coords in coordinates:
                # 转换坐标格式 (lon, lat) -> (x, y)
                x, y = zip(*polygon_coords)
                polygon = Polygon(np.column_stack((x, y)), closed=True)
                patches.append(polygon)
        
        # 处理多重多边形
        elif geometry['type'] == 'MultiPolygon':
            coordinates = geometry['coordinates']
            for multi_coords in coordinates:
                for polygon_coords in multi_coords:
                    x, y = zip(*polygon_coords)
                    polygon = Polygon(np.column_stack((x, y)), closed=True)
                    patches.append(polygon)
    
    # 创建多边形集合并添加到图形（其他国家）
    p = PatchCollection(patches, alpha=0.7)
    # 使用循环颜色，确保不同国家有不同颜色
    p.set_color([colors[i % len(colors)] for i in range(len(patches))])
    # 设置边界线颜色和宽度
    p.set_edgecolor('k')
    p.set_linewidth(0.5)
    ax.add_collection(p)
    
    # 现在绘制中国地图数据，使其显示在其他国家之上
    china_patches = []
    # 遍历中国地图数据中的每个特征
    for feature in china_data['features']:
        geometry = feature['geometry']
        
        # 处理多边形
        if geometry['type'] == 'Polygon':
            coordinates = geometry['coordinates']
            for polygon_coords in coordinates:
                # 转换坐标格式 (lon, lat) -> (x, y)
                x, y = zip(*polygon_coords)
                polygon = Polygon(np.column_stack((x, y)), closed=True)
                china_patches.append(polygon)
        
        # 处理多重多边形
        elif geometry['type'] == 'MultiPolygon':
            coordinates = geometry['coordinates']
            for multi_coords in coordinates:
                for polygon_coords in multi_coords:
                    x, y = zip(*polygon_coords)
                    polygon = Polygon(np.column_stack((x, y)), closed=True)
                    china_patches.append(polygon)
    
    # 创建中国多边形集合并添加到图形
    china_p = PatchCollection(china_patches, alpha=0.9)
    # 使用特殊颜色表示中国
    china_p.set_color([0.85, 0.16, 0.16, 0.9])  # 红色系
    china_p.set_edgecolor('k')
    china_p.set_linewidth(0.8)
    ax.add_collection(china_p)
    
    # 绘制8000公里范围
    # 计算中国边界的包围盒
    china_min_lat = min([p[0] for p in china_key_points]) - 5
    china_max_lat = max([p[0] for p in china_key_points]) + 5
    china_min_lon = min([p[1] for p in china_key_points]) - 5
    china_max_lon = max([p[1] for p in china_key_points]) + 5
    
    # 计算从中国边界扩展指定公里的范围
    km_per_degree = 111.0  # 简化计算：1度≈111公里
    radius_degree = radius_km / km_per_degree
    
    # 绘制总的范围边界
    range_boundary = [
        (china_min_lon - radius_degree, china_min_lat - radius_degree),
        (china_max_lon + radius_degree, china_min_lat - radius_degree),
        (china_max_lon + radius_degree, china_max_lat + radius_degree), 
        (china_min_lon - radius_degree, china_max_lat + radius_degree),
        (china_min_lon - radius_degree, china_min_lat - radius_degree)
    ]
    
    # 绘制范围边界
    range_x = [p[0] for p in range_boundary]
    range_y = [p[1] for p in range_boundary]
    ax.plot(range_x, range_y, color='orange', linewidth=2, linestyle='--', label=f'{radius_km}公里范围')
    
    # 在中国主要城市位置绘制范围圆（用于可视化）
    for lat, lon in china_key_points:
        circle = Circle((lon, lat), radius_degree, fill=False, edgecolor='orange', 
                       linestyle='--', linewidth=0.5, alpha=0.5)
        ax.add_patch(circle)
    
    # 绘制主要城市
    for city in WORLD_MAJOR_CITIES:
        ax.plot(city['lon'], city['lat'], 'ro', markersize=6)
        if font_set:
            ax.text(city['lon'] + 2, city['lat'] + 1, f"{city['name']}({city['country']})", 
                   fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
    
    # 添加中国主要城市标记
    for lat, lon in china_key_points:
        ax.plot(lon, lat, 'go', markersize=8, label='中国主要城市')
    
    # 设置标题和标签
    if font_set:
        plt.title(f'世界地图与中国边界{radius_km}公里范围', fontsize=16)
        plt.xlabel('经度', fontsize=12)
        plt.ylabel('纬度', fontsize=12)
    else:
        plt.title(f'World Map with {radius_km}km Range from China Border', fontsize=16)
        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Latitude', fontsize=12)
    
    # 添加图例
    ax.legend(loc='lower right', fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存为SVG和PNG文件
    svg_path = os.path.join(output_dir, f'{filename_prefix}.svg')
    png_path = os.path.join(output_dir, f'{filename_prefix}.png')
    
    plt.savefig(svg_path, format='svg', bbox_inches='tight')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    
    if show_map:
        plt.show()
    else:
        plt.close()
    
    return [svg_path, png_path]