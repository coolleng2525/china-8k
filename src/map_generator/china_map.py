import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from src.data_handler.json_loader import load_china_map_data
from src.utils.font_config import setup_fonts
import logging

# 设置中文字体
font_set = setup_fonts()

# 中国主要城市数据
MAJOR_CITIES = [
    {"name": "北京", "lat": 39.9, "lon": 116.4},
    {"name": "上海", "lat": 31.2, "lon": 121.4},
    {"name": "广州", "lat": 23.1, "lon": 113.2},
    {"name": "深圳", "lat": 22.5, "lon": 114.1},
    {"name": "成都", "lat": 30.6, "lon": 104.0},
    {"name": "武汉", "lat": 30.5, "lon": 114.3},
    {"name": "西安", "lat": 34.3, "lon": 108.9},
    {"name": "重庆", "lat": 29.5, "lon": 106.5},
    {"name": "天津", "lat": 39.3, "lon": 117.2},
    {"name": "杭州", "lat": 30.2, "lon": 120.1},
    {"name": "南京", "lat": 32.0, "lon": 118.7},
    {"name": "哈尔滨", "lat": 45.8, "lon": 126.7},
    {"name": "长春", "lat": 43.8, "lon": 125.3},
    {"name": "沈阳", "lat": 41.8, "lon": 123.4},
    {"name": "昆明", "lat": 25.0, "lon": 102.7},
    {"name": "贵阳", "lat": 26.5, "lon": 106.7},
    {"name": "拉萨", "lat": 29.6, "lon": 91.1},
    {"name": "乌鲁木齐", "lat": 43.8, "lon": 87.6},
    {"name": "兰州", "lat": 36.0, "lon": 103.8},
    {"name": "西宁", "lat": 36.6, "lon": 101.8}
]

# 初始化日志
logger = logging.getLogger(__name__)

def draw_china_map(output_dir="outputs", filename_prefix="china_map", show_map=True, data_path=None):
    """
    绘制中国地图，包括省界和主要城市
    
    参数:
        output_dir: 输出文件目录
        filename_prefix: 输出文件名前缀
        show_map: 是否显示地图
        data_path: 地图数据文件路径，默认为None（使用默认路径）
    
    返回:
        生成的文件路径列表
    """
    # 创建图形和坐标轴
    plt.figure(figsize=(12, 10), dpi=150)
    ax = plt.axes()
    
    # 设置地图范围
    ax.set_xlim(70, 140)
    ax.set_ylim(15, 55)
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 获取中国地图数据
    china_data = load_china_map_data(data_path=data_path)
    
    # 存储所有省份的多边形
    patches = []
    
    # 颜色列表，用于不同省份
    colors = plt.cm.tab20(np.linspace(0, 1, 34))  # 假设中国有34个省级行政区
    
    # 遍历JSON数据中的每个特征
    for i, feature in enumerate(china_data['features']):
        geometry = feature['geometry']
        
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
    
    # 创建多边形集合并添加到图形
    p = PatchCollection(patches, alpha=0.6)
    p.set_color(colors[0 % len(colors)])  # 使用统一的颜色
    ax.add_collection(p)
    
    print(f"正在绘制主要城市... number of cities: {len(MAJOR_CITIES)}")
    # 绘制主要城市
    for city in MAJOR_CITIES:
        ax.plot(city['lon'], city['lat'], 'ro', markersize=6)
        if font_set and len(MAJOR_CITIES) <= 20:  # 城市数量不多时才添加标签，避免拥挤
            print(f"正在绘制城市: {city['name']}")
            ax.text(city['lon'] + 0.5, city['lat'] + 0.3, city['name'], fontsize=9)
    
    # 设置标题和标签
    if font_set:
        plt.title('中国地图', fontsize=16)
        plt.xlabel('经度', fontsize=12)
        plt.ylabel('纬度', fontsize=12)
    else:
        plt.title('China Map', fontsize=16)
        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Latitude', fontsize=12)
    
    # 调整布局
    plt.tight_layout()
    
    # 确保输出目录存在
    import os
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


def generate_china_map():
    try:
        logger.info("开始生成中国地图")
        
        # 替换原来的print语句
        logger.debug(f"加载的省份数量: {len(provinces)}")
        
        # 错误处理示例
        if not provinces:
            logger.warning("未加载到任何省份数据")
            
    except Exception as e:
        logger.error("生成中国地图时发生错误", exc_info=True)
        raise