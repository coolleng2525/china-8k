import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import logging
from src.data_handler.country_data import get_countries_data
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

# 配置日志记录器
logger = logging.getLogger(__name__)

# 确保logger至少有一个处理器（如果没有父处理器的话）
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def draw_8000km_range_map(radius_km=8000, output_dir="outputs", filename_prefix="china_8000km_range", show_map=True):
    """
    绘制以中国边界为起点的指定公里范围地图
    
    参数:
        radius_km: 范围半径（公里）
        output_dir: 输出文件目录
        filename_prefix: 输出文件名前缀
        show_map: 是否显示地图
    
    返回:
        生成的文件路径列表
    """
    logger.info(f"开始绘制{radius_km}公里范围地图")
    
    # 创建图形
    plt.figure(figsize=(14, 10), dpi=150)
    ax = plt.axes()

    # 计算中国边界的包围盒
    china_min_lat = min([p[0] for p in china_key_points]) - 5
    china_max_lat = max([p[0] for p in china_key_points]) + 5
    china_min_lon = min([p[1] for p in china_key_points]) - 5
    china_max_lon = max([p[1] for p in china_key_points]) + 5

    # 计算从中国边界扩展指定公里的范围
    km_per_degree = 111.0  # 简化计算：1度≈111公里
    radius_degree = radius_km / km_per_degree
    
    # 根据半径动态调整地图显示范围，确保足够大
    map_margin_degree = max(20, radius_degree * 0.3)  # 额外的边距
    display_min_lon = china_min_lon - radius_degree - map_margin_degree
    display_max_lon = china_max_lon + radius_degree + map_margin_degree
    display_min_lat = china_min_lat - radius_degree - map_margin_degree
    display_max_lat = china_max_lat + radius_degree + map_margin_degree
    
    # 确保经纬度在有效范围内
    display_min_lon = max(-180, display_min_lon)
    display_max_lon = min(180, display_max_lon)
    display_min_lat = max(-85, display_min_lat)  # 不使用-90以避免极坐标问题
    display_max_lat = min(85, display_max_lat)   # 不使用90以避免极坐标问题
    
    # 设置地图范围（经纬度）
    ax.set_xlim(display_min_lon, display_max_lon)
    ax.set_ylim(display_min_lat, display_max_lat)

    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.5)

    # 绘制总的范围边界（改进版：考虑地球曲率的矩形近似）
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
    ax.plot(range_x, range_y, color='orange', linewidth=1.5, linestyle='--', label=f'{radius_km}公里范围')

    # 获取国家数据
    countries = get_countries_data()
    logger.debug(f"获取到{len(countries)}个国家数据")

    # 计算并标注在指定公里范围内的国家
    within_range_countries = []
    beyond_range_countries = []

    for country, (lat, lon) in countries.items():
        # 计算到中国的最短距离（到中国关键点的最小距离）
        min_distance = min([great_circle_distance(lat, lon, c_lat, c_lon) for c_lat, c_lon in china_key_points])
        
        # 判断是否在范围内
        if min_distance <= radius_km:
            within_range_countries.append((country, lat, lon))
        else:
            beyond_range_countries.append((country, lat, lon))

    logger.info(f"{radius_km}公里范围内包含{len(within_range_countries)}个国家和地区")

    # 标注范围内的国家（绿色）
    for country, lat, lon in within_range_countries:
        # 只在显示范围内标注
        if display_min_lon <= lon <= display_max_lon and display_min_lat <= lat <= display_max_lat:
            ax.plot(lon, lat, 'go', markersize=5)
            if font_set:
                ax.text(lon + 1, lat + 0.5, country, fontsize=9)

    # 标注范围外的国家（蓝色，仅标注在地图范围内的）
    for country, lat, lon in beyond_range_countries:
        if display_min_lon <= lon <= display_max_lon and display_min_lat <= lat <= display_max_lat:
            ax.plot(lon, lat, 'bo', markersize=3, alpha=0.6)

    # 添加中国主要城市标记
    for lat, lon in china_key_points:
        ax.plot(lon, lat, 'ro', markersize=6)

    # 添加图例
    china_patch = mpatches.Patch(color='red', label='中国主要城市')
    range_patch = mpatches.Patch(color='orange', label=f'{radius_km}公里范围')
    within_patch = mpatches.Patch(color='green', label='范围内国家')
    beyond_patch = mpatches.Patch(color='blue', alpha=0.6, label='范围外国家')

    if font_set:
        plt.legend(handles=[china_patch, range_patch, within_patch, beyond_patch], 
                  loc='lower right', fontsize=10)
        plt.title(f'以中国边界为起点的{radius_km}公里范围地图', fontsize=16)
        plt.xlabel('经度', fontsize=12)
        plt.ylabel('纬度', fontsize=12)
    else:
        plt.legend(handles=[china_patch, range_patch, within_patch, beyond_patch], 
                  loc='lower right', fontsize=10)
        plt.title(f'{radius_km}km Range Map Starting from China Border', fontsize=16)
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
    logger.info(f"地图已保存到: {svg_path} 和 {png_path}")

    if show_map:
        plt.show()
    else:
        plt.close()

    # 输出范围内的国家列表（使用日志而不是print）
    logger.info(f"以中国边界为起点{radius_km}公里范围内的主要国家和地区：")
    for i, (country, _, _) in enumerate(within_range_countries, 1):
        logger.info(f"{i}. {country}")

    return [svg_path, png_path]