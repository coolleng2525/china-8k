# 数据处理模块
"""
数据处理模块负责加载和管理地图所需的数据，包括JSON地图数据和国家数据。
"""

from .json_loader import load_china_map_data
from .country_data import get_countries_data

__all__ = ['load_china_map_data', 'get_countries_data']